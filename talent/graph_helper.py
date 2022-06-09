import requests
import json
from talent.resources import base64_images

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
  # Send GET to /me
  user = requests.get(
    '{0}/me'.format(graph_url),
    headers={
      'Authorization': 'Bearer {0}'.format(token),
    },
    params={
      '$select': 'displayName,mail,mailboxSettings,userPrincipalName'
    })
  # Return the JSON result
  return user.json()

def get_previous_email(token):

  # Get the last offer email that was sent
  prev = requests.get('{0}/users/textoflashinfo@radiofrance.com/mailFolders/AQMkADUyMTVlNzBiLTA5MjUtNGYzZi04N2M0LTQ4YzE3MDUxY2U1YQAuAAADkG9IhG2sbkGrgBGxESAG7AEAE0lF7TDB8Ua0eQw7CjCi4wAAAc8-jAAAAA==/messages'.format(graph_url), headers={
    'Authorization': 'Bearer {0}'.format(token),
    'Content-Type': 'application/json'},
    params={'$top':7, '$search':'Consultez'}
  )
  email = prev.json()['value'][0]['body']['content']
  
  return email

def save_draft(token, body):

  # Create json body with all necessary information for draft email
  body_json = {
      "subject":"Consultez les offres à pourvoir sur l’Espace Emploi de Radio France",
      "from": {
        "emailAddress" : {
          "address":"textoflashinfo@radiofrance.com"
        }
      },
      "body": {
        "contentType":"HTML",
        "content": body
      },
      "hasAttachments": False,
      "attachments":[
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "flash_info",
          "contentId": "flash_info",
          "contentType": "image/png;base64",
          "contentBytes": base64_images['flash_info'],
          "isInline" : True
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "paris",
          "contentId": "paris",
          "contentType": "image/png;base64",
          "contentBytes": base64_images['paris'],
          "isInline" : True
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "region",
          "contentId": "region",
          "contentType": "image/png;base64",
          "contentBytes": base64_images['region'],
          "isInline" : True
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "rf_long",
          "contentId": "rf_long",
          "contentType": "image/png;base64",
          "contentBytes": base64_images['rf_long'],
          "isInline" : True
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "square",
          "contentId": "square",
          "contentType": "image/png;base64",
          "contentBytes": base64_images['square'],
          "isInline" : True
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "texto",
          "contentId": "texto",
          "contentType": "image/png;base64",
          "contentBytes": base64_images['texto'],
          "isInline" : True
        }
      ]
  }

  # Save draft to mailbox
  drafter = requests.post(
    '{0}/users/textoflashinfo@radiofrance.com/messages'.format(graph_url),
    headers={
      'Authorization': 'Bearer {0}'.format(token),
      'Content-Type': 'application/json',
    }, json=body_json
  )

  # Return POST response
  return drafter.text