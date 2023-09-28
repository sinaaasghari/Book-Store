from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_writer_translators_book_description(url):
   
    # Search the blocks for all author and translator links
    def get_person_links(soup):
        if soup is None:
            print("Soup is empty!")
            return 0

        containers = soup.find_all("div", class_="product-container well clearfix")
        if not containers or len(containers) == 0:
            print("Container not found!")
            return 0

        container = containers[0]

        persons = {}

        blocks = container.find_all(
            lambda tag: tag.name == "div" and tag.get("class") == ["clearfix"]
        )
        for block in blocks:
            if block:
                anchors = block.find_all("a", itemprop="author")
                for anchor in anchors:
                    if anchor:
                        name_span = anchor.find("span", itemprop="name")
                        name = name_span.text.strip() if name_span else None
                        href = anchor["href"] if "href" in anchor.attrs else None

                        if name:
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

        person_description = None
        if person_div:
            h5_tag = person_div.find("h5")
            if h5_tag:
                person_description = h5_tag.text.strip()

        details_list.append(
            {"name": name, "id": person_id, "description": person_description}
        )

    df_person = pd.DataFrame(details_list)

    book_id = url.split("/")[-1].split("-")[0]

    description_div = soup.find("div", class_="product-description")

    book_description = None
    if description_div:
        book_description = description_div.text.strip()

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

        description = None
        if description_div:
            h2_tag = description_div.find("h2")
            if h2_tag:
                description = h2_tag.text.strip()

        hashtag_text = link.text.strip()

        details_list.append(
            {"id": hashtag_id, "category": hashtag_text, "description": description}
        )

    df_hashtags = pd.DataFrame(details_list)

    return df_hashtags


# Try it out
# url = "https://www.iranketab.ir/book/1007-man-s-search-for-meaning"
# url = 'https://www.iranketab.ir/book/92718-bia-ba-man-bebin'
# url = 'https://www.iranketab.ir/book/845-the-slight-edge'
url = "https://www.iranketab.ir/book/121589-high-conflict-why-we-get-trapped-and-how-we-get-out"

df_writer_translators, df_book_desc = get_writer_translators_book_description(url)
df_categories = get_hashtags_details(url)

print(f"writers & translators:\n{df_writer_translators}")
print(f"book description:\n{df_book_desc}")
print(f"categories:\n{df_categories}")
