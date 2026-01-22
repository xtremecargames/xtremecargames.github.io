import requests
from bs4 import BeautifulSoup
import os
import re

def fetch_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def combine_texts(texts):
    return "#\n".join(texts)

def main():
    urls = os.getenv('APP_ADS_URLS')
    
    if not urls:
        print("No URLs are set properly.")
        return
    
    urls = re.split(r'[,\n]+', urls.strip())
    
    texts = [fetch_text(url.strip()) for url in urls if url.strip()]
    combined_text = combine_texts(texts)

    output_file = "app-ads.txt"
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_text = file.read()
    else:
        existing_text = ""

    changes_detected = "false"
    if combined_text != existing_text:
        with open(output_file, 'w') as file:
            file.write(combined_text)
        changes_detected = "true"

    print(f"::set-output name=changes_detected::{changes_detected}")

if __name__ == "__main__":
    main()

