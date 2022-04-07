import re
import string
from spellchecker import SpellChecker
from talent.resources import *
import requests
from talent.auth_helper import get_token_talentsoft
import json

spell = SpellChecker(language='fr')

spell.word_frequency.load_words(valid)

def get_offers_base(token, count):
    offers = []
    headers = {'Content-Type' :'application/json; charset=utf-8','Authorization' : f'Bearer {token}'}
    url = f"https://radiofrance-coll.talent-soft.com/api/v2/offersummaries?count={count}"

    r = requests.get(url, headers=headers)

    data = r.json()

    for element in data['data']:

        reference = element['reference']
        params = {'reference': reference, 'metadata' : 'true'}
        r_offer = requests.get('https://radiofrance-coll.talent-soft.com/api/v2/offers/getoffer', headers=headers, params=params)
        offer = r_offer.json()
        offers.append(offer)
    
    return offers

def get_direction(offer):
    if offer['customFields']['offer']['shortText1']:
        direction = offer['customFields']['offer']['shortText1']
    else:
        direction = offer['organisation']['name']
    
    return direction

def delete_duplicates(cat_list):
  return list(dict.fromkeys(cat_list))

def article_lowcaser(text):
    for article in articles:
        if article.title() in text:
            text = text.replace(article.title(), article)
    
    return text

def highcaser(text, list, all_caps = False):
    for word in list:
        match = re.search(r'\b{0}\b'.format(word), text)
        if match:
            if all_caps: 
                text = text.replace(word, word.upper())
            else:
                text = text.replace(word, word.title())

    return text

class OfferProcessor:
    def __init__(self, original_offer_title, original_offer_direction, original_offer_url):
        self.title = original_offer_title.lower()
        self.direction = original_offer_direction.lower()
        self.url = original_offer_url

    def offer_cleaner(self):
        service = ""
        postes = ""
        mob = False
        france_bleu = False
        text = self.title
        direction = self.direction

        if "france bleu" in direction or "région" in direction:
            france_bleu = True

        if ":" in text:
            split_colon = text.split(":")
            if "postes" in split_colon[0]:
                postes = split_colon[0]
            text = split_colon[1]

        for suffix in suffixes:

            parenth = "(" + suffix + ")"
            if parenth in text:
                text = text.replace(parenth, "")

            for point in punctuation:
                compound = point + suffix
                cond = compound + " "
                if cond in text :
                    text = text.replace(compound, "")

        no_point_text = text.translate(str.maketrans('','', string.punctuation))
        spell_list = no_point_text.split()

        for word in spell_list:
            if word not in spell:
                cor = spell.correction(word)
                text = text.replace(word, cor)

        if "-" in text:
            split_text = text.split("-")
            for part in split_text:
                if "mobilité" in part :
                    text = text.replace(part, "")
                    mob = True

                if "france bleu" in part or "fb" in part:
                    text = text.replace(part, "")
                    france_bleu = True

                if france_bleu:
                    for word in france_bleu_words:
                        if word in part:
                            text = text.replace(word, "")

                if "service technique" in part or "délégation" in part:
                    text = text.replace(part, "")
                    if "h/f" in part:
                        part = part.replace("h/f", "")
                    part = part.strip(" ")
                    service = part.title()
                    service = article_lowcaser(service)

                if "méditerranée" in part.lower() and "-" in part:
                    if service:
                        service = service + "-" + part
                        text = text.replace(part, "")  


                if "direction" in part or "orchestre" in part:
                    direction = part
                    text = text.replace(part, "")

        else:
            for bleu in bleus:
                low = bleu.lower()
                if low in text:
                    text = text.replace(low, "")
        
        direction = direction.strip()

        text = text.strip(" -")
        text = text.replace("  ", " ")

        for x, y in zip(replaced, replacements):
            if x in text.lower():
                text = text.replace(x, y)

        text = text[0].upper() + text[1:]

        if "h/f" not in text:
            text = text + ("h/f")

        if re.search(r'(?<=\S)h/f', text):
            text = text.replace("h/f", " H/F")   
        else:
            text = text.replace("h/f", "H/F")   

        if france_bleu:
            direction = direction.title()
            direction = article_lowcaser(direction)
        
        else:
            direction = highcaser(direction, capital)
            direction = highcaser(direction, syndicats, all_caps=True)
            direction = direction[0].upper() + direction[1:]
            
        self.title = text
        self.direction = direction
        self.mob = mob
        self.postes = postes
        self.france_bleu = france_bleu

        color = ""
        cat = []

        for key, values in labels.items():
            for value in values:
                if value in self.title.lower():
                    cat.append(key)
        
        cat = delete_duplicates(cat)
        
        if len(cat) == 1:
            color = black
        
        elif len(cat) > 1:
            color = red
     
        else:
            cat.append("À catégoriser")
            color = red

        cat = cat[0]

        self.cat = cat
        self.color = color

        offer={"color": self.color, "postes": self.postes, "mob": self.mob, "url": self.url, "title": self.title, "direction": self.direction}

        return offer

def get_offers():

    token_talentsoft = get_token_talentsoft()
    offers_base = get_offers_base(token_talentsoft, 50)
    offers_france_bleu = {}
    offers_paris = {}
    for offer in offers_base:
        direction = get_direction(offer)
        offer = OfferProcessor(offer['title'], direction, offer['offerUrl'])
        cleaned_offer = offer.offer_cleaner()
        if offer.france_bleu:
          offers_france_bleu.setdefault(offer.cat, []).append(cleaned_offer)
        else:
          offers_paris.setdefault(offer.cat, []).append(cleaned_offer)
    return {"offers_paris": offers_paris, "offers_france_bleu": offers_france_bleu}

def run():
    offers = get_offers()
    with open('talent/generated_offers.json', 'w') as file:
        json.dump(offers, file)
    


