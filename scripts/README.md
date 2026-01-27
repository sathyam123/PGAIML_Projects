Scripts to automate opening websites and scraping product data in Chrome

Files:
- `open_syzygy_chrome.ps1` - PowerShell script to open the URL in Google Chrome (Windows).
- `open_syzygy_chrome.py` - Python Selenium script that opens https://www.syzygyai.in/ and optionally clicks the Research link.
- `amazon_iphone_search.py` - Python Selenium script to search Amazon.in for iPhone 16, capture product details, and identify the lowest-priced item.
- `requirements.txt` - Python dependencies for Selenium scripts.

## PowerShell Usage (Windows PowerShell)

Open https://www.syzygyai.in/ normally:

```powershell
.\scripts\open_syzygy_chrome.ps1
```

Open in incognito mode:

```powershell
.\scripts\open_syzygy_chrome.ps1 -Incognito
```

Open in a new window:

```powershell
.\scripts\open_syzygy_chrome.ps1 -NewWindow
```

## Python Selenium Usage

### Setup (one-time)

1. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r scripts\requirements.txt
```

### Syzygy AI Automation

Open the page and click Research link (visible browser):

```powershell
python scripts\open_syzygy_chrome.py --click-research
```

Run headless with screenshot:

```powershell
python scripts\open_syzygy_chrome.py --headless --click-research --screenshot syzygy.png
```

### Amazon iPhone 16 Search

Search visible browser (shows first 5 products):

```powershell
python scripts\amazon_iphone_search.py
```

Search headless with screenshot:

```powershell
python scripts\amazon_iphone_search.py --headless --screenshot amazon_results.png
```

Search for different product (default: iPhone 16):

```powershell
python scripts\amazon_iphone_search.py --search "iPhone 15"
```

Capture more products (default: 5):

```powershell
python scripts\amazon_iphone_search.py --max-products 10
```

Combine options:

```powershell
python scripts\amazon_iphone_search.py --headless --search "iPhone 16" --max-products 10 --screenshot amazon.png
```

## VS Code Launch Configurations

Open the workspace: `File → Open Workspace from File...` → `PGAIML_Projects.code-workspace`

Press `F5` to run:
- **Python: Open Syzygy (Visible)** - Opens Syzygy and clicks Research link
- **Python: Open Syzygy (Headless)** - Runs headless with screenshot
- **Python: Amazon iPhone Search (Visible)** - Amazon search with visible browser
- **Python: Amazon iPhone Search (Headless + Screenshot)** - Amazon search headless with screenshot
- **PowerShell: Open Syzygy** - PowerShell Syzygy launch

## Script Output

Both scripts print:
- Status messages as they run
- All captured products with names and prices
- The lowest-priced product (Amazon script)
- Optional screenshot path if `--screenshot` is provided

## Notes

- `webdriver-manager` automatically downloads a ChromeDriver matching your Chrome browser version
- On corporate networks with restricted internet, you may need to install ChromeDriver manually
- Amazon blocks some bot traffic; if you encounter 403 errors, try adding delays or running via a proxy
- Scripts wait up to 15 seconds for elements to load (configurable with `--timeout`)

