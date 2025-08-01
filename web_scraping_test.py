import requests
from bs4 import BeautifulSoup

url = "https://usda.library.cornell.edu/concern/publications/3t945q76s?locale=en"  # Replace with the actual URL
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

links = soup.find_all('a')

pdf_links = []
for link in links:
    href = link.get('href')
    if href and href.endswith('.pdf'):
        pdf_links.append(href)

for i, pdf_url in enumerate(pdf_links):
    try:
        pdf_response = requests.get(pdf_url, stream=True)
        pdf_response.raise_for_status()  # Raise an exception for bad status codes

        # Extract filename from URL or assign a generic name
        filename = pdf_url.split('/')[-1] if '/' in pdf_url else f"downloaded_pdf_{i+1}.pdf"

        with open(filename, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {pdf_url}: {e}")