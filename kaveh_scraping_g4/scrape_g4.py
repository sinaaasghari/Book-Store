

from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_writer_translators_book_description(url):
    
    # Search the blocks for all author and translator links
    def get_person_links(soup):
        blocks = soup.find_all("div", class_="clearfix")
        persons = {}

        for block in blocks:
            author_links = block.find_all("a", itemprop="author")

            for link in author_links:
                name = link.find("span", itemprop="name").text
                href = link["href"]
                persons[name] = href

        return persons

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    persons = get_person_links(soup)

    details_list = []

    for name, link in persons.items():
        person_response = requests.get(f"https://www.iranketab.ir{link}")
        person_soup = BeautifulSoup(person_response.content, "html.parser")

        person_id = link.split("/")[-1].split("-")[0]
        person_div = person_soup.find("div", class_="col-md-9")

        if person_div:
            person_description = person_div.find("h5").text.strip()
        else:
            person_description = None

        details_list.append(
            {"name": name, "id": person_id, "description": person_description}
        )

    df_person = pd.DataFrame(details_list)

    # Create dataframe for book descriptions
    book_id = url.split("/")[-1].split("-")[0]

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    description_div = soup.find("div", class_="product-description")

    if description_div:
        book_description = description_div.text.strip()
    else:
        book_description = None

    df_book = pd.DataFrame({"id": book_id, "description": book_description}, index=[0])


    return df_person, df_book


def get_hashtags_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tag_links = soup.find_all("a", class_="product-tags-item")

    details_list = []

    for link in tag_links:
        hashtag_url = f"https://www.iranketab.ir{link['href']}"

        hashtag_response = requests.get(hashtag_url)
        hashtag_soup = BeautifulSoup(hashtag_response.content, "html.parser")

        hashtag_id = link["href"].split("/")[-1].split("-")[0]

        description_div = hashtag_soup.find("div", class_="col-md-10")

        if description_div:
            description = description_div.find("h2").text.strip()
        else:
            description = None

        hashtag_text = link.text.strip()

        details_list.append(
            {"id": hashtag_id, "category": hashtag_text, "description": description}
        )

    df_hashtags = pd.DataFrame(details_list)
    
    return df_hashtags


# Try it out
url = "https://www.iranketab.ir/book/1007-man-s-search-for-meaning"

df_writer_translators, df_book_desc = get_writer_translators_book_description(url)
df_categories = get_hashtags_details(url)

print(f"writers & translators:\n{df_writer_translators}")
print(f"book description:\n{df_book_desc}")
print(f"categories:\n{df_categories}")
