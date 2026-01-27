#!/usr/bin/env python3
"""
Automate Amazon.in search for iPhone 16.

Usage:
    python scripts/amazon_iphone_search.py [--headless] [--timeout SECONDS]

This script:
1. Opens https://www.amazon.in/
2. Searches for "iPhone 16"
3. Waits for search results to load
4. Captures product name and price from the first 6 valid products
5. Prints all products and identifies the lowest-priced one
6. Generates and opens an HTML results page in the browser
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
    # Remove currency symbols and commas
    cleaned = price_str.replace('₹', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return float('inf')


def generate_html_results(products, output_file='amazon_results.html'):
    """Generate an HTML page displaying products and the lowest-priced one.
    
    Returns:
        str: Path to the generated HTML file
    """
    if not products:
        html_content = '<html><body><h1>No products found</h1></body></html>'
    else:
        lowest = min(products, key=lambda p: p['price_value'])
        
        products_html = ''.join([
            f'''<tr>
                <td>{i}</td>
                <td>{prod['name'][:70]}</td>
                <td>{prod['price']}</td>
                <td>₹{prod['price_value']:,.2f}</td>
              </tr>'''
            for i, prod in enumerate(products, 1)
        ])
        
        lowest_badge = f'''
            <div style="background-color: #d4edda; padding: 20px; border-radius: 5px; margin-top: 30px; border-left: 5px solid #28a745;">
                <h2 style="color: #155724; margin-top: 0;">✓ LOWEST PRICED PRODUCT</h2>
                <p><strong>Name:</strong> {lowest['name']}</p>
                <p><strong>Price:</strong> {lowest['price']}</p>
                <p><strong>Numeric Price:</strong> ₹{lowest['price_value']:,.2f}</p>
            </div>
        '''
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Amazon iPhone 16 Search Results</title>
    <style>
        * {{ font-family: Arial, sans-serif; }}
        body {{ margin: 20px; background-color: #f5f5f5; }}
        h1 {{ color: #232f3e; border-bottom: 3px solid #FF9900; padding-bottom: 10px; }}
        h2 {{ color: #232f3e; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        th {{
            background-color: #232f3e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f9f9f9;
        }}
        .summary {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .lowest {{
            background-color: #d4edda;
            padding: 20px;
            border-radius: 5px;
            margin-top: 30px;
            border-left: 5px solid #28a745;
        }}
        .lowest h2 {{
            color: #155724;
            margin-top: 0;
        }}
        .lowest p {{
            color: #155724;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <h1>🛍️ Amazon.in iPhone 16 Search Results</h1>
    
    <div class="summary">
        <p><strong>Search Term:</strong> iPhone 16</p>
        <p><strong>Results Captured:</strong> {len(products)} products</p>
        <p><strong>Search Time:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h2>Product List (First {len(products)} Results)</h2>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Product Name</th>
                <th>Price (Displayed)</th>
                <th>Price (Numeric)</th>
            </tr>
        </thead>
        <tbody>
            {products_html}
        </tbody>
    </table>
    
    <div class="lowest">
        <h2>✓ LOWEST PRICED PRODUCT</h2>
        <p><strong>Name:</strong> {lowest['name']}</p>
        <p><strong>Price:</strong> {lowest['price']}</p>
        <p><strong>Numeric Price:</strong> ₹{lowest['price_value']:,.2f}</p>
    </div>
</body>
</html>'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file



def search_amazon_iphone(driver, search_term='iPhone 16', wait_timeout=15, max_products=5):
    """Search Amazon and collect product details.
    
    Returns:
        list: List of dicts with 'name', 'price', 'price_value' keys
    """
    driver.get('https://www.amazon.in/')
    
    # Wait for page to be fully loaded by checking for search box
    wait = WebDriverWait(driver, wait_timeout)
    search_box = wait.until(
        EC.element_to_be_clickable((By.ID, 'twotabsearchtextbox'))
    )
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)
    
    print(f"Searching for '{search_term}'...\n")
    
    # Wait for search results container to load
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
    )
    print("Search results loaded.\n")
    
    # Collect product data from search results
    products = []
    result_elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    
    print(f"Found {len(result_elements)} result elements. Extracting first {max_products} valid products...\n")
    
    for elem in result_elements:
        if len(products) >= max_products:
            break
        
        try:
            # Try to get product name
            name_elem = elem.find_element(By.XPATH, ".//span[@data-component-type='s-title']//span")
            product_name = name_elem.text.strip()
            
            # Try to get price
            price_elem = None
            try:
                price_elem = elem.find_element(By.XPATH, ".//span[@data-a-price-whole]")
                price_text = price_elem.text.strip()
            except:
                # Fallback: try alternate price locator
                try:
                    price_elem = elem.find_element(By.XPATH, ".//span[contains(@class, 'a-price-whole')]")
                    price_text = price_elem.text.strip()
                except:
                    price_text = 'N/A'
            
            if product_name and price_text != 'N/A':
                price_value = parse_price(price_text)
                products.append({
                    'name': product_name,
                    'price': price_text,
                    'price_value': price_value
                })
                print(f"✓ Product {len(products)}: {product_name[:60]}... | Price: {price_text}")
        except Exception as e:
            # Skip products that fail to parse
            continue
    
    return products


def main():
    parser = argparse.ArgumentParser(description='Search Amazon.in for iPhone 16 and find the cheapest.')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout in seconds for element waits (default: 10)')
    parser.add_argument('--search', type=str, default='iPhone 16', help='Search term (default: iPhone 16)')
    parser.add_argument('--max-products', type=int, default=6, help='Max products to capture (default: 6)')
    parser.add_argument('--screenshot', type=str, default=None, help='Save screenshot after search')
    parser.add_argument('--results-html', type=str, default='amazon_results.html', help='Output HTML file with results')
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
        products = search_amazon_iphone(
            driver,
            search_term=args.search,
            wait_timeout=args.timeout,
            max_products=args.max_products
        )

        if args.screenshot:
            driver.save_screenshot(args.screenshot)
            print(f"\n📸 Screenshot saved: {args.screenshot}")

        # Print summary to console
        print("\n" + "="*80)
        print("CAPTURED PRODUCTS")
        print("="*80)
        for i, prod in enumerate(products, 1):
            print(f"{i}. {prod['name'][:70]}")
            print(f"   Price: {prod['price']}")
            print()

        if products:
            lowest = min(products, key=lambda p: p['price_value'])
            print("="*80)
            print("LOWEST PRICED PRODUCT")
            print("="*80)
            print(f"Name:  {lowest['name']}")
            print(f"Price: {lowest['price']}")
            print("="*80)
            
            # Generate HTML results page
            html_file = generate_html_results(products, args.results_html)
            print(f"\n📄 Results HTML generated: {html_file}")
            
            # Open the HTML file in the browser
            abs_path = os.path.abspath(html_file)
            file_url = f'file:///{abs_path}'.replace('\\', '/')
            print(f"🌐 Opening results in browser: {file_url}\n")
            driver.get(file_url)
            
            if not args.headless:
                try:
                    input('Press Enter to close the browser and exit...')
                except KeyboardInterrupt:
                    pass
        else:
            print("⚠ No valid products captured.")

    except Exception as e:
        print(f"❌ Error: {e}")
        if not args.headless:
            try:
                input('\nPress Enter to close the browser and exit...')
            except KeyboardInterrupt:
                pass
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
