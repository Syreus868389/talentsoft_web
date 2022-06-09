import re
import string
from spellchecker import SpellChecker
from talent.resources import *
import requests
from talent.auth_helper import get_token_talentsoft
from datetime import datetime
from talent.models import Offer, OfferFranceBleu

spell = SpellChecker(language='fr')

# Load valid words from resources
spell.word_frequency.load_words(valid)

# Get current datetime
today = datetime.now()

# Get offers from TalentSoft
def get_offers_base(token, count):

    # Initialize list
    offers = []

    # Prepare headers for request
    headers = {'Content-Type' :'application/json; charset=utf-8','Authorization' : f'Bearer {token}'}
    url = f"https://radiofrance-coll.talent-soft.com/api/v2/offersummaries?count={count}"

    # Send GET request to Talentsoft API
    r = requests.get(url, headers=headers)

    # Translate response to JSON
    data = r.json()

    # For loop to get detailes information for each offer and populate list
    for element in data['data']:

        reference = element['reference']
        params = {'reference': reference, 'metadata' : 'true'}
        r_offer = requests.get('https://radiofrance-coll.talent-soft.com/api/v2/offers/getoffer', headers=headers, params=params)
        offer = r_offer.json()
        offers.append(offer)
    
    return offers

# Get direction or service for each offer
def get_direction(offer):
    if offer['customFields']['offer']['shortText1']:
        direction = offer['customFields']['offer']['shortText1']
    else:
        direction = offer['organisation']['name']
    
    return direction

# Delete duplicates from list of categories
def delete_duplicates(cat_list):
  return list(dict.fromkeys(cat_list))

# Lowcase articles
def article_lowcaser(text):
    for article in articles:
        if article.title() in text:
            text = text.replace(article.title(), article)
    
    return text

# Uppercase specific words from resources
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
        # Add title, directio and url attributes to current class object
        self.title = original_offer_title.lower()
        self.direction = original_offer_direction.lower()
        self.url = original_offer_url

    def offer_cleaner(self):

        # Initialize variables
        service = ""
        postes = ""
        mob = ""
        france_bleu = False
        text = self.title
        direction = self.direction
        color = ""
        cat = []

        # Check if the offer concerns France Bleu
        if "france bleu" in direction or "région" in direction:
            france_bleu = True

        # If the offer has a colon, delete the first part as it is most likely the service, and record it if it indicates multiples jobs
        if ":" in text:
            split_colon = text.split(":")

            if "postes" in split_colon[0]:
                postes = split_colon[0]
            
            text = split_colon[1]

        # Delete suffixes
        for suffix in suffixes:

            parenth = "(" + suffix + ")"
            if parenth in text:
                text = text.replace(parenth, "")

            for point in punctuation:
                compound = point + suffix
                cond = compound + " "
                if cond in text :
                    text = text.replace(compound, "")

        # Split text to word list in order to make spell check
        no_point_text = text.translate(str.maketrans('','', string.punctuation))
        spell_list = no_point_text.split()

        # Spell check
        for word in spell_list:
            if word not in spell:
                cor = spell.correction(word)
                text = text.replace(word, cor)

        # Split text if there are hyphens, update varaiables according to values, and delete unnecessary parts
        if "-" in text:
            split_text = text.split("-")
            for part in split_text:
                if "mobilité" in part :
                    text = text.replace(part, "")
                    mob = True

                # Workaround if multiple jobs indications are between parentheses
                for chiffre_par, chiffre in zip(postes_numbers_par, postes_numbers):
                    if chiffre_par in part:
                        postes = chiffre
                        text = text.replace(chiffre_par, "")

                # Check if it is France Bleu once again
                if "france bleu" in part or "fb" in part:
                    text = text.replace(part, "")
                    france_bleu = True

                if france_bleu:
                    for word in france_bleu_words:
                        if word in part:
                            text = text.replace(word, "")

                # Record if there are details about the service
                if "service technique" in part or "délégation" in part:
                    text = text.replace(part, "")
                    if "h/f" in part:
                        part = part.replace("h/f", "")
                    part = part.strip(" ")
                    service = part.title()
                    service = article_lowcaser(service)

                # Sud-Méditerranée workaround
                if "méditerranée" in part.lower() and "-" in part:
                    if service:
                        service = service + "-" + part
                        text = text.replace(part, "")  

                # Refining service and direction
                if "direction" in part or "orchestre" in part:
                    direction = part
                    text = text.replace(part, "")

        # Delete France Bleu mentions if some are left
        else:
            for bleu in bleus:
                low = bleu.lower()
                if low in text:
                    text = text.replace(low, "")
        
        # Clean direction from trailing spaces
        direction = direction.strip()

        # Clean text from punctuation and trailing spaces
        text = text.strip(" -:")
        text = text.replace("  ", " ")

        # Assign categories
        for key, values in labels.items():
            for value in values:
                if value in text:
                    cat.append(key)
        
        cat = delete_duplicates(cat)
        
        # If only one category is assigned, the textt is black, if not it will be red
        if len(cat) == 1:
            color = black
        
        elif len(cat) > 1:
            color = red
     
        else:
            cat.append("À catégoriser")
            color = red

        # Replace some words
        for x, y in zip(replaced, replacements):
            if x in text:
                text = text.replace(x, y)
            if x in direction:
                direction = direction.replace(x, y)


        # Capitalize first letter
        text = text[0].upper() + text[1:]

        # Add "H/F" mention
        if "h/f" not in text:
            text = text + ("h/f")

        if re.search(r'(?<=\S)h/f', text):
            text = text.replace("h/f", " H/F")   
        else:
            text = text.replace("h/f", "H/F")   

        # Compose France Bleu offers, assigning a city
        if france_bleu:
            self.ville = ""
            villes = []
            direction = direction.title()
            direction = article_lowcaser(direction)
            for locale, ville in bleus_villes.items():
                if locale in direction:
                    villes.append(ville)
                    self.ville = "(" + villes[0] + ")"

            if not self.ville:
                color = orange
        
        # Uppercase direction or service
        else:
            direction = highcaser(direction, capital)
            direction = highcaser(direction, syndicats, all_caps=True)
            direction = direction[0].upper() + direction[1:]
            
        # Assign attributes to class object    
        self.title = text
        self.direction = direction
        self.mob = mob
        self.postes = postes
        self.france_bleu = france_bleu

        # Keep only one category
        cat = cat[0]

        self.cat = cat
        self.color = color
        self.creation_date = today.strftime('%A %d %B %Y - %H:%M')

# Main function
def get_offers():
    
    # Fetch tables from database and delete values
    tables = [Offer, OfferFranceBleu]
    
    for table in tables:
        old_offers = table.objects.all()
        old_offers.delete()

    # Get Talentsoft token and offers
    token_talentsoft = get_token_talentsoft()
    offers_base = get_offers_base(token_talentsoft, 50)

    for offer in offers_base:

        # Process offers
        direction = get_direction(offer)
        offer = OfferProcessor(offer['title'], direction, offer['offerUrl'])
        offer.offer_cleaner()

        # Write offers to database
        if offer.france_bleu:
          offer_in_db = OfferFranceBleu(
              title = offer.title,
              cat = offer.cat,
              color = offer.color,
              postes = offer.postes,
              direction = offer.direction,
              mob = offer.mob,
              creation_date = offer.creation_date,
              ville = offer.ville,
              url = offer.url
            )
        else:
          offer_in_db = Offer(
              title = offer.title,
              cat = offer.cat,
              color = offer.color,
              postes = offer.postes,
              direction = offer.direction,
              mob = offer.mob,
              creation_date = offer.creation_date,
              url = offer.url
            )
        
        # Save database
        offer_in_db.save()

def run():
    get_offers()
    


