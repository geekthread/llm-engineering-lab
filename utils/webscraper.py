import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_webpage_text(url: str) -> str:
    """Fetch webpage and return clean text."""
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)

def get_website_links(url, headers=None, timeout=10):
    """
    Return cleaned, absolute links found on a webpage.

    Args:
        url (str): Website URL to scrape.
        headers (dict, optional): Request headers.
        timeout (int): Request timeout in seconds.

    Returns:
        list[str]: Unique, valid absolute URLs.
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()

        # Skip empty, anchors, JS, mail links
        if href.startswith(("#", "javascript:", "mailto:")):
            continue

        # Convert relative URLs to absolute
        absolute_url = urljoin(url, href)

        # Keep only HTTP/HTTPS links
        parsed = urlparse(absolute_url)
        if parsed.scheme in ("http", "https"):
            links.add(absolute_url)

    return sorted(links)
