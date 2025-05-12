import requests
import pandas as pd
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_top_imdb_matches(title, year=None, max_results=5, verbose=True):
    """
    Searches IMDb for the given movie/TV show title (and year if provided).
    Returns a list of tuples: (displayed title text, IMDb ID), ranked by order of appearance.
    """
    if not isinstance(title, str) or not title.strip():
        return []

    query = title.strip()
    if year and not pd.isna(year):
        try:
            query += f" {int(year)}"
        except ValueError:
            pass  # ignore invalid year format
    
    if verbose:
        print(f"Searching for: '{query}'")
    
    # Use the updated search URL format
    search_url = f"https://www.imdb.com/find/?q={query.replace(' ', '+')}&s=tt&exact=true&ref_=fn_tt_ex"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if verbose:
            print(f"Request status: {response.status_code}")
    except Exception as e:
        if verbose:
            print(f"Error fetching IMDb page for '{query}':", e)
        return []

    if response.status_code != 200:
        if verbose:
            print(f"IMDb search failed for '{query}' with status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Updated selector for IMDb's current structure
    # Try multiple possible selectors as IMDb might have different layouts
    results = []
    
    # First try the new search results layout
    search_results = soup.select('li.ipc-metadata-list-summary-item')
    
    if search_results:
        for result in search_results[:max_results]:
            link = result.select_one('a.ipc-metadata-list-summary-item__t')
            if link:
                href = link.get('href', '')
                if '/title/' in href:
                    imdb_id = href.split('/')[2]
                    title_text = link.get_text(strip=True)
                    
                    # Get additional info like year and type if available
                    year_elem = result.select_one('.ipc-metadata-list-summary-item__tl')
                    if year_elem:
                        title_text += f" {year_elem.get_text(strip=True)}"
                    
                    results.append((title_text, imdb_id))
    
    # If no results found with new layout, try alternative selectors
    if not results:
        # Try another common IMDb results pattern
        search_results = soup.select('.findResult')
        for result in search_results[:max_results]:
            link = result.select_one('a')
            if link and '/title/' in link.get('href', ''):
                imdb_id = link.get('href').split('/')[2]
                title_text = result.get_text(strip=True)
                results.append((title_text, imdb_id))
    
    # If still no results, try an even more generic approach
    if not results:
        all_links = soup.select('a[href*="/title/tt"]')
        for link in all_links[:max_results]:
            href = link.get('href', '')
            if '/title/' in href:
                imdb_id = href.split('/')[2]
                title_text = link.get_text(strip=True)
                if title_text:  # Ensure we're not getting empty text
                    results.append((title_text, imdb_id))
    
    if verbose:
        print(f"Found {len(results)} results")
        for r in results:
            print(f"  - {r[0]} ({r[1]})")

    # Sort matches by fuzzy similarity if more than one result
    if len(results) > 1:
        results = sorted(results, key=lambda x: similar(title, x[0]), reverse=True)

    return results