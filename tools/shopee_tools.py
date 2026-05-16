from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Optional, Any
import json
import re


class BrowserConfig:
    _instance = None
    _page: Optional[Any] = None
    _queue: Optional[Any] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_page(self, page: Any):
        self._page = page

    def get_page(self) -> Optional[Any]:
        return self._page

    def set_queue(self, queue: Any):
        self._queue = queue

    def execute_command(self, action: str, params: dict = None) -> str:
        if self._queue is None:
            return "Error: Browser command queue not initialized."
        
        from queue import Queue
        result_queue = Queue()
        
        self._queue.put({
            "action": action,
            "params": params or {},
            "result_queue": result_queue
        })
        
        try:
            result = result_queue.get(timeout=30)
            if result["status"] == "success":
                return result["data"]
            else:
                return f"Error: {result['message']}"
        except Exception as e:
            return f"Error: Command timed out or failed: {str(e)}"


class ExtractShopeeAdsMetricsInput(BaseModel):
    pass


class ExtractShopeeAdsMetricsTool(BaseTool):
    name: str = "extract_shopee_ads_metrics"
    description: str = """
    Use this tool to extract advertising metrics from Shopee Seller Center ads dashboard.
    
    This tool will:
    1. Navigate to the Shopee Ads dashboard
    2. Extract the campaign/product table data including:
       - Product Name
       - Shopee Cost (Biaya Iklan)
       - GMV/Sales Revenue (Omset Penjualan)
       - Clicks (Jumlah Klik)
       - Conversion Rate (Tingkat Konversi/CR)
    
    3. Return the data as a clean JSON array
    
    IMPORTANT: This tool requires the browser to be logged into Shopee Seller Center.
    If not logged in, the agent will navigate to the login page first.
    """
    args_schema: Type[BaseModel] = ExtractShopeeAdsMetricsInput

    def _run(self, **kwargs) -> str:
        config = BrowserConfig.get_instance()
        
        result = config.execute_command("goto", {"url": "https://seller.shopee.co.id/ads/spsa/product"})
        
        result += "\n" + config.execute_command("wait", {"timeout": 3000})
        
        result += "\n" + config.execute_command("scroll_down")
        
        page_text = config.execute_command("get_text")
        
        return page_text


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
