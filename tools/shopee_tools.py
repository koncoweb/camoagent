from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Optional, Any
from tools.browser_tool import BrowserConfig
import json
import re
import time


class ExtractShopeeAdsMetricsInput(BaseModel):
    max_pages: int = Field(default=20, description="Maximum number of pages to iterate through pagination (default: 20, set 1 for single page only)")


class ExtractShopeeAdsMetricsTool(BaseTool):
    name: str = "extract_shopee_ads_metrics"
    description: str = """
    Use this tool to extract advertising metrics from Shopee Seller Center ads dashboard.
    
    This tool handles PAGINATION AUTOMATICALLY:
    - Detects Next/Previous buttons on the Shopee ads table
    - Iterates through ALL pages to collect complete data
    - Extracts the campaign/product table data including:
       - Product Name
       - Shopee Cost (Biaya Iklan)
       - GMV/Sales Revenue (Omset Penjualan)
       - Clicks (Jumlah Klik)
       - Conversion Rate (Tingkat Konversi/CR)
    
    Use max_pages=1 to extract only the current page (no pagination).
    Use max_pages=20 (default) to iterate up to 20 pages.
    
    IMPORTANT: 
    - Requires browser to be logged into Shopee Seller Center
    - User should manually navigate to the ads dashboard first
    """
    args_schema: Type[BaseModel] = ExtractShopeeAdsMetricsInput

    def _run(self, max_pages: int = 20, **kwargs) -> str:
        config = BrowserConfig.get_instance()
        
        try:
            result = config.execute_command("evaluate_js", {
                "script": """
                (function() {
                    // Check if we have login page
                    if (document.querySelector('input[name="password"]') || 
                        window.location.href.includes('/login')) {
                        return JSON.stringify({status: 'not_logged_in'});
                    }
                    
                    // Check for table data (Shopee uses various table structures)
                    let hasTable = document.querySelector('table, [role="table"], .table-wrapper, .ads-table');
                    return JSON.stringify({
                        status: 'ok',
                        hasTable: !!hasTable,
                        url: window.location.href
                    });
                })()
                """
            })
            
            if '"status":"not_logged_in"' in result or '"not_logged_in"' in result:
                return json.dumps({
                    "status": "error",
                    "message": "Browser is not logged into Shopee. Please login manually first."
                }, indent=2)
            
        except Exception:
            pass
        
        collected_product_data = []
        pages_processed = 0
        
        for page_num in range(1, max_pages + 1):
            try:
                if page_num > 1:
                    time.sleep(1.0)
                    config.execute_command("scroll_down", {})
                    time.sleep(1.0)
                
                    next_result = config.execute_command("evaluate_js", {
                        "script": """
                        (function() {
                            // Try multiple Next button selectors common in Shopee
                            const nextSelectors = [
                                'button.next:not([disabled])',
                                'button:has(.shopee-icon-button__right)',
                                '.pagination button:contains("Next")',
                                '.pagination .next:not([disabled])',
                                'button[aria-label="Next"]:not([disabled])',
                                '[class*="pagination"] button:last-child:not([disabled])',
                                '.ads-pagination .next:not([disabled])',
                                'li.next a:not([disabled])',
                                '.ant-pagination-next:not([disabled])',
                                '.page-next:not([disabled])',
                                'button:has([class*="right"]):not([disabled])',
                                'span.next a:not([class*="disabled"])',
                                'a[rel="next"]:not([class*="disabled"])',
                            ];
                            
                            for (const selector of nextSelectors) {
                                try {
                                    const el = document.querySelector(selector);
                                    if (el && el.offsetParent !== null) {
                                        return JSON.stringify({
                                            found: true,
                                            selector: selector,
                                            text: el.innerText || el.textContent || '',
                                            disabled: el.hasAttribute('disabled') || el.classList.contains('disabled'),
                                            x: el.getBoundingClientRect().x,
                                            y: el.getBoundingClientRect().y
                                        });
                                    }
                                } catch(e) { continue; }
                            }
                            
                            // Check all buttons for Next label
                            const buttons = document.querySelectorAll('button, a.btn, span[role="button"]');
                            for (const btn of buttons) {
                                const text = (btn.innerText || btn.textContent || '').toLowerCase().trim();
                                if (['next', 'selanjutnya', 'berikutnya', 'selanjutnya >', 'lanjut'].includes(text) ||
                                    ['>', '›', '»'].includes(text) ||
                                    btn.getAttribute('aria-label')?.toLowerCase()?.includes('next')) {
                                    if (btn.offsetParent !== null && !btn.hasAttribute('disabled') && !btn.classList.contains('disabled')) {
                                        return JSON.stringify({
                                            found: true,
                                            selector: `button:has-text("${text}")`,
                                            text: btn.innerText || btn.textContent || '',
                                            disabled: false,
                                            x: btn.getBoundingClientRect().x,
                                            y: btn.getBoundingClientRect().y
                                        });
                                    }
                                }
                            }
                            
                            return JSON.stringify({found: false});
                        })()
                        """
                    })
                    
                    parsed_next = json.loads(next_result) if next_result else {"found": False}
                    
                    if not parsed_next.get("found"):
                        break
                    
                    if parsed_next.get("disabled"):
                        break
                    
                    time.sleep(0.3)
                    
                    click_result = config.execute_command("evaluate_js", {
                        "script": """
                        (function() {
                            const selectors = [
                                'button.next:not([disabled])',
                                '.ant-pagination-next:not([disabled])',
                                '.page-next:not([disabled])',
                                'a[rel="next"]',
                                'li.next a',
                                '.pagination .next:not([disabled])',
                            ];
                            
                            for (const selector of selectors) {
                                try {
                                    const el = document.querySelector(selector);
                                    if (el && el.offsetParent !== null) {
                                        el.click();
                                        return 'clicked:' + selector;
                                    }
                                } catch(e) {}
                            }
                            
                            const buttons = document.querySelectorAll('button, a');
                            for (const btn of buttons) {
                                const text = (btn.innerText || btn.textContent || '').toLowerCase().trim();
                                if (['next', 'selanjutnya', '>', '›', '»'].includes(text) ||
                                    btn.getAttribute('aria-label')?.toLowerCase()?.includes('next')) {
                                    if (btn.offsetParent !== null && !btn.hasAttribute('disabled') && !btn.classList.contains('disabled')) {
                                        btn.click();
                                        return 'clicked:text-match';
                                    }
                                }
                            }
                            
                            return 'no_next_found';
                        })()
                        """
                    })
                    
                    time.sleep(2.0)
                    
                    config.execute_command("scroll_down", {})
                    time.sleep(1.5)
                
                page_text = config.execute_command("get_text", {})
                
                if page_text and not page_text.startswith("Error"):
                    collected_product_data.append(page_text)
                    pages_processed = page_num
                else:
                    if page_num == 1:
                        return json.dumps({
                            "status": "error",
                            "message": f"Could not read page content: {page_text}"
                        }, indent=2)
                    break
                
            except Exception as e:
                if page_num == 1:
                    return json.dumps({
                        "status": "error",
                        "message": f"Error during extraction: {str(e)}"
                    }, indent=2)
                break
        
        combined_text = "\n\n--- PAGE {} ---\n\n".format(1) + collected_product_data[0]
        for i, page_data in enumerate(collected_product_data[1:], start=2):
            combined_text += "\n\n--- PAGE {} ---\n\n".format(i) + page_data
        
        return json.dumps({
            "status": "success",
            "pages_extracted": pages_processed,
            "total_pages_attempted": max_pages,
            "data": combined_text,
            "instruction": "Parse this text into JSON format with fields: product_name, shopee_cost, gmv, clicks, cr, selling_price. All pages are separated by '--- PAGE N ---' markers."
        }, indent=2, ensure_ascii=False)


class CalculateActualFinancialsInput(BaseModel):
    raw_data: str = Field(..., description="Raw JSON data from Shopee ads extraction")
    hpp_percentage: float = Field(default=0.7, description="HPP (Cost of Goods) as percentage of selling price (0.0-1.0)")
    operational_cost: float = Field(default=0, description="Fixed operational costs")
    admin_fee_percentage: float = Field(default=0.023, description="Shopee admin fee percentage (default: 2.3%)")


class CalculateActualFinancialsTool(BaseTool):
    name: str = "calculate_actual_financials"
    description: str = """
    Use this tool to calculate actual financial metrics for Shopee ads products.
    
    This tool processes JSON data and calculates:
    1. Actual Cost = Shopee Cost * 1.11 (adding 11% VAT on ads)
    2. Actual ROAS = GMV / Actual Cost
    3. Net Profit per Product = Selling Price - HPP - (Admin Fee % * Selling Price) - Operational Cost
    4. Break-Even ROAS = Selling Price / Net Profit per Product
    5. Max CPC (Target Max Bid) = Net Profit per Product * Conversion Rate (CR)
    
    Classification:
    - "Bagus" (Good): Actual ROAS > Target ROAS (default: 5.0)
    - "Cukup" (Moderate): Target ROAS > Actual ROAS > Break-Even ROAS
    - "Rugi" (Loss): Actual ROAS < Break-Even ROAS
    
    Returns enriched JSON with all calculated fields and performance status.
    """
    args_schema: Type[BaseModel] = CalculateActualFinancialsInput

    def _run(
        self, 
        raw_data: str,
        hpp_percentage: float = 0.7,
        operational_cost: float = 0,
        admin_fee_percentage: float = 0.023,
        **kwargs
    ) -> str:
        try:
            if isinstance(raw_data, str):
                data = json.loads(raw_data)
            else:
                data = raw_data
            
            if not isinstance(data, list):
                if isinstance(data, dict) and 'products' in data:
                    data = data['products']
                else:
                    return json.dumps({
                        "status": "error",
                        "message": "Invalid data format. Expected a list of products or dict with 'products' key."
                    }, indent=2)
            
            results = []
            
            for product in data:
                product_name = product.get('product_name', product.get('name', 'Unknown'))
                shopee_cost = float(product.get('shopee_cost', product.get('cost', 0)))
                gmv = float(product.get('gmv', product.get('sales', product.get('revenue', 0))))
                clicks = float(product.get('clicks', product.get('click', 0)))
                cr = float(product.get('cr', product.get('conversion_rate', 0)))
                
                if cr > 1:
                    cr = cr / 100
                
                selling_price = float(product.get('selling_price', product.get('price', 0)))
                if selling_price == 0 and gmv > 0 and clicks > 0:
                    selling_price = gmv / clicks if clicks > 0 else 0
                
                actual_cost = shopee_cost * 1.11
                
                actual_roas = gmv / actual_cost if actual_cost > 0 else 0
                
                net_profit = selling_price - (hpp_percentage * selling_price) - (admin_fee_percentage * selling_price) - operational_cost
                
                break_even_roas = selling_price / net_profit if net_profit > 0 else 0
                
                max_cpc = net_profit * cr if cr > 0 else 0
                
                target_roas = 5.0
                if actual_roas > target_roas:
                    status = "Bagus"
                elif actual_roas > break_even_roas:
                    status = "Cukup"
                else:
                    status = "Rugi"
                
                enriched_product = {
                    "product_name": product_name,
                    "shopee_cost": round(shopee_cost, 2),
                    "actual_cost": round(actual_cost, 2),
                    "gmv": round(gmv, 2),
                    "actual_roas": round(actual_roas, 2),
                    "selling_price": round(selling_price, 2),
                    "hpp": round(hpp_percentage * selling_price, 2),
                    "admin_fee": round(admin_fee_percentage * selling_price, 2),
                    "net_profit": round(net_profit, 2),
                    "break_even_roas": round(break_even_roas, 2),
                    "clicks": int(clicks),
                    "conversion_rate": round(cr * 100, 2),
                    "max_cpc": round(max_cpc, 2),
                    "status": status
                }
                
                results.append(enriched_product)
            
            return json.dumps({
                "status": "success",
                "products": results,
                "summary": {
                    "total_products": len(results),
                    "total_cost": round(sum(p['shopee_cost'] for p in results), 2),
                    "total_gmv": round(sum(p['gmv'] for p in results), 2),
                    "avg_roas": round(sum(p['actual_roas'] for p in results) / len(results), 2) if results else 0,
                    "bagus_count": sum(1 for p in results if p['status'] == 'Bagus'),
                    "cukup_count": sum(1 for p in results if p['status'] == 'Cukup'),
                    "rugi_count": sum(1 for p in results if p['status'] == 'Rugi')
                }
            }, indent=2, ensure_ascii=False)
            
        except json.JSONDecodeError as e:
            return json.dumps({
                "status": "error",
                "message": f"JSON parsing error: {str(e)}",
                "raw_data_preview": raw_data[:500] if len(raw_data) > 500 else raw_data
            }, indent=2)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Calculation error: {str(e)}"
            }, indent=2)


class GenerateAdsRecommendationInput(BaseModel):
    financial_data: str = Field(..., description="JSON data from CalculateActualFinancials tool")


class GenerateAdsRecommendationTool(BaseTool):
    name: str = "generate_ads_recommendation"
    description: str = """
    Use this tool to generate bid optimization recommendations based on financial analysis.
    
    Recommendation Rules:
    - "Rugi" (Loss): Recommend "Turunkan Bid ke Max CPC atau Pause"
    - "Cukup" (Moderate): Recommend "Pertahankan Bid"
    - "Bagus" (Good): Recommend "Naikkan Bid 5%"
    
    Returns recommendations in markdown format with summary table.
    """
    args_schema: Type[BaseModel] = GenerateAdsRecommendationInput

    def _run(self, financial_data: str, **kwargs) -> str:
        try:
            if isinstance(financial_data, str):
                data = json.loads(financial_data)
            else:
                data = financial_data
            
            products = data.get('products', [])
            
            recommendations = []
            for product in products:
                status = product.get('status', 'Unknown')
                product_name = product.get('product_name', 'Unknown')
                max_cpc = product.get('max_cpc', 0)
                
                if status == "Rugi":
                    action = "Turunkan Bid ke Max CPC atau Pause"
                elif status == "Cukup":
                    action = "Pertahankan Bid"
                else:
                    action = "Naikkan Bid 5%"
                
                recommendations.append({
                    "product_name": product_name,
                    "current_status": status,
                    "max_cpc": max_cpc,
                    "recommendation": action
                })
            
            summary = data.get('summary', {})
            
            markdown_output = f"""## 📊 Shopee Ads Optimization Report

### Summary
| Metric | Value |
|--------|-------|
| Total Products | {summary.get('total_products', 0)} |
| Total Cost | Rp {summary.get('total_cost', 0):,.0f} |
| Total GMV | Rp {summary.get('total_gmv', 0):,.0f} |
| Average ROAS | {summary.get('avg_roas', 0):.2f}x |

### Performance Distribution
| Status | Count | Emoji |
|--------|-------|-------|
| ✅ Bagus | {summary.get('bagus_count', 0)} | 🎯 |
| ⚠️ Cukup | {summary.get('cukup_count', 0)} | ⏸️ |
| ❌ Rugi | {summary.get('rugi_count', 0)} | 🛑 |

---

## 📋 Detailed Recommendations

| Product | Status | Max CPC | Action |
|---------|--------|---------|--------|
"""
            
            for rec in recommendations:
                status_emoji = "✅" if rec['status'] == 'Bagus' else "⚠️" if rec['status'] == 'Cukup' else "❌"
                markdown_output += f"| {status_emoji} {rec['product_name'][:40]} | {rec['current_status']} | Rp {rec['max_cpc']:,.0f} | {rec['recommendation']} |\n"
            
            return markdown_output
            
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"


def get_shopee_tools():
    return [
        ExtractShopeeAdsMetricsTool(),
        CalculateActualFinancialsTool(),
        GenerateAdsRecommendationTool(),
    ]
