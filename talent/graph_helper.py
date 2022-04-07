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

def save_draft(token, body):
  body_json = {
      "subject":"Consultez les offres à pourvoir sur l’Espace Emploi de Radio France",
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
  drafter = requests.post(
    '{0}/users/textoflashinfo@radiofrance.com/messages'.format(graph_url),
    headers={
      'Authorization': 'Bearer {0}'.format(token),
      'Content-Type': 'application/json',
    }, json=body_json
  )

  return drafter.text