import requests
from bs4 import BeautifulSoup

def fetch_web_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (ChatAgentMiniBrowser)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as ex:
        return f"<error>{str(ex)}</error>"

def parse_web_answer(html, html_render=False):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # Get readable text
        main_text = ' '.join(soup.stripped_strings)[:5000]
        if html_render:
            # Return prettified, scriptless HTML for preview panel
            for script in soup(['script', 'style']):
                script.decompose()
            return soup.prettify()[:7000]
        return main_text
    except Exception as ex:
        return f"(Web parse error: {ex})"
