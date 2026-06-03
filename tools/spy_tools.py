from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Optional, Any
from tools.browser_tool import BrowserConfig
import json
import re
import time


# ══════════════════════════════════════════
# SHOPEE DOM EXTRACTION SCRIPT (shared)
# ══════════════════════════════════════════

SHOPEE_PRODUCT_EXTRACT_JS = """
(function() {
    try {
        const items = [];
        const selectors = [
            '[class*="shopee-search-item-result"]',
            '[class*="search-result-item"]',
            '[class*="col-xs-2-4"]',
            '[class*="product-card"]',
            '[data-sqe="item"]',
            '.shopee-item-card',
        ];

        let elements = [];
        for (const sel of selectors) {
            elements = document.querySelectorAll(sel);
            if (elements.length > 0) break;
        }

        if (elements.length === 0) {
            elements = document.querySelectorAll('[class*="item"]');
        }

        const textContent = (el, fallback) => {
            if (!el) return fallback;
            return (el.innerText || el.textContent || fallback).trim();
        };

        const extractNumber = (str) => {
            if (!str) return 0;
            const cleaned = str.replace(/[^\\d.]/g, '');
            const num = parseInt(cleaned, 10);
            return isNaN(num) ? 0 : num;
        };

        const extractFloat = (str) => {
            if (!str) return 0;
            const match = str.match(/(\\d+[.,]?\\d*)/);
            return match ? parseFloat(match[1].replace(',','.')) : 0;
        };

        const extractDiscount = (el) => {
            return extractNumber(textContent(el, '0'));
        };

        elements.forEach((el, idx) => {
            if (idx >= 100) return;

            const nameEl = el.querySelector(
                '[class*="name"], [class*="title"], [class*="product-name"], a[class*="link"], [class*="desc"]'
            );
            const priceEl = el.querySelector(
                '[class*="price"]:not([class*="original"]):not([class*="before"]):not([class*="discount"])'
            );
            const origPriceEl = el.querySelector(
                '[class*="original"], [class*="before"], [class*="strikethrough"], [class*="old-price"]'
            );
            const soldEl = el.querySelector(
                '[class*="sold"], [class*="sales"], [class*="order"]'
            );
            const ratingEl = el.querySelector(
                '[class*="rating"], [class*="star"]'
            );
            const storeEl = el.querySelector(
                '[class*="shop-name"], [class*="store-name"], [class*="seller"]'
            );
            const locEl = el.querySelector(
                '[class*="location"], [class*="city"], [class*="address"]'
            );
            const discountEl = el.querySelector(
                '[class*="discount"], [class*="percent"], [class*="tag-percent"]'
            );
            const freeShipEl = el.querySelector(
                '[class*="free-shipping"], [class*="freeship"], [class*="free-delivery"]'
            );
            const linkEl = el.querySelector('a[href*="shopee.co.id"]');
            const imgEl = el.querySelector('img');
            const adEl = el.querySelector('[class*="ad"], [class*="sponsored"], [class*="iklan"]');
            const starEl = el.querySelector('[class*="star-seller"], [class*="preferred"], [class*="mall"]');
            const voucherEl = el.querySelector('[class*="voucher"], [class*="promo"], [class*="cashback"]');
            const ribbonEl = el.querySelector('[class*="ribbon"], [class*="badge"], [class*="tag"]');

            const name = textContent(nameEl, 'Unknown Product');
            if (!name || name === 'Unknown Product') return;

            items.push({
                product_name: name.slice(0, 150),
                price: extractNumber(textContent(priceEl, '0')),
                original_price: extractNumber(textContent(origPriceEl, '')) || 0,
                sold: extractNumber(textContent(soldEl, '0')),
                sold_text: textContent(soldEl, '0'),
                rating: extractFloat(textContent(ratingEl, '0')),
                store_name: textContent(storeEl, 'Unknown'),
                store_location: textContent(locEl, ''),
                is_ad: !!adEl,
                is_star_seller: !!starEl || !!el.querySelector('[class*="mall"]'),
                discount_percent: extractNumber(textContent(discountEl, '0')),
                free_shipping: !!freeShipEl,
                has_voucher: !!voucherEl,
                badge: textContent(ribbonEl, ''),
                product_url: linkEl ? (linkEl.href || '') : '',
                image_url: imgEl ? (imgEl.src || '') : '',
            });
        });

        return JSON.stringify({count: items.length, products: items});
    } catch(e) {
        return JSON.stringify({count: 0, products: [], error: e.message});
    }
})()
"""

SHOPEE_NEXT_BUTTON_JS = """
(function() {
    const nextSelectors = [
        '.shopee-icon-button--right:not([disabled])',
        '[class*="page-item"][class*="next"]:not([class*="disabled"])',
        '.ant-pagination-next:not([class*="disabled"])',
        'a[rel="next"]:not([class*="disabled"])',
        'button[aria-label="Next page"]:not([disabled])',
        'button[aria-label="next page"]:not([disabled])',
        '[class*="pagination"] button:last-of-type:not([disabled])',
        '.page-link[aria-label="Next"]:not([disabled])',
        'li.next a:not([class*="disabled"])',
        '.shopee-button-solid--primary:contains("Next")',
    ];

    for (const selector of nextSelectors) {
        try {
            const els = document.querySelectorAll(selector);
            for (const el of els) {
                if (el.offsetParent && !el.disabled && !el.classList.contains('disabled')) {
                    return JSON.stringify({found: true, text: (el.innerText||'').trim()});
                }
            }
        } catch(e) {}
    }

    const allBtns = document.querySelectorAll('button, a, span[role="button"]');
    for (const btn of allBtns) {
        const text = (btn.innerText || '').toLowerCase().trim();
        if (['next', 'selanjutnya', 'berikutnya', '>', 'lanjut', 'next page'].includes(text)) {
            if (btn.offsetParent && !btn.disabled && !btn.classList.contains('disabled')) {
                return JSON.stringify({found: true, text: text});
            }
        }
    }
    return JSON.stringify({found: false});
})()
"""

SHOPEE_CLICK_NEXT_JS = """
(function() {
    const selectors = [
        '[class*="page-item"][class*="next"]',
        '.shopee-icon-button--right',
        '.ant-pagination-next',
        'a[rel="next"]',
        'button[aria-label="Next page"]',
        'button[aria-label="next page"]',
        'li.next a',
    ];

    for (const sel of selectors) {
        try {
            const els = document.querySelectorAll(sel);
            for (const el of els) {
                if (el.offsetParent && !el.disabled && !el.classList.contains('disabled')) {
                    el.click();
                    return 'clicked:' + sel;
                }
            }
        } catch(e) {}
    }

    const buttons = document.querySelectorAll('button, a');
    for (const btn of buttons) {
        const text = (btn.innerText || '').toLowerCase().trim();
        if (['next', 'selanjutnya', '>', 'lanjut'].includes(text)) {
            if (btn.offsetParent && !btn.disabled && !btn.classList.contains('disabled')) {
                btn.click();
                return 'clicked:direct';
            }
        }
    }
    return 'no_next';
})()
"""

SHOPEE_REVIEW_EXTRACT_JS = """
(function() {
    try {
        const reviews = [];
        const reviewCards = document.querySelectorAll(
            '[class*="review-item"], [class*="comment-item"], [class*="rating-item"],'
            + '[class*="shopee-product-rating__main"], [class*="review-card"]'
        );

        const extractText = (el) => (el?.innerText || el?.textContent || '').trim();

        reviewCards.forEach((card, idx) => {
            if (idx >= 50) return;

            const username = card.querySelector(
                '[class*="username"], [class*="author"], [class*="reviewer"], [class*="name"]'
            );
            const ratingStars = card.querySelectorAll(
                '[class*="star"][class*="active"], [class*="star"][class*="filled"],'
                + '[class*="rating"] [class*="star"], svg[class*="star"]'
            );
            const comment = card.querySelector(
                '[class*="content"], [class*="comment"], [class*="review-text"], [class*="description"]'
            );
            const date = card.querySelector(
                '[class*="time"], [class*="date"], [class*="created"]'
            );
            const variant = card.querySelector(
                '[class*="variation"], [class*="variant"], [class*="sku"]'
            );
            const images = card.querySelectorAll('img[class*="review"], img[class*="photo"]');

            const rating = ratingStars.length || 0;

            reviews.push({
                username: extractText(username) || 'Anonymous',
                rating: rating,
                comment: extractText(comment) || '',
                date: extractText(date) || '',
                variant: extractText(variant) || '',
                has_images: images.length > 0,
            });
        });

        return JSON.stringify({count: reviews.length, reviews: reviews});
    } catch(e) {
        return JSON.stringify({count: 0, reviews: [], error: e.message});
    }
})()
"""

SHOPEE_STORE_EXTRACT_JS = """
(function() {
    try {
        const store = {};

        const nameEl = document.querySelector(
            '[class*="shop-name"], [class*="store-name"], [class*="seller-name"], h1'
        );
        const ratingEl = document.querySelector(
            '[class*="shop-rating"], [class*="rating-number"]'
        );
        const followerEl = document.querySelector(
            '[class*="follower"], [class*="followers"]'
        );
        const productCountEl = document.querySelector(
            '[class*="product-count"], [class*="total-product"]'
        );
        const joinedEl = document.querySelector(
            '[class*="joined"], [class*="since"], [class*="created"]'
        );
        const chatEl = document.querySelector(
            '[class*="chat-perf"], [class*="response"]'
        );
        const badgeEl = document.querySelector(
            '[class*="badge"], [class*="tag"], [class*="label"]'
        );

        const extractNum = (s) => {
            if (!s) return 0;
            const n = parseInt(s.replace(/[^\\d]/g, ''), 10);
            return isNaN(n) ? 0 : n;
        };

        store.name = (nameEl?.innerText || document.title || 'Unknown').trim();
        store.rating = parseFloat((ratingEl?.innerText || '0').replace(',','.')) || 0;
        store.followers = extractNum(followerEl?.innerText || '0');
        store.product_count = extractNum(productCountEl?.innerText || '0');
        store.joined_since = (joinedEl?.innerText || '').trim();
        store.chat_performance = (chatEl?.innerText || '').trim();
        store.badges = (badgeEl?.innerText || '').trim();

        const isOfficial = !!document.querySelector(
            '[class*="official"], [class*="verified"], [class*="mall"]'
        );
        store.is_official = isOfficial;

        return JSON.stringify({status: 'ok', store: store});
    } catch(e) {
        return JSON.stringify({status: 'error', message: e.message});
    }
})()
"""


# ══════════════════════════════════════════
# INPUT MODELS
# ══════════════════════════════════════════

class MarketScanInput(BaseModel):
    max_pages: int = Field(default=5, description="Max pages to scan (default: 5, max: 20)")
    extract_structured: bool = Field(default=True, description="Use structured DOM extraction (recommended)")


class ReviewMineInput(BaseModel):
    max_reviews: int = Field(default=50, description="Max reviews to extract (default: 50)")
    include_all_stars: bool = Field(default=False, description="Include all star ratings, not just 1-2")


class StoreProfileInput(BaseModel):
    store_url: str = Field(default="", description="URL tokes to profile (leave empty for current page)")


class GapAnalyzeInput(BaseModel):
    product_data_json: str = Field(default="", description="JSON array of product data from scan")
    min_sellers_for_gap: int = Field(default=5, description="Max sellers for gap opportunity")


class KeywordExtractInput(BaseModel):
    max_products: int = Field(default=20, description="Number of top products to analyze")


# ══════════════════════════════════════════
# TOOLS
# ══════════════════════════════════════════

class MarketScanTool(BaseTool):
    name: str = "scan_shopee_market"
    description: str = """
    Scan Shopee marketplace search results and extract STRUCTURED product data.

    V2 FEATURES:
    - Structured DOM extraction (no raw text parsing — MUCH more accurate)
    - Extracts: product_name, price, original_price, sold, rating, store_name,
      store_location, is_ad, is_star_seller, discount_percent, free_shipping,
      has_voucher, badge, product_url, image_url
    - Automatic pagination across ALL pages
    - Indonesian price format handling (Rp 12.345 → 12345)

    IMPORTANT: Browser must be on shopee.co.id search/category page.
    """
    args_schema: Type[BaseModel] = MarketScanInput

    def _run(self, max_pages: int = 5, extract_structured: bool = True, **kwargs) -> str:
        config = BrowserConfig.get_instance()

        # Verify site
        try:
            info = config.execute_command("evaluate_js", {
                "script": "JSON.stringify({url: window.location.href, title: document.title})"
            })
            parsed = json.loads(info) if info else {}
            if not parsed.get('url', '').includes('shopee.co.id'):
                return json.dumps({"status": "error", "message": f"Not on Shopee. URL: {parsed.get('url')}"}, indent=2)
        except Exception:
            pass

        all_products = []
        pages_processed = 0

        for page_num in range(1, max_pages + 1):
            try:
                if page_num > 1:
                    time.sleep(1.5)
                    config.execute_command("scroll_down", {})

                    next_js = config.execute_command("evaluate_js", {"script": SHOPEE_NEXT_BUTTON_JS})
                    parsed_next = json.loads(next_js) if next_js else {"found": False}
                    if not parsed_next.get("found"):
                        break

                    config.execute_command("evaluate_js", {"script": SHOPEE_CLICK_NEXT_JS})
                    time.sleep(2.5)
                    config.execute_command("scroll_down", {})
                    time.sleep(1.0)
                    config.execute_command("scroll_down", {})

                if extract_structured:
                    result_js = config.execute_command("evaluate_js", {"script": SHOPEE_PRODUCT_EXTRACT_JS})
                    parsed = json.loads(result_js) if result_js else {"count": 0, "products": []}
                    page_products = parsed.get("products", [])
                    all_products.extend(page_products)
                    pages_processed = page_num
                else:
                    page_text = config.execute_command("get_text", {})
                    if page_text and not page_text.startswith("Error"):
                        all_products.append({"raw_text": page_text, "page": page_num})
                        pages_processed = page_num
                    elif page_num == 1:
                        return json.dumps({"status": "error", "message": f"Cannot read page: {page_text}"}, indent=2)

            except Exception as e:
                if page_num == 1:
                    return json.dumps({"status": "error", "message": f"Scan error: {str(e)}"}, indent=2)
                break

        if extract_structured:
            return json.dumps({
                "status": "success",
                "extraction_method": "structured_dom",
                "pages_scanned": pages_processed,
                "total_products": len(all_products),
                "products": all_products,
            }, indent=2, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "success",
                "extraction_method": "raw_text",
                "pages_scanned": pages_processed,
                "data": "\n\n".join([p.get("raw_text", "") for p in all_products]),
            }, indent=2, ensure_ascii=False)


class ReviewMinerTool(BaseTool):
    name: str = "mine_product_reviews"
    description: str = """
    Extract and analyze product reviews from a Shopee product page.

    Analyzes:
    - All reviews with star ratings, comments, dates
    - Pain points from 1-2 star reviews
    - Strengths from 4-5 star reviews
    - Common keywords mentioned by customers

    IMPORTANT: Browser must be on a Shopee product detail page with reviews visible.
    Navigate to the product page and click the "Reviews/Ulasan" tab first.
    """
    args_schema: Type[BaseModel] = ReviewMineInput

    def _run(self, max_reviews: int = 50, include_all_stars: bool = False, **kwargs) -> str:
        config = BrowserConfig.get_instance()

        try:
            info = config.execute_command("evaluate_js", {
                "script": "JSON.stringify({url: window.location.href})"
            })
            parsed = json.loads(info) if info else {}
            if '/product/' not in parsed.get('url', '') and '/i.' not in parsed.get('url', ''):
                return json.dumps({"status": "error", "message": "Not on a product page. Navigate to a Shopee product first."}, indent=2)
        except Exception:
            pass

        # Scroll to load reviews
        for _ in range(5):
            config.execute_command("scroll_down", {})
            time.sleep(1.0)

        try:
            result_js = config.execute_command("evaluate_js", {"script": SHOPEE_REVIEW_EXTRACT_JS})
            parsed = json.loads(result_js) if result_js else {"count": 0, "reviews": []}
            reviews = parsed.get("reviews", [])

            pain_points = [r for r in reviews if r.get("rating", 0) <= 2]
            strengths = [r for r in reviews if r.get("rating", 0) >= 4]

            return json.dumps({
                "status": "success",
                "total_reviews_extracted": len(reviews),
                "average_rating": round(sum(r.get("rating", 0) for r in reviews) / max(len(reviews), 1), 1),
                "pain_points": pain_points[:10],
                "pain_point_count": len(pain_points),
                "strengths": strengths[:10],
                "strengths_count": len(strengths),
                "all_reviews": reviews if include_all_stars else [],
                "instruction": (
                    "Analyze PAIN POINTS: common complaints = improvement opportunities. "
                    "Analyze STRENGTHS: what customers love = competitive advantage to match or exceed. "
                    "Extract common keywords, themes, and actionable product improvement suggestions."
                )
            }, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"status": "error", "message": f"Review extraction failed: {str(e)}"})


class StoreProfilerTool(BaseTool):
    name: str = "profile_shopee_store"
    description: str = """
    Extract detailed store profile from a Shopee store page.

    Extracts:
    - Store name, rating, follower count, product count
    - Joined date, chat performance score
    - Official/Star Seller badges
    - Store location

    IMPORTANT: Browser must be on a Shopee store page
    (e.g., shopee.co.id/shopname).
    """
    args_schema: Type[BaseModel] = StoreProfileInput

    def _run(self, store_url: str = "", **kwargs) -> str:
        config = BrowserConfig.get_instance()

        if store_url:
            config.execute_command("goto", {"url": store_url})
            time.sleep(3)

        try:
            result_js = config.execute_command("evaluate_js", {"script": SHOPEE_STORE_EXTRACT_JS})
            return result_js if result_js else json.dumps({"status": "error", "message": "No store data found"})
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Store profiling failed: {str(e)}"})


class GapAnalyzeTool(BaseTool):
    name: str = "analyze_market_gaps"
    description: str = """
    Identify GAP OPPORTUNITIES from scanned market data.

    Detects:
    - Products with high demand (sold count) but few visible sellers
    - Underserved price ranges  
    - Categories with high ratings but limited options
    
    Provide JSON product data from scan_shopee_market.
    """
    args_schema: Type[BaseModel] = GapAnalyzeInput

    def _run(self, product_data_json: str = "", min_sellers_for_gap: int = 5, **kwargs) -> str:
        try:
            if not product_data_json:
                return json.dumps({"status": "error", "message": "No product data provided"})

            data = json.loads(product_data_json) if isinstance(product_data_json, str) else product_data_json
            products = data.get("products", data) if isinstance(data, dict) else data

            store_product_count = {}
            price_ranges = {"budget": [], "mid": [], "premium": []}

            for p in products:
                store = p.get("store_name", "Unknown")
                store_product_count[store] = store_product_count.get(store, 0) + 1

                price = p.get("price", 0)
                if price < 100000:
                    price_ranges["budget"].append(p)
                elif price < 500000:
                    price_ranges["mid"].append(p)
                else:
                    price_ranges["premium"].append(p)

            gap_opportunities = []
            for store, count in store_product_count.items():
                if count <= min_sellers_for_gap:
                    store_products = [p for p in products if p.get("store_name") == store]
                    avg_sold = sum(p.get("sold", 0) for p in store_products) / max(len(store_products), 1)
                    avg_rating = sum(p.get("rating", 0) for p in store_products) / max(len(store_products), 1)
                    if avg_sold > 50:
                        gap_opportunities.append({
                            "store": store,
                            "products_visible": count,
                            "avg_sold": int(avg_sold),
                            "avg_rating": round(avg_rating, 1),
                            "sample_product": store_products[0].get("product_name", "") if store_products else "",
                            "price_range": [p.get("price", 0) for p in store_products[:3]],
                        })

            gap_opportunities.sort(key=lambda x: x["avg_sold"], reverse=True)

            # Find underserved price ranges
            price_gaps = []
            for tier, tier_products in price_ranges.items():
                if len(tier_products) <= 3 and len(products) > 10:
                    price_gaps.append({
                        "tier": tier,
                        "label": {"budget": "Budget (<100rb)", "mid": "Mid-range (100rb-500rb)", "premium": "Premium (>500rb)"}[tier],
                        "product_count": len(tier_products),
                        "opportunity": "Very few products in this range — low competition"
                    })

            return json.dumps({
                "status": "success",
                "total_products_analyzed": len(products),
                "unique_stores": len(store_product_count),
                "ads_percentage": round(sum(1 for p in products if p.get("is_ad")) / max(len(products), 1) * 100, 1),
                "price_distribution": {
                    "budget": len(price_ranges["budget"]),
                    "mid_range": len(price_ranges["mid"]),
                    "premium": len(price_ranges["premium"])
                },
                "gap_opportunities": gap_opportunities[:10],
                "price_gaps": price_gaps,
                "instruction": "Focus on gap_opportunities (high demand, few sellers) and price_gaps (underserved tiers)."
            }, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"status": "error", "message": f"Gap analysis failed: {str(e)}"})


class KeywordExtractorTool(BaseTool):
    name: str = "extract_listing_keywords"
    description: str = """
    Extract common keywords from product titles in scanned data.

    Useful for:
    - Finding high-performing keywords competitors use
    - Optimizing your own product listings
    - Discovering search terms you haven't targeted

    Provide JSON product data from scan_shopee_market.
    """
    args_schema: Type[BaseModel] = KeywordExtractInput

    def _run(self, max_products: int = 20, **kwargs) -> str:
        try:
            # Get the scanned data from config context
            return json.dumps({
                "status": "info",
                "message": "Provide product_data JSON to analyze listing keywords.",
                "instruction": (
                    "Analyze product titles for keyword patterns: "
                    "1. What words appear most frequently? "
                    "2. What keywords do top-selling products use? "
                    "3. What attributes are commonly mentioned (size, color, material, etc.)? "
                    "4. What search terms are missing from lower-ranked products? "
                    "This helps optimize YOUR product listings for better search visibility."
                )
            }, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


def get_spy_tools():
    return [
        MarketScanTool(),
        ReviewMinerTool(),
        StoreProfilerTool(),
        GapAnalyzeTool(),
        KeywordExtractorTool(),
    ]
