#!/usr/bin/env python3
"""
Search iPhone on Amazon.in homepage and find minimum priced product.

Usage:
    python scripts/amazon_homepage_search.py [--headless] [--search-term TERM]

This script:
1. Opens https://www.amazon.in/
2. Searches for iPhone (or custom term)
3. Captures first 6 products with prices
4. Identifies minimum priced product
5. Generates HTML report with results
6. Displays results in browser
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
from selenium.webdriver.common.keys import Keys


def parse_price(price_str):
    """Extract numeric price from price string (e.g., '₹45,999' -> 45999)."""
    if not price_str:
        return float('inf')
    cleaned = price_str.replace('₹', '').replace(',', '').replace('(', '').replace(')', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return float('inf')


def generate_html_results(products, search_term, output_file='amazon_results.html'):
    """Generate HTML report with products and minimum priced item."""
    if not products:
        html_content = '<html><body><h1>No products found</h1></body></html>'
    else:
        lowest = min(products, key=lambda p: p['price_value'])
        rank = [i for i, p in enumerate(products, 1) if p['price_value'] == lowest['price_value']][0]
        
        products_html = ''.join([
            f'''<tr {"style='background-color: #fff3cd;'" if prod['price_value'] == lowest['price_value'] else ""}>
                <td>{i}</td>
                <td>{prod['name'][:80]}</td>
                <td>{prod['price']}</td>
                <td style="text-align: right; font-weight: bold; color: {"#28a745" if prod['price_value'] == lowest['price_value'] else "#232f3e"}">₹{prod['price_value']:,.2f}</td>
              </tr>'''
            for i, prod in enumerate(products, 1)
        ])
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Amazon iPhone Search - Minimum Price</title>
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
            font-size: 28px;
            font-weight: bold;
            color: #28a745;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
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
        <h1>🛍️ Amazon.in - {search_term} - MINIMUM PRICE PRODUCT</h1>
        
        <div class="summary">
            <p><strong>Search Term:</strong> {search_term}</p>
            <p><strong>Products Analyzed:</strong> {len(products)} products</p>
            <p><strong>Source:</strong> https://www.amazon.in/</p>
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
            <h2>🏆 MINIMUM PRICED {search_term.upper()}</h2>
            <p><strong>Product Name:</strong></p>
            <p style="font-size: 18px;">{lowest['name']}</p>
            
            <p><strong>Price:</strong></p>
            <p class="price-highlight">{lowest['price']}</p>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">Minimum Price</div>
                    <div class="stat-value" style="color: #28a745;">₹{lowest['price_value']:,.0f}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Position in Results</div>
                    <div class="stat-value">#{rank}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Total Products</div>
                    <div class="stat-value">{len(products)}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Price Range</div>
                    <div class="stat-value">₹{min(p['price_value'] for p in products):,.0f} - ₹{max(p['price_value'] for p in products):,.0f}</div>
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


def search_amazon_homepage(driver, search_term='iPhone', wait_timeout=20, max_products=6):
    """Search Amazon homepage and extract products.
    
    Returns:
        list: List of dicts with 'name', 'price', 'price_value' keys
    """
    # Open homepage
    driver.get('https://www.amazon.in/')
    print(f"Opened: https://www.amazon.in/\n")
    time.sleep(2)
    
    # Find and fill search box
    wait = WebDriverWait(driver, wait_timeout)
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
    )
    search_box.clear()
    search_box.send_keys(search_term)
    print(f"Searching for: {search_term}")
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)
    
    # Wait for results to load
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
    )
    print("✓ Search results loaded.\n")
    
    # Extract products
    products = []
    result_elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    
    print(f"Found {len(result_elements)} results. Extracting first {max_products} valid products...\n")
    
    for elem in result_elements:
        if len(products) >= max_products:
            break
        
        try:
            # Get product name
            name_elem = elem.find_element(By.XPATH, ".//span[@data-component-type='s-title']//span")
            product_name = name_elem.text.strip()
            
            # Get price
            price_text = 'N/A'
            try:
                price_elem = elem.find_element(By.XPATH, ".//span[@data-a-price-whole]")
                price_text = price_elem.text.strip()
            except:
                try:
                    price_elem = elem.find_element(By.XPATH, ".//span[contains(@class, 'a-price-whole')]")
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
    parser = argparse.ArgumentParser(description='Search Amazon.in from homepage and find minimum priced product.')
    parser.add_argument('--search-term', type=str, default='iPhone', help='Search term (default: iPhone)')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
    parser.add_argument('--timeout', type=int, default=20, help='Timeout in seconds (default: 20)')
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
        products = search_amazon_homepage(
            driver,
            search_term=args.search_term,
            wait_timeout=args.timeout,
            max_products=args.max_products
        )

        if args.screenshot:
            time.sleep(1)
            driver.save_screenshot(args.screenshot)
            print(f"📸 Screenshot saved: {args.screenshot}\n")

        # Console output
        print("="*80)
        print(f"AMAZON SEARCH RESULTS FOR: {args.search_term.upper()}")
        print("="*80)
        for i, prod in enumerate(products, 1):
            print(f"{i}. {prod['name'][:70]}")
            print(f"   Price: {prod['price']} (₹{prod['price_value']:,.2f})")
        print()

        if products:
            lowest = min(products, key=lambda p: p['price_value'])
            rank = [i for i, p in enumerate(products, 1) if p['price_value'] == lowest['price_value']][0]
            
            print("="*80)
            print(f"🏆 MINIMUM PRICED {args.search_term.upper()}")
            print("="*80)
            print(f"Name:  {lowest['name']}")
            print(f"Price: {lowest['price']}")
            print(f"Value: ₹{lowest['price_value']:,.2f}")
            print(f"Position: #{rank} in results")
            print("="*80)
            
            # Generate HTML and open in browser
            html_file = generate_html_results(products, args.search_term, args.results_html)
            print(f"\n📄 HTML Report: {html_file}")
            
            abs_path = os.path.abspath(html_file)
            file_url = f'file:///{abs_path}'.replace('\\', '/')
            print(f"🌐 Opening results in browser...\n")
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
