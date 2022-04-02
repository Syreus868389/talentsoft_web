from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

def get_token (client_id, client_secret):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url="https://radiofrance-coll.talent-soft.com/api/token", include_client_id=True, client_secret=client_secret)

    return token['access_token']