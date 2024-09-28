import requests
from bs4 import BeautifulSoup
import json
import sys


def get_sinta_publications(author_id):

    results = []
    publications = []

    # Base URL for the Sinta author page
    url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"

    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    profiles = soup.find("div", class_="stat-profile")
    sinta_score_overall = profiles.find("div", class_="pr-num").text.strip()
    sinta_score_3years = profiles.find_all("div", class_="pr-num")[1].text.strip()
    affil_score = profiles.find_all("div", class_="pr-num")[2].text.strip()
    affil_score_3years = profiles.find_all("div", class_="pr-num")[3].text.strip()

    # Find the publication elements
    publication_scopus = []
    articles = soup.find_all("div", class_="ar-list-item")
    for article in articles:
        title_element = article.find("div", class_="ar-title")
        title = title_element.text.strip()
        link = title_element.find("a").get("href")
        meta_element = article.find("div", class_="ar-meta")
        journal = meta_element.find("a", class_="ar-pub").text.strip()
        journal_link = meta_element.find("a", class_="ar-pub").get("href")
        creators = meta_element.find_all("a")[-1].text.strip()
        quartile = meta_element.find("a", class_="ar-quartile").text.strip()
        meta_element = article.find_all("div", class_="ar-meta")[1]
        year = meta_element.find("a", class_="ar-year").text.strip()
        citations = meta_element.find("a", class_="ar-cited").text.strip()

        # Append publication data to the list
        publication_scopus.append(
            {
                "title": title,
                "link": link,
                "creators": creators,
                "journal": journal,
                "journal_link": journal_link,
                "quartile": quartile,
                "year": year,
                "citations": citations,
            }
        )
        
    # Base URL for the Sinta author page
    urlWOS = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}/?view=wos"

    # Send a GET request to the URL
    response = requests.get(urlWOS)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the publication elements
    publication_wos = []
    articles = soup.find_all("div", class_="ar-list-item")

    for article in articles:
        title_element = article.find("div", class_="ar-title")
        title = title_element.text.strip()
        link = title_element.find("a").get("href")

        meta_element = article.find("div", class_="ar-meta")
        publisher = meta_element.find("a", class_="ar-pub").text.strip()
        journal = meta_element.find_all("a", class_="ar-pub")[1].text.strip()
        journal_link = meta_element.find_all("a", class_="ar-pub")[1].get("href")
        authors = meta_element.find_all("a")[4].text.strip()
        meta_elements = article.find_all("div", class_="ar-meta")
        year = ""
        citation = ""
        doi = ""

        # Handle the second ar-meta div if it exists
        if len(meta_elements) > 1:
            meta_element2 = meta_elements[1]
            year_element = meta_element2.find("a", class_="ar-year")
            citation_element = meta_element2.find("a", class_="ar-cited")
            doi_element = meta_element2.find("a", class_="ar-sinta")
            if year_element:
                year = year_element.text.strip()
            if citation_element:
                citation = citation_element.text.strip()
            if doi_element:
                doi = doi_element.text.strip()

        # Append publication data to the list
        publication_wos.append(
            {
                "title": title,
                "link": link,
                "publisher": publisher,
                "journal": journal,
                "journal_link": journal_link,
                "authors": authors,
                "year": year,
                "citation": citation,
                "doi": doi,
            }
        )

    # Base URL for the Sinta author page
    urlGaruda = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}/?view=garuda"

    # Send a GET request to the URL
    response = requests.get(urlGaruda)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the publication elements
    publication_garuda= []
    articles = soup.find_all("div", class_="ar-list-item")
    
    for article in articles:
        title_element = article.find("div", class_="ar-title")
        title = title_element.text.strip()
        link = title_element.find("a").get("href")
        meta_element = article.find("div", class_="ar-meta")
        publisher = meta_element.find("a").text.strip()
        journal = meta_element.find("a", class_="ar-pub").text.strip()
        journal_link = meta_element.find("a", class_="ar-pub").get("href")
        meta_element2 = article.find_all("div", class_="ar-meta")[1]
        authors = meta_element2.find_all("a")[1].text.strip()
        year = meta_element2.find("a", class_="ar-year").text.strip()
        doi = meta_element2.find("a", class_="ar-cited").text.strip()
        akreditasi = meta_element2.find("a", class_="ar-quartile").text.strip()
        
        # Append publication data to the list
        publication_garuda.append(
            {
                "title": title,
                "link": link,
                "publisher": publisher,
                "journal": journal,
                "journal_link": journal_link,
                "authors": authors,
                "year": year,
                "doi": doi,
                "akreditasi": akreditasi,
            }
        )
    
    # Base URL for the Sinta author page
    urlScholar = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}/?view=googlescholar"

    # Send a GET request to the URL
    response = requests.get(urlScholar)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the publication elements
    publication_scholar= []
    articles = soup.find_all("div", class_="ar-list-item")

    for article in articles:
        title_element = article.find("div", class_="ar-title")
        title = title_element.text.strip()
        link = title_element.find("a").get("href")
        meta_element = article.find("div", class_="ar-meta")
        author = meta_element.find("a").text.strip()
        journal = meta_element.find("a", class_="ar-pub").text.strip()
        meta_element2 = article.find_all("div", class_="ar-meta")[1]
        year = meta_element2.find("a", class_="ar-year").text.strip()
        citation = meta_element2.find("a", class_="ar-cited").text.strip()
    
        publication_scholar.append({
            "title": title,
            "link": link,
            "author": author,
            "journal": journal,
            "year": year,
            "citation": citation,
        })
    
        #  Rama belum ada publikasi

    publications.append(
        {
            "scopus": publication_scopus,
            "wos": publication_wos,
            "garuda": publication_garuda,
            "scholar": publication_scholar,
        }
    )

    # Base URL for researches tab
    url2 = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}/?view=researches"

    # Send a GET request to the URL
    response = requests.get(url2)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the publication elements
    researches = []
    articles = soup.find_all("div", class_="ar-list-item")

    for article in articles:
        title = article.find("div", class_="ar-title").text.strip()
        link = article.find("div", class_="ar-title").find("a").get("href")
        leader = article.find("div", class_="ar-meta").find("a").text.strip()
        journal = (
            article.find("div", class_="ar-meta")
            .find("a", class_="ar-pub")
            .text.strip()
        )
        meta_element = article.find_all("div", class_="ar-meta")[1]
        personils = meta_element.find("a").text.strip()
        meta_element2 = article.find_all("div", class_="ar-meta")[2]
        year = meta_element2.find("a", class_="ar-year").text.strip()
        quartile = meta_element2.find("a", class_="ar-quartile").text.strip()
        approved = meta_element2.find(
            "a", class_="ar-quartile text-success"
        ).text.strip()

        researches.append(
            {
                "title": title,
                "link": link,
                "leader": leader,
                "journal": journal,
                "personils": personils,
                "year": year,
                "quartile": quartile,
                "approved": approved,
            }
        )

    # Base URL for Community Service tab
    url3 = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}/?view=services"

    # Send a GET request to the URL
    response = requests.get(url3)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the publication elements
    communityService = []
    articles = soup.find_all("div", class_="ar-list-item")

    for article in articles:
        title = article.find("div", class_="ar-title").text.strip()
        link = article.find("div", class_="ar-title").find("a").get("href")
        leader = article.find("div", class_="ar-meta").find("a").text.strip()
        journal = (
            article.find("div", class_="ar-meta")
            .find("a", class_="ar-pub")
            .text.strip()
        )
        meta_element = article.find_all("div", class_="ar-meta")[1]
        # loop get all personils dipisahkan oleh (;)
        personils = meta_element.find("a").text.strip()
        meta_element2 = article.find_all("div", class_="ar-meta")[2]
        year = meta_element2.find("a", class_="ar-year").text.strip()
        quartile = meta_element2.find("a", class_="ar-quartile").text.strip()
        approved = meta_element2.find(
            "a", class_="ar-quartile text-success"
        ).text.strip()

        communityService.append(
            {
                "title": title,
                "link": link,
                "leader": leader,
                "journal": journal,
                "personils": personils,
                "year": year,
                "quartile": quartile,
                "approved": approved,
            }
        )

    # Base URL for Community Service tab
    url4 = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}/?view=iprs"

    # Send a GET request to the URL
    response = requests.get(url4)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the publication elements
    iprs = []
    articles = soup.find_all("div", class_="ar-list-item")

    for article in articles:
        title = article.find("div", class_="ar-title").text.strip()
        link = article.find("div", class_="ar-title").find("a").get("href")
        inventor = article.find_all("div", class_="ar-meta")[0].find("a").text.strip()
        publication = (
            article.find_all("div", class_="ar-meta")[0]
            .find("a", class_="ar-pub")
            .text.strip()
        )
        year = (
            article.find_all("div", class_="ar-meta")[1]
            .find("a", class_="ar-year")
            .text.strip()
        )
        permohonan = (
            article.find_all("div", class_="ar-meta")[1]
            .find("a", class_="ar-cited")
            .text.strip()
        )
        hak = (
            article.find_all("div", class_="ar-meta")[1]
            .find("a", class_="ar-quartile")
            .text.strip()
        )

        iprs.append(
            {
                "title": title,
                "link": link,
                "inventor": inventor,
                "publication": publication,
                "year": year,
                "permohonan": permohonan,
                "hak": hak,
            }
        )

    # Base URL for Books tab
    url5 = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}/?view=books"

    # Send a GET request to the URL
    response = requests.get(url5)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for author ID {author_id}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the publication elements
    books = []
    articles = soup.find_all("div", class_="ar-list-item")

    for article in articles:
        title = article.find("div", class_="ar-title").text.strip()
        link = article.find("div", class_="ar-title").find("a").get("href")
        category = article.find_all("div", class_="ar-meta")[0].find("a").text.strip()
        author = article.find_all("div", class_="ar-meta")[1].find("a").text.strip()
        publisher = (
            article.find_all("div", class_="ar-meta")[1]
            .find("a", class_="ar-pub")
            .text.strip()
        )
        year = (
            article.find_all("div", class_="ar-meta")[2]
            .find("a", class_="ar-year")
            .text.strip()
        )
        kota = (
            article.find_all("div", class_="ar-meta")[2]
            .find("a", class_="ar-cited")
            .text.strip()
        )
        isbn = (
            article.find_all("div", class_="ar-meta")[2]
            .find("a", class_="ar-quartile")
            .text.strip()
        )

        books.append(
            {
                "title": title,
                "link": link,
                "category": category,
                "author": author,
                "publisher": publisher,
                "year": year,
                "kota": kota,
                "isbn": isbn,
            }
        )

    # push publication to result as json
    results.append(
        {
            "sinta_score_overall": sinta_score_overall,
            "sinta_score_3years": sinta_score_3years,
            "affil_score": affil_score,
            "affil_score_3years": affil_score_3years,
            "publications": publications,
            "researches": researches,
            "communityService": communityService,
            "iprs": iprs,
            "books": books,
        }
    )

    return results


if __name__ == "__main__":
    author_id = sys.argv[1]
    data = get_sinta_publications(author_id)
    print(json.dumps(data, indent=4))
