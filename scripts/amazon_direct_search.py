#!/usr/bin/env python3
"""
Scrape Amazon.in search results page directly and identify the minimum priced iPhone 16.

Usage:
    python scripts/amazon_direct_search.py [--headless] [--timeout SECONDS]

This script:
1. Opens the direct Amazon search results URL
2. Waits for products to load
3. Captures first 6 product names and prices
4. Identifies and displays the minimum priced product
5. Generates an HTML report with results
"""
import argparse
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_price(price_str):
    """Extract numeric price from price string (e.g., '₹45,999' -> 45999)."""
    if not price_str:
        return float('inf')
    # Remove currency symbols and commas
    cleaned = price_str.replace('₹', '').replace(',', '').replace('(', '').replace(')', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return float('inf')


def generate_html_results(products, output_file='amazon_results.html', search_url=None):
    """Generate an HTML page displaying products and the lowest-priced one."""
    if not products:
        html_content = '<html><body><h1>No products found</h1></body></html>'
    else:
        lowest = min(products, key=lambda p: p['price_value'])
        
        products_html = ''.join([
            f'''<tr {"style='background-color: #d4edda;'" if prod['price_value'] == lowest['price_value'] else ""}>
                <td>{i}</td>
                <td>{prod['name'][:80]}</td>
                <td>{prod['price']}</td>
                <td style="text-align: right; font-weight: bold;">₹{prod['price_value']:,.2f}</td>
              </tr>'''
            for i, prod in enumerate(products, 1)
        ])
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Amazon iPhone 16 - Minimum Price Product</title>
    <style>
        * {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #232f3e; border-bottom: 4px solid #FF9900; padding-bottom: 10px; margin-top: 0; }}
        h2 {{ color: #232f3e; margin-top: 30px; }}
        .summary {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .summary p {{
            margin: 8px 0;
            font-size: 16px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        th {{
            background-color: #232f3e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
            border-bottom: 2px solid #FF9900;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f9f9f9;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .lowest {{
            background-color: #d4edda;
            padding: 25px;
            border-radius: 8px;
            margin-top: 30px;
            border-left: 6px solid #28a745;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .lowest h2 {{
            color: #155724;
            margin-top: 0;
            font-size: 28px;
        }}
        .lowest p {{
            color: #155724;
            margin: 12px 0;
            font-size: 16px;
        }}
        .price-highlight {{
            font-size: 24px;
            font-weight: bold;
            color: #28a745;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }}
        .stat-box {{
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            flex: 1;
        }}
        .stat-label {{
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 20px;
            font-weight: bold;
            color: #232f3e;
        }}
        .timestamp {{
            color: #666;
            font-size: 12px;
            margin-top: 20px;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛍️ Amazon.in iPhone 16 - Minimum Price Product</h1>
        
        <div class="summary">
            <p><strong>Search URL:</strong> <a href="{search_url if search_url else '#'}" target="_blank">{search_url if search_url else 'Direct page'}</a></p>
            <p><strong>Products Analyzed:</strong> {len(products)} products</p>
            <p><strong>Analysis Date:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <h2>📋 All Products ({len(products)})</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">#</th>
                    <th>Product Name</th>
                    <th>Price (Original)</th>
                    <th style="text-align: right;">Numeric Price</th>
                </tr>
            </thead>
            <tbody>
                {products_html}
            </tbody>
        </table>
        
        <div class="lowest">
            <h2>🏆 MINIMUM PRICED PRODUCT</h2>
            <p><strong>Product Name:</strong></p>
            <p>{lowest['name']}</p>
            
            <p><strong>Price:</strong></p>
            <p class="price-highlight">{lowest['price']}</p>
            
            <p><strong>Numeric Value:</strong></p>
            <p class="price-highlight">₹{lowest['price_value']:,.2f}</p>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">Lowest Price</div>
                    <div class="stat-value">₹{lowest['price_value']:,.0f}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Ranking</div>
                    <div class="stat-value">#{[i for i, p in enumerate(products, 1) if p['price_value'] == lowest['price_value']][0]}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Total Products</div>
                    <div class="stat-value">{len(products)}</div>
                </div>
            </div>
        </div>
        
        <div class="timestamp">Generated on {time.strftime('%d %B %Y at %H:%M:%S')}</div>
    </div>
</body>
</html>'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file


def scrape_amazon_search(driver, url, wait_timeout=15, max_products=6):
    """Scrape products from the Amazon search results page.
    
    Returns:
        list: List of dicts with 'name', 'price', 'price_value' keys
    """
    driver.get(url)
    print(f"Loading: {url}\n")
    time.sleep(2)
    
    # Wait for search results to load
    wait = WebDriverWait(driver, wait_timeout)
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
    )
    print("✓ Search results loaded.\n")
    
    # Collect product data
    products = []
    result_elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    
    print(f"Found {len(result_elements)} result elements. Extracting first {max_products} valid products...\n")
    
    for elem in result_elements:
        if len(products) >= max_products:
            break
        
        try:
            # Get product name
            name_elem = elem.find_element(By.XPATH, ".//span[@data-component-type='s-title']//span")
            product_name = name_elem.text.strip()
            
            # Get price - try multiple locators
            price_text = 'N/A'
            try:
                # Try primary price locator
                price_elem = elem.find_element(By.XPATH, ".//span[@data-a-price-whole]")
                price_text = price_elem.text.strip()
            except:
                try:
                    # Try alternate price locator
                    price_elem = elem.find_element(By.XPATH, ".//span[contains(@class, 'a-price-whole')]")
                    price_text = price_elem.text.strip()
                except:
                    try:
                        # Try price symbol + amount
                        price_elem = elem.find_element(By.XPATH, ".//span[contains(@class, 'a-price')]//span[contains(text(), '₹')]")
                        price_text = price_elem.text.strip()
                    except:
                        pass
            
            if product_name and price_text != 'N/A':
                price_value = parse_price(price_text)
                products.append({
                    'name': product_name,
                    'price': price_text,
                    'price_value': price_value
                })
                print(f"✓ Product {len(products)}: {product_name[:70]}...")
                print(f"  Price: {price_text} (₹{price_value:,.2f})\n")
        except Exception as e:
            continue
    
    return products


def main():
    parser = argparse.ArgumentParser(description='Scrape Amazon search results and find minimum priced product.')
    parser.add_argument('--url', type=str, default='https://www.amazon.in/s?k=iPhone+16&ref=nb_sb_noss',
                       help='Amazon search results URL')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
    parser.add_argument('--timeout', type=int, default=15, help='Timeout in seconds for element waits')
    parser.add_argument('--max-products', type=int, default=6, help='Max products to capture (default: 6)')
    parser.add_argument('--screenshot', type=str, default=None, help='Save screenshot after scraping')
    parser.add_argument('--results-html', type=str, default='amazon_results.html', help='Output HTML file')
    args = parser.parse_args()

    options = Options()
    if args.headless:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        products = scrape_amazon_search(
            driver,
            url=args.url,
            wait_timeout=args.timeout,
            max_products=args.max_products
        )

        if args.screenshot:
            time.sleep(1)
            driver.save_screenshot(args.screenshot)
            print(f"\n📸 Screenshot saved: {args.screenshot}")

        # Console output
        print("\n" + "="*80)
        print("PRODUCT SUMMARY")
        print("="*80)
        for i, prod in enumerate(products, 1):
            print(f"{i}. {prod['name'][:70]}")
            print(f"   Price: {prod['price']} (₹{prod['price_value']:,.2f})")

        if products:
            lowest = min(products, key=lambda p: p['price_value'])
            print("\n" + "="*80)
            print("🏆 MINIMUM PRICED PRODUCT")
            print("="*80)
            print(f"Name:  {lowest['name']}")
            print(f"Price: {lowest['price']}")
            print(f"Value: ₹{lowest['price_value']:,.2f}")
            print("="*80)
            
            # Generate and open HTML
            html_file = generate_html_results(products, args.results_html, args.url)
            print(f"\n📄 Results HTML: {html_file}")
            
            abs_path = os.path.abspath(html_file)
            file_url = f'file:///{abs_path}'.replace('\\', '/')
            print(f"🌐 Opening in browser...\n")
            driver.get(file_url)
            
            if not args.headless:
                try:
                    input('Press Enter to close...')
                except KeyboardInterrupt:
                    pass
        else:
            print("⚠ No valid products found.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if not args.headless:
            try:
                input('\nPress Enter to close...')
            except KeyboardInterrupt:
                pass
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
