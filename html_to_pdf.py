# #!/usr/bin/env python3
# """
# HTML to PDF Converter Script (Browser-based)
# Converts HTML files to PDF using Playwright for accurate rendering
# """

# import sys
# import os
# from pathlib import Path

# try:
#     from playwright.sync_api import sync_playwright
# except ImportError:
#     print("Error: playwright library not found.")
#     print("Please install it using:")
#     print("  pip install playwright")
#     print("  playwright install chromium")
#     sys.exit(1)


# def convert_html_to_pdf(html_file, pdf_file=None, landscape=False, wait_time=2000, full_page=False):
#     """
#     Convert an HTML file to PDF using a headless browser.
    
#     Args:
#         html_file (str): Path to the input HTML file
#         pdf_file (str, optional): Path to the output PDF file
#         landscape (bool): Whether to use landscape orientation
#         wait_time (int): Time in ms to wait for page load (for animations/fonts)
#         full_page (bool): Capture entire scrollable page as single PDF page
    
#     Returns:
#         str: Path to the generated PDF file
#     """
#     # Validate input file
#     if not os.path.exists(html_file):
#         raise FileNotFoundError(f"HTML file not found: {html_file}")
    
#     # Determine output file name
#     if pdf_file is None:
#         pdf_file = Path(html_file).with_suffix('.pdf')
    
#     # Get absolute path for the HTML file
#     html_path = Path(html_file).resolve()
#     html_url = f"file://{html_path}"
    
#     print(f"Converting {html_file} to PDF...")
#     print(f"Loading page and waiting {wait_time}ms for resources...")
    
#     with sync_playwright() as p:
#         # Launch browser
#         browser = p.chromium.launch(headless=True)
        
#         if full_page:
#             # For full page, set a consistent viewport width (typical desktop)
#             page = browser.new_page(viewport={'width': 1440, 'height': 900})
#         else:
#             page = browser.new_page()
        
#         # Navigate to HTML file
#         page.goto(html_url, wait_until="networkidle")
        
#         # Wait for additional resources (fonts, animations to initialize)
#         page.wait_for_timeout(wait_time)
        
#         # Get page dimensions if full_page is enabled
#         pdf_options = {
#             'path': pdf_file,
#             'print_background': True,
#             'scale': 1.0
#         }
        
#         if full_page:
#             # Scroll to bottom to trigger lazy-loading content
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             page.wait_for_timeout(500)
            
#             # Get full page dimensions
#             dimensions = page.evaluate("""() => {
#                 return {
#                     width: Math.max(
#                         document.body.scrollWidth,
#                         document.documentElement.scrollWidth,
#                         document.body.offsetWidth,
#                         document.documentElement.offsetWidth,
#                         document.documentElement.clientWidth
#                     ),
#                     height: Math.max(
#                         document.body.scrollHeight,
#                         document.documentElement.scrollHeight,
#                         document.body.offsetHeight,
#                         document.documentElement.offsetHeight
#                     )
#                 };
#             }""")
            
#             page_width = dimensions['width']
#             page_height = dimensions['height']
            
#             pdf_options.update({
#                 'width': f'{page_width}px',
#                 'height': f'{page_height}px',
#                 'margin': {'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
#                 'page_ranges': '1'  # Only first page (which contains everything)
#             })
#             print(f"Full page dimensions: {page_width}px x {page_height}px")
#         else:
#             pdf_options.update({
#                 'format': 'A4',
#                 'landscape': landscape,
#                 'margin': {'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'},
#                 'prefer_css_page_size': True
#             })
        
#         # Generate PDF
#         page.pdf(**pdf_options)
        
#         browser.close()
    
#     print(f"✓ Successfully created: {pdf_file}")
#     return pdf_file


# def convert_html_to_pdf_custom_size(html_file, pdf_file=None, width="1920px", height="1080px", wait_time=2000):
#     """
#     Convert HTML to PDF with custom dimensions (useful for preserving aspect ratios).
    
#     Args:
#         html_file (str): Path to the input HTML file
#         pdf_file (str): Path to the output PDF file
#         width (str): Page width (e.g., "1920px", "16in")
#         height (str): Page height (e.g., "1080px", "9in")
#         wait_time (int): Time to wait for page load
#     """
#     if not os.path.exists(html_file):
#         raise FileNotFoundError(f"HTML file not found: {html_file}")
    
#     if pdf_file is None:
#         pdf_file = Path(html_file).with_suffix('.pdf')
    
#     html_path = Path(html_file).resolve()
#     html_url = f"file://{html_path}"
    
#     print(f"Converting {html_file} to PDF with custom size ({width} x {height})...")
    
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(html_url, wait_until="networkidle")
#         page.wait_for_timeout(wait_time)
        
#         page.pdf(
#             path=pdf_file,
#             width=width,
#             height=height,
#             print_background=True,
#             margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
#             scale=1.0
#         )
        
#         browser.close()
    
#     print(f"✓ Successfully created: {pdf_file}")
#     return pdf_file


# def main():
#     """Main function to handle command-line arguments"""
#     if len(sys.argv) < 2:
#         print("Usage: python html_to_pdf.py <input.html> [output.pdf] [options]")
#         print("\nOptions:")
#         print("  --landscape         Use landscape orientation")
#         print("  --full-page         Capture entire scrollable page as single PDF page")
#         print("  --custom WxH        Custom size (e.g., --custom 1920px,1080px)")
#         print("  --wait TIME         Wait time in milliseconds (default: 2000)")
#         print("\nExamples:")
#         print("  python html_to_pdf.py myfile.html")
#         print("  python html_to_pdf.py myfile.html output.pdf")
#         print("  python html_to_pdf.py myfile.html --full-page")
#         print("  python html_to_pdf.py code.html output.pdf --custom 1920px,1080px")
#         sys.exit(1)
    
#     html_file = sys.argv[1]
#     pdf_file = None
#     landscape = False
#     full_page = False
#     custom_size = None
#     wait_time = 2000
    
#     # Parse arguments
#     i = 2
#     while i < len(sys.argv):
#         arg = sys.argv[i]
#         if arg == '--landscape':
#             landscape = True
#         elif arg == '--full-page':
#             full_page = True
#         elif arg == '--custom' and i + 1 < len(sys.argv):
#             custom_size = sys.argv[i + 1].split(',')
#             i += 1
#         elif arg == '--wait' and i + 1 < len(sys.argv):
#             wait_time = int(sys.argv[i + 1])
#             i += 1
#         elif not arg.startswith('--') and pdf_file is None:
#             pdf_file = arg
#         i += 1
    
#     try:
#         if custom_size:
#             width, height = custom_size[0].strip(), custom_size[1].strip()
#             convert_html_to_pdf_custom_size(html_file, pdf_file, width, height, wait_time)
#         else:
#             convert_html_to_pdf(html_file, pdf_file, landscape, wait_time, full_page)
#     except Exception as e:
#         print(f"Error: {e}")
#         sys.exit(1)


# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
"""
HTML to PDF Converter Script (Browser-based)
Converts HTML files to PDF using Playwright for accurate rendering
"""

import sys
import os
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright library not found.")
    print("Please install it using:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)


def convert_html_to_pdf(html_file, pdf_file=None, landscape=False, wait_time=2000, full_page=False, viewport_width=1440):
    """
    Convert an HTML file to PDF using a headless browser.
    
    Args:
        html_file (str): Path to the input HTML file
        pdf_file (str, optional): Path to the output PDF file
        landscape (bool): Whether to use landscape orientation
        wait_time (int): Time in ms to wait for page load (for animations/fonts)
        full_page (bool): Capture entire scrollable page as single PDF page
        viewport_width (int): Viewport width for rendering (default: 1440)
    
    Returns:
        str: Path to the generated PDF file
    """
    # Validate input file
    if not os.path.exists(html_file):
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    
    # Determine output file name
    if pdf_file is None:
        pdf_file = Path(html_file).with_suffix('.pdf')
    
    # Get absolute path for the HTML file
    html_path = Path(html_file).resolve()
    html_url = f"file://{html_path}"
    
    print(f"Converting {html_file} to PDF...")
    print(f"Loading page and waiting {wait_time}ms for resources...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        
        if full_page:
            # For full page, set a consistent viewport width (typical desktop)
            page = browser.new_page(viewport={'width': viewport_width, 'height': 900})
        else:
            page = browser.new_page()
        
        # Navigate to HTML file
        page.goto(html_url, wait_until="networkidle")
        
        # Wait for additional resources (fonts, animations to initialize)
        page.wait_for_timeout(wait_time)
        
        # Get page dimensions if full_page is enabled
        pdf_options = {
            'path': pdf_file,
            'print_background': True,
            'scale': 1.0
        }
        
        if full_page:
            # Scroll to bottom to trigger lazy-loading content
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            
            # Get full page dimensions
            dimensions = page.evaluate("""() => {
                return {
                    width: Math.max(
                        document.body.scrollWidth,
                        document.documentElement.scrollWidth,
                        document.body.offsetWidth,
                        document.documentElement.offsetWidth,
                        document.documentElement.clientWidth
                    ),
                    height: Math.max(
                        document.body.scrollHeight,
                        document.documentElement.scrollHeight,
                        document.body.offsetHeight,
                        document.documentElement.offsetHeight
                    )
                };
            }""")
            
            page_width = dimensions['width']
            page_height = dimensions['height']
            
            pdf_options.update({
                'width': f'{page_width}px',
                'height': f'{page_height}px',
                'margin': {'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
                'page_ranges': '1'  # Only first page (which contains everything)
            })
            print(f"Full page dimensions: {page_width}px x {page_height}px")
        else:
            pdf_options.update({
                'format': 'A4',
                'landscape': landscape,
                'margin': {'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'},
                'prefer_css_page_size': True
            })
        
        # Generate PDF
        page.pdf(**pdf_options)
        
        browser.close()
    
    print(f"✓ Successfully created: {pdf_file}")
    return pdf_file


def convert_html_to_pdf_custom_size(html_file, pdf_file=None, width="1920px", height="1080px", wait_time=2000):
    """
    Convert HTML to PDF with custom dimensions (useful for preserving aspect ratios).
    
    Args:
        html_file (str): Path to the input HTML file
        pdf_file (str): Path to the output PDF file
        width (str): Page width (e.g., "1920px", "16in")
        height (str): Page height (e.g., "1080px", "9in")
        wait_time (int): Time to wait for page load
    """
    if not os.path.exists(html_file):
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    
    if pdf_file is None:
        pdf_file = Path(html_file).with_suffix('.pdf')
    
    html_path = Path(html_file).resolve()
    html_url = f"file://{html_path}"
    
    print(f"Converting {html_file} to PDF with custom size ({width} x {height})...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(html_url, wait_until="networkidle")
        page.wait_for_timeout(wait_time)
        
        page.pdf(
            path=pdf_file,
            width=width,
            height=height,
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
            scale=1.0
        )
        
        browser.close()
    
    print(f"✓ Successfully created: {pdf_file}")
    return pdf_file


def main():
    """Main function to handle command-line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python html_to_pdf.py <input.html> [output.pdf] [options]")
        print("\nOptions:")
        print("  --landscape         Use landscape orientation")
        print("  --full-page         Capture entire scrollable page as single PDF page")
        print("  --width WIDTH       Viewport width for full-page (default: 1440)")
        print("  --custom WxH        Custom size (e.g., --custom 1920px,1080px)")
        print("  --wait TIME         Wait time in milliseconds (default: 2000)")
        print("\nExamples:")
        print("  python html_to_pdf.py myfile.html")
        print("  python html_to_pdf.py myfile.html output.pdf")
        print("  python html_to_pdf.py myfile.html --full-page")
        print("  python html_to_pdf.py myfile.html --full-page --width 1920")
        print("  python html_to_pdf.py code.html output.pdf --custom 1920px,1080px")
        sys.exit(1)
    
    html_file = sys.argv[1]
    pdf_file = None
    landscape = False
    full_page = False
    viewport_width = 1440
    custom_size = None
    wait_time = 2000
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--landscape':
            landscape = True
        elif arg == '--full-page':
            full_page = True
        elif arg == '--width' and i + 1 < len(sys.argv):
            viewport_width = int(sys.argv[i + 1])
            i += 1
        elif arg == '--custom' and i + 1 < len(sys.argv):
            custom_size = sys.argv[i + 1].split(',')
            i += 1
        elif arg == '--wait' and i + 1 < len(sys.argv):
            wait_time = int(sys.argv[i + 1])
            i += 1
        elif not arg.startswith('--') and pdf_file is None:
            pdf_file = arg
        i += 1
    
    try:
        if custom_size:
            width, height = custom_size[0].strip(), custom_size[1].strip()
            convert_html_to_pdf_custom_size(html_file, pdf_file, width, height, wait_time)
        else:
            convert_html_to_pdf(html_file, pdf_file, landscape, wait_time, full_page, viewport_width)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()