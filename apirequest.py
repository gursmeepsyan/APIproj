import requests
import pandas as pd

baseurl = 'https://rickandmortyapi.com/api/'
endpoint = 'character'

def main_request(baseurl, endpoint, x):
    try:
        r = requests.get(f'{baseurl}{endpoint}?page={x}')
        r.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_pages(response):
    if response is not None and 'info' in response:
        return response['info']['pages']
    return 0

def parse_json(response):
    charlist = []
    if response is not None and 'results' in response:
        for item in response['results']:
            char = {
                'ID': item['id'],
                'name': item['name'],
                'num_eps': len(item['episode'])
            }
            charlist.append(char)
    return charlist

mainlist = []
data = main_request(baseurl, endpoint, 1)
total_pages = get_pages(data)

if total_pages > 0:
    for x in range(1, total_pages + 1):
        page_data = main_request(baseurl, endpoint, x)
        if page_data:
            mainlist.extend(parse_json(page_data))

df = pd.DataFrame(mainlist)

df.to_csv('charlist.csv', index=False)
