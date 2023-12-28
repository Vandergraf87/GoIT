import requests
from bs4 import BeautifulSoup
import json

base_url = "http://quotes.toscrape.com"
quotes_url = "/page/1/"

quotes_data = []
authors_data = {}

def get_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get author info
    author_info = {
        "fullname": soup.select_one(".author-title").get_text(strip=True),
        "born_date": "",
        "born_location": "",
        "description": ""
    }

    # Check for items and add them to author information
    born_date_elem = soup.select_one(".author-born-date")
    if born_date_elem:
        author_info["born_date"] = born_date_elem.get_text(strip=True)

    born_location_elem = soup.select_one(".author-born-location")
    if born_location_elem:
        author_info["born_location"] = born_location_elem.get_text(strip=True)

    description_elem = soup.select_one(".author-description")
    if description_elem:
        author_info["description"] = description_elem.get_text(strip=True)

    return author_info

while quotes_url:
    full_url = base_url + quotes_url
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get quotes info
    for quote in soup.select(".quote"):
        tags = [tag.get_text(strip=True) for tag in quote.select(".tag")]
        author_name = quote.select_one(".author").get_text(strip=True)
        text = quote.select_one(".text").get_text(strip=True)

        # Get a link to the author
        author_link = quote.select_one(".author + a")
        author_url = base_url + author_link["href"]
        
        # Get information about the author, if it is not already saved
        if author_name not in authors_data:
            author_info = get_author_info(author_url)
            authors_data[author_name] = author_info

        quotes_data.append({"tags": tags, "author": author_name, "quote": text})

    # Get a link to the next page
    next_page = soup.select_one(".next a")
    quotes_url = next_page["href"] if next_page else None

# Save data to JSON files
with open("quotes.json", "w", encoding="utf-8") as quotes_file:
    json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

with open("authors.json", "w", encoding="utf-8") as authors_file:
    json.dump(list(authors_data.values()), authors_file, ensure_ascii=False, indent=2)
