from bs4 import BeautifulSoup

def compare_prev(html, offers_corpus):

    soup = BeautifulSoup(html)
    blocks = soup.find_all(id="offer")

    for block in blocks:
        for offers in offers_corpus:
            for offer in offers:
                if block.a.get('href') == offer['url']:
                    offer['last_week_content'] = f'{block}'

    return offers_corpus