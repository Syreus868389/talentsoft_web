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
          "contentBytes": base64_images['flash_info']
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "paris",
          "contentBytes": base64_images['paris']
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "region",
          "contentBytes": base64_images['region']
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "rf_long",
          "contentBytes": base64_images['rf_long']
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "rf",
          "contentBytes": base64_images['rf']
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "square",
          "contentBytes": base64_images['square']
        },
        {
          "@odata.type": "#microsoft.graph.fileAttachment",
          "name": "texto",
          "contentBytes": base64_images['texto']
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