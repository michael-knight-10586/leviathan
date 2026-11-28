"""Discovery: list every CSV file currently published on football-data.co.uk."""

from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.request import Request, urlopen

DATA_PAGE = "https://www.football-data.co.uk/data.php"
USER_AGENT = "leviathan (github.com/michael-knight-10586/leviathan)"


class _LinkParser(HTMLParser):
    """Collects (href, link text) for every <a> tag on a page."""

    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, "".join(self._text).strip()))
            self._href = None


def _links(page_url):
    """Fetch a page and return its links as (absolute url, link text)."""
    request = Request(page_url, headers={"User-Agent": USER_AGENT})
    html = urlopen(request, timeout=30).read().decode("latin-1")
    parser = _LinkParser()
    parser.feed(html)
    return [(urljoin(page_url, href), text) for href, text in parser.links if href]


def discover():
    """Crawl the site and return (country_pages, files).

    country_pages: sorted list of country page urls found on data.php.
    files: sorted list of (url, source_page) for every CSV linked from them.

    Any page that fails to load stops the run with an error, so a site
    problem can never make files look deleted.
    """
    country_pages = sorted({
        url for url, text in _links(DATA_PAGE)
        if "Football Results" in text and url.lower().endswith(".php")
    })
    found = {}
    for page in country_pages:
        for url, _ in _links(page):
            if url.lower().endswith(".csv"):
                found.setdefault(url, page)
    return country_pages, sorted(found.items())


def compare_pages(previous_pages, current_pages):
    """Return (added, removed) country pages between two runs, each sorted."""
    previous, current = set(previous_pages), set(current_pages)
    return sorted(current - previous), sorted(previous - current)
