import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def find_year_in_text(text):
    current_year = datetime.now().year
    pattern = re.compile(r'\b(19[0-9]{2}|20[0-9]{2}|21[0-9]{2})\b')
    matches = pattern.findall(text)
    years = [int(match) for match in matches if 1900 <= int(match) <= current_year]
    if years:
        return years[0]
    else:
        return None

def get_publications(garuda_id):
    page = 1
    url = f"https://garuda.kemdikbud.go.id/author/view/{garuda_id}?page={page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        next_button = soup.select_one('.page-column')
        
        if next_button:
            last_page = int(next_button.select('a')[-2].get_text())
            publications = []
            for page in range(1, last_page + 1):
                url = f"https://garuda.kemdikbud.go.id/author/view/{garuda_id}?page={page}"
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    for article in soup.find_all('div', class_='article-item'):
                        title_element = article.select_one('.title-article')
                        title = title_element.get_text(strip=True) if title_element else ''
                        
                        journal_element = article.select_one('.subtitle-article')
                        subtitle_text = journal_element.get_text(strip=True) if journal_element else ''
                        journal = subtitle_text
                        year = find_year_in_text(subtitle_text)

                        publisher_element = article.select_one('.subtitle-article:nth-of-type(2)')
                        publisher = publisher_element.get_text(strip=True) if publisher_element else ''
                        
                        authors = ', '.join([a.get_text(strip=True) for a in article.select('.author-article')])

                        url_element = article.select_one('.article-item a')
                        url = url_element.get('href') if url_element else ''
                        
                        doi_element = article.select_one('.article-item .action-article a.title-citation:nth-of-type(3)')
                        doi = doi_element.get_text(strip=True) if doi_element and doi_element.get_text(strip=True).startswith('DOI: ') else ''
                        
                        publications.append({
                            'title': title,
                            'year': year,
                            'journal': journal,
                            'authors': authors,
                            'url': url,
                            'publisher': publisher,
                            'doi': doi
                        })
            return publications
        else:
            return None
    else:
        return None