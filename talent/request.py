from auth_helper import get_token_talentsoft
from offer_processor import get_offers, get_direction, OfferProcessor
import json

token = get_token_talentsoft()

offers = get_offers(token, 30)

for offer in offers:
    direction = get_direction(offer)

    offer = OfferProcessor(offer['title'], direction, offer['offerUrl'])
    offer.offer_cleaner()
    print(offer.color)
    
