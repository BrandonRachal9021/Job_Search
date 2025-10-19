from bs4 import BeautifulSoup
import requests, re

def main():
    print(r"""
 __        __   _
 \ \      / /__| | ___ ___  _ __ ___   ___
  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \
   \ V  V /  __/ | (_| (_) | | | | | |  __/
    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|
                                                    
✨ Welcome to Brandon's Scraper ✨
Let's build something awesome today!
App Purpose:
This Python scraper is designed to collect data automatically from websites,
organize the information, and display or save it in a clean, usable format.
It helps automate repetitive data-gathering tasks for projects or research.
""")
    

def fetch_xula_mission():
    url = "https://www.xula.edu/about/mission-values.html"
    headers = {
        
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try the hinted container first
    container = soup.select_one("div.editorarea")

    text = ""
    if container:
        text = container.get_text(separator=" ", strip=True)

    # Fallback: search the whole document for the key phrase and pull the paragraph
    if not text:
        needle = re.compile(r"founded by Saint", re.I)
        hit = soup.find(string=needle)
        if hit:
            # Prefer the nearest <p> ancestor if present
            p = hit.find_parent("p")
            text = p.get_text(" ", strip=True) if p else hit.strip()

    if not text:
        # Last-chance debug: show what sections we did find to help adjust selectors
        print("⚠️ Could not extract mission text. Debug info:")
        print(" - editorarea found?" , bool(container))
        print(" - Length of page HTML:", len(resp.text))
        return None

    return text

# --- call it (put this where you want output to appear) ---
mission = fetch_xula_mission()
if mission:
    print("\n🎯 XULA Mission Statement:\n")
    print(mission)
else:
    print("⚠️ Could not find mission statement; check selectors or site structure.")





if __name__ == "__main__":
    main()