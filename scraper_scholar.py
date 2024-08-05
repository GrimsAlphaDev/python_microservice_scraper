# scraper_scholar.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_scholar_data(scholar_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f'https://scholar.google.com/citations?user={scholar_id}'
    driver.get(url)
    time.sleep(1)
    
    articles = []
    
    while True:
        try:
            button = driver.find_element(By.ID, 'gsc_bpf_more')
            button.click()
            time.sleep(3)
            
            if(button.get_attribute('disabled')):
                rows = driver.find_elements(By.CSS_SELECTOR, '.gsc_a_tr')
                for row in rows:
                    title = row.find_element(By.CSS_SELECTOR, '.gsc_a_at').text
                    authors = row.find_elements(By.CSS_SELECTOR, '.gs_gray')[0].text
                    journal = row.find_elements(By.CSS_SELECTOR, '.gs_gray')[1].text
                    citations = row.find_element(By.CSS_SELECTOR, '.gsc_a_ac').text
                    year = row.find_element(By.CSS_SELECTOR, '.gsc_a_h').text
                    link = row.find_element(By.CSS_SELECTOR, '.gsc_a_at').get_attribute('href')
                    articles.append({
                        'title': title,
                        'link': link,
                        'authors': authors,
                        'journal': journal,
                        'citations': citations,
                        'year': year,
                    })
                break
        except Exception:
            break
    driver.quit()
    return articles