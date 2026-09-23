import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SEASON = 51
BASE_URL = "https://survivor.fandom.com"
API_URL = f"{BASE_URL}/api.php"

TRIBES_BY_COLOR = {
    "3bb1db": "Kele",
    "ffda45": "Hina",
    "ff5d51": "Uli",
    "feb635": "Civa",
    "d05dbd": "Lagi",
    "a7f084": "Vula",
    "fcdd31": "Gata",
    "ff4148": "Lavo",
    "049ed9": "Tuku",
}


def get_tribe_from_color(color):
    return TRIBES_BY_COLOR.get(color, "Unknown")


def get_castaways():
    response = requests.get(
        API_URL,
        params={
            "action": "parse",
            "page": f"Survivor_{SEASON}",
            "prop": "text",
            "format": "json",
        },
        headers={"User-Agent": "survivor-list-maker/1.0"},
        timeout=30,
    )
    response.raise_for_status()
    html = response.json()["parse"]["text"]["*"]
    soup = BeautifulSoup(html, "html.parser")

    castaways = []
    for row in soup.find_all("tr"):
        info_cell = row.find("td", align="left")
        link = info_cell.find("a", title=True) if info_cell else None
        small = info_cell.find("small") if info_cell else None
        if not link or not small:
            continue

        info = list(small.stripped_strings)
        if len(info) < 2:
            continue
        age, residence, state = [part.strip() for part in info[0].split(",", 2)]
        image_cell = row.find("td")
        image = image_cell.find("img") if image_cell else None
        image_url = (image.get("data-src") or image.get("src")) if image else ""
        image_url = image_url.split("/revision")[0]
        style = image_cell.get("style", "") if image_cell else ""
        color_match = re.search(r"background:\s*#([0-9a-fA-F]{6})", style)
        tribe_color = color_match.group(1).lower() if color_match else ""

        castaways.append(
            {
                "tribeColor": tribe_color,
                "tribe": get_tribe_from_color(tribe_color),
                "iconURL": image_url,
                "name": link["title"],
                "age": age,
                "currentResidence": f"{residence}, {state}",
                "occupation": " ".join(info[1:]),
                "pageURL": f"{BASE_URL}{link['href']}",
                "id": len(castaways) + 1,
            }
        )

    if not castaways:
        raise RuntimeError("No castaways found in the Survivor page response")
    return castaways


output_path = Path(__file__).with_name(f"season_{SEASON}_castaways.json")
with output_path.open("w", encoding="utf-8") as outfile:
    json.dump(get_castaways(), outfile, indent=4)
