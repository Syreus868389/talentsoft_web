from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from talent.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
from talent.graph_helper import *
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from talent.models import Offer, OfferFranceBleu
from django.forms.models import model_to_dict

# Create your views here.

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def home(request):
  context = initialize_context(request)

  return render(request, 'home.html', context)

def sign_in(request):
  # Get the sign-in flow
  flow = get_sign_in_flow()
  # Save the expected flow so we can use it in the callback
  try:
    request.session['auth_flow'] = flow
  except Exception as e:
    print(e)
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(flow['auth_uri'])

def callback(request):
  # Make the token request
  result = get_token_from_code(request)

  #Get the user's profile
  user = get_user(result['access_token'])

  # Store user
  store_user(request, user)
  return HttpResponseRedirect(reverse('home'))

def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))

def produce_draft(request):
  context = initialize_context(request)
  user = context['user']

  if user['is_authenticated']:
    referer = request.META.get('HTTP_REFERER')
    if referer == request.build_absolute_uri('/'):
      offers_france_bleu = {}
      offers_paris = {}

      offer_model = Offer.objects.values()
      offer_model_france_bleu = OfferFranceBleu.objects.values()

      for i in offer_model_france_bleu:
        offers_france_bleu.setdefault(i['cat'],[]).append(i)
      for i in offer_model:
        offers_paris.setdefault(i['cat'],[]).append(i)

      context['offers_france_bleu'] = offers_france_bleu
      context['offers_paris'] = offers_paris
      print(context)
      email = render_to_string('email.html', context=context)
      token = get_token(request)
      draft_response = save_draft(token, email)

      context['draft_response'] = json.loads(draft_response)

      return render(request, 'response.html', context)
    
    else:
      return render(request, '404.html')

  else:
    return render(request, '404.html')

  

