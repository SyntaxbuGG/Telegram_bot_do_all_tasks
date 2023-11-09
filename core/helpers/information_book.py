import requests


def request_main(name_author):
    url_get = f"https://openlibrary.org/search/authors.json?q={name_author}"
    get_url = requests.get(url_get).json()
    key_author = get_url.get('docs')[0]
    url_author = f'https://covers.openlibrary.org/a/olid/{key_author["key"]}-L.jpg'
    return (key_author['name'], url_author)
