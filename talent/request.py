from auth_helper import get_token_talentsoft
from offer_processor import get_offers, get_direction, OfferProcessor
import json

token = get_token_talentsoft()

offers_base = get_offers(token, 30)

offers = {}

for offer in offers_base:
    direction = get_direction(offer)

    offer = OfferProcessor(offer['title'], direction, offer['offerUrl'])
    offer.offer_cleaner()
    offers.setdefault(offer.cat, []).append(offer)
    
