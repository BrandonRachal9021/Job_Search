# --- imports (top) ---
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import re
from typing import Optional
from bs4 import BeautifulSoup
import requests

# --- banner ---
def print_banner():
    print(r"""
 __        __   _                            _         
 \ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___   
  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  
   \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | 
    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  
                                                       
   ✨ Welcome to Brandon's Scraper ✨
    Let's build something awesome today!
""", flush=True)

# --- XULA scraper ---
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

    # Try hinted container
    mission_div = soup.find("div", class_="editorarea")
    text = mission_div.get_text(" ", strip=True) if mission_div else ""

    # Fallback: look for the key phrase anywhere
    if not text:
        hit = soup.find(string=re.compile(r"founded by Saint", re.I))
        if hit:
            p = hit.find_parent("p")
            text = p.get_text(" ", strip=True) if p else hit.strip()

    if text:
        print("\n🎯 XULA Mission Statement:\n")
        print(text)
    else:
        print("⚠️ XULA mission not found. Site structure may have changed.")

# --- Dillard scraper ---
def fetch_dillard_mission():
    url = "https://www.dillard.edu/about/history-traditions/our-mission/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=25)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find a heading with "mission" then gather following paragraphs
    heading = None
    for tag in soup.find_all(re.compile(r"^h[1-4]$")):
        if "mission" in tag.get_text(" ", strip=True).lower():
            heading = tag
            break

def fetch_tulane_mission():
    url = "https://tulane.edu/about/leadership-and-administration/mission-statement"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print("⚠️ Could not fetch Tulane page:", e)
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try a heading with "mission" → grab the next paragraph(s)
    for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        if "mission" in tag.get_text(" ", strip=True).lower():
            p = tag.find_next("p")
            if p:
                print("\n🎯 Tulane University Mission Statement:\n")
                print(p.get_text(" ", strip=True))
                return

    # Fallback: first paragraph that mentions "mission"
    for p in soup.find_all("p"):
        txt = p.get_text(" ", strip=True)
        if "mission" in txt.lower() and len(txt) > 50:
            print("\n🎯 Tulane University Mission Statement:\n")
            print(txt)
            return

    print("⚠️ Tulane mission not found on the page.")


    def collect_after_heading(h, max_chars=2000):
        chunks, node = [], h.find_next_sibling()
        stop = {"h1","h2","h3","h4","section","hr","nav","footer"}
        while node and node.name not in stop:
            if node.name == "p":
                t = node.get_text(" ", strip=True)
                if t: chunks.append(t)
                if sum(len(x) for x in chunks) > max_chars:
                    break
            node = node.find_next_sibling()
        return " ".join(chunks).strip()

    text = collect_after_heading(heading) if heading else ""

    if not text:
        # Fallback: any reasonable paragraph mentioning mission/purpose/vision
        for p in soup.find_all("p"):
            t = p.get_text(" ", strip=True)
            low = t.lower()
            if any(k in low for k in ("mission","purpose","vision")) and len(t) > 60:
                text = t
                break

    if text:
        print("\n🎯 Dillard University Mission Statement:\n")
        print(text)
    else:
        print("⚠️ Dillard mission not found. Try inspecting the page and adjust logic.")

# --- run both (nothing overwritten) ---
def main():
    print_banner()
    print("\n🧠 App Purpose:\nThis Python scraper is designed to collect data automatically from websites,organize the information, and display or save it in a clean, usable format.It helps automate repetitive data-gathering tasks for projects or research.\n")
    fetch_xula_mission()
    fetch_dillard_mission()
    fetch_tulane_mission()

if __name__ == "__main__":
    main()
