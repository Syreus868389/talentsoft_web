from auth_support import get_token
import requests
from config import *
from offer_processor import get_offers, get_direction, OfferProcessor
import json

token = get_token(client_id=client_id, client_secret=client_secret)

offers = get_offers(token, 30)

for offer in offers:
    direction = get_direction(offer)

    offer = OfferProcessor(offer['title'], direction, offer['offerUrl'])
    offer.offer_cleaner()
    print(offer.color)
    
