from bs4 import BeautifulSoup

def compare_prev(html, offers_corpus):

    soup = BeautifulSoup(html)
    theme_blocks = soup.find_all("p",{"class":"xxxmsonormal"})

    for theme_block in theme_blocks:
        last_week_cat = theme_block.find(style="color:#283493")
        if last_week_cat:
            new_cat = last_week_cat.string
            blocks = theme_block.next_sibling
            for block in blocks:   
                for offers in offers_corpus:
                    for offer in offers:
                        if block.a:
                            if block.a.get("href") == offer['url']:
                                offer['cat'] = new_cat
                                offer['last_week_content'] = f'{block}'

    return offers_corpus