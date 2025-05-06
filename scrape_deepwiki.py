import os
import re
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse, parse_qs

# Base URL and initial page
BASE_URL = "https://deepwiki.com/shaadclt/LLM-Driven-Marketing-Assistant"
OUTPUT_DIR = "docs"

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Keep track of visited pages to avoid duplicates
visited_pages = set()

# Sections from the sidebar menu
sections = [
    "Overview",
    "System Architecture",
    "Installation and Setup",
    "Core Functionality",
    "LLM Integration",
    "Prompt Engineering",
    "Age-Based Content Generation",
    "User Interface",
    "User Input Components", 
    "Output Display",
    "Development Guide",
    "Adding New Examples",
    "Dependencies and External Libraries"
]

def clean_filename(name):
    """Convert a section name to a valid filename."""
    return re.sub(r'[^\w\-]', '_', name).lower()

def get_section_url(section_name):
    """Get the URL for a section, handling anchor links correctly."""
    section_slug = clean_filename(section_name)
    return f"{BASE_URL}#{section_slug}"

def extract_content(soup, section_name=None):
    """Extract the main content from the page based on DeepWiki's structure."""
    # Try to find the main content container
    main_content = None
    
    # Try to find the content by the section's id if a section name is provided
    if section_name:
        section_id = clean_filename(section_name)
        main_content = soup.find(id=section_id) or soup.find(id=f"section-{section_id}")
    
    # If we couldn't find the section directly, try different methods
    if not main_content:
        # Look for the main article container
        main_content = soup.find('article') or soup.find('div', {'class': 'article'})
        
        # Look for the main content div
        if not main_content:
            main_content = soup.find('div', {'class': re.compile('.*content.*')})
        
        # Try to get markdown content
        if not main_content:
            main_content = soup.find('div', {'class': re.compile('.*markdown.*')})
        
        # If still not found, get the body and extract relevant content
        if not main_content:
            # Look for headers and paragraphs as a fallback
            headers_and_content = soup.find_all(['h1', 'h2', 'h3', 'p', 'pre', 'table', 'ul', 'ol', 'div'])
            if headers_and_content:
                # Filter out navigation and other irrelevant elements
                relevant_elements = [
                    el for el in headers_and_content 
                    if not any(cls in str(el.get('class', '')) for cls in ['nav', 'menu', 'sidebar', 'footer', 'header'])
                ]
                if relevant_elements:
                    # Combine them to form our content
                    content_html = ''.join(str(el) for el in relevant_elements)
                    return content_html
    
    return str(main_content) if main_content else ""

def extract_table_of_contents(soup):
    """Extract the table of contents or navigation from the page."""
    # Look for navigation elements
    nav = soup.find('nav') or soup.find('div', {'class': re.compile('.*nav.*|.*menu.*|.*sidebar.*')})
    if nav:
        links = nav.find_all('a')
        toc_items = []
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            if text and href:
                toc_items.append((text, href))
        return toc_items
    return []

def html_to_markdown(html_content):
    """Convert HTML content to Markdown format with improved handling."""
    md_content = html_content
    
    # Replace heading tags
    md_content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', md_content)
    md_content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', md_content)
    md_content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', md_content)
    md_content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n', md_content)
    md_content = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1\n\n', md_content)
    md_content = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1\n\n', md_content)
    
    # Replace paragraph tags
    md_content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', md_content, flags=re.DOTALL)
    
    # Replace links (removing hash tags for internal links)
    def process_link(match):
        url = match.group(1)
        text = match.group(2)
        
        # Handle internal links 
        if url.startswith('#'):
            link_section = url[1:]  # Remove the hash
            return f"[{text}](#{link_section})"
        elif not url.startswith(('http://', 'https://')):
            # Relative links
            return f"[{text}]({url})"
        else:
            # External links
            return f"[{text}]({url})"
    
    md_content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', process_link, md_content)
    
    # Replace lists
    md_content = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\1\n', md_content, flags=re.DOTALL)
    md_content = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\1\n', md_content, flags=re.DOTALL)
    md_content = re.sub(r'<li[^>]*>(.*?)</li>', r'* \1\n', md_content, flags=re.DOTALL)
    
    # Replace code blocks
    md_content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```\n\n', md_content, flags=re.DOTALL)
    md_content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', md_content)
    
    # Replace tables
    def process_table(match):
        table_html = match.group(0)
        soup = BeautifulSoup(table_html, 'html.parser')
        
        # Process header row
        header_row = soup.find('thead')
        if header_row:
            headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
        else:
            first_row = soup.find('tr')
            if first_row:
                headers = [th.get_text().strip() for th in first_row.find_all(['th', 'td'])]
            else:
                headers = []
        
        # Start building the markdown table
        md_table = ""
        if headers:
            md_table += "| " + " | ".join(headers) + " |\n"
            md_table += "| " + " | ".join(["---" for _ in headers]) + " |\n"
        
        # Process body rows
        body_rows = soup.find('tbody').find_all('tr') if soup.find('tbody') else soup.find_all('tr')
        for i, row in enumerate(body_rows):
            # Skip the first row if it's the header and we've already processed headers
            if i == 0 and headers and not soup.find('thead'):
                continue
            
            cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
            if cells:
                md_table += "| " + " | ".join(cells) + " |\n"
        
        return md_table + "\n"
    
    # Replace table tags
    md_content = re.sub(r'<table[^>]*>.*?</table>', process_table, md_content, flags=re.DOTALL)
    
    # Replace divs with newlines
    md_content = re.sub(r'<div[^>]*>(.*?)</div>', r'\1\n', md_content, flags=re.DOTALL)
    
    # Replace line breaks
    md_content = re.sub(r'<br[^>]*>', '\n', md_content)
    
    # Replace bold and italic
    md_content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', md_content)
    md_content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', md_content)
    md_content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', md_content)
    md_content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', md_content)
    
    # Remove remaining HTML tags
    md_content = re.sub(r'<[^>]+>', '', md_content)
    
    # Clean up excessive newlines and spaces
    md_content = re.sub(r'\n{3,}', '\n\n', md_content)
    md_content = re.sub(r' {2,}', ' ', md_content)
    
    # Unescape HTML entities
    md_content = md_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    md_content = md_content.replace('&quot;', '"').replace('&apos;', "'")
    
    return md_content

def scrape_section(section):
    """Scrape a specific section and save it as Markdown."""
    section_url = get_section_url(section)
    if section_url in visited_pages:
        return
    
    visited_pages.add(section_url)
    
    print(f"Scraping {section} from {section_url}...")
    
    try:
        response = requests.get(section_url)
        if response.status_code != 200:
            print(f"Failed to fetch {section_url}, status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content = extract_content(soup, section)
        
        if not content:
            print(f"No content found for {section}")
            return
        
        markdown = html_to_markdown(content)
        
        # Create directories if needed
        section_dir = os.path.dirname(os.path.join(OUTPUT_DIR, f"{clean_filename(section)}.md"))
        if not os.path.exists(section_dir):
            os.makedirs(section_dir)
        
        # Save the markdown content
        filename = os.path.join(OUTPUT_DIR, f"{clean_filename(section)}.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {section}\n\n")
            f.write(markdown)
        
        print(f"Saved {filename}")
        
        # Respect the website by adding a small delay between requests
        time.sleep(1.5)
    
    except Exception as e:
        print(f"Error scraping {section_url}: {str(e)}")

def scrape_main_page():
    """Scrape the main page to extract structure and content."""
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print(f"Failed to fetch {BASE_URL}, status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract main content
        content = extract_content(soup)
        
        # Extract the table of contents for additional sections
        toc = extract_table_of_contents(soup)
        
        if content:
            markdown = html_to_markdown(content)
            
            # Create README file with table of contents
            with open(os.path.join(OUTPUT_DIR, "README.md"), 'w', encoding='utf-8') as f:
                f.write("# LLM-Driven Marketing Assistant Documentation\n\n")
                f.write("## Table of Contents\n\n")
                for section in sections:
                    f.write(f"* [{section}]({clean_filename(section)}.md)\n")
                f.write("\n")
            
            # Save the main page
            with open(os.path.join(OUTPUT_DIR, "index.md"), 'w', encoding='utf-8') as f:
                f.write("# LLM-Driven Marketing Assistant\n\n")
                f.write(markdown)
            
            print("Saved main page to index.md")
            print("Saved table of contents to README.md")
        else:
            print("No content found on the main page")
        
        # Add any additional sections found in the table of contents
        for title, href in toc:
            if title not in sections:
                sections.append(title)
    
    except Exception as e:
        print(f"Error scraping main page: {str(e)}")

def main():
    # Create output directory structure
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Scrape the main page first
    scrape_main_page()
    
    # Scrape each section
    for section in sections:
        scrape_section(section)
    
    print("Scraping completed!")

if __name__ == "__main__":
    main() 