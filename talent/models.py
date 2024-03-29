from django.db import models

class Offer(models.Model):
    title = models.CharField(max_length=300)
    cat = models.CharField(max_length=300)
    color = models.CharField(max_length=300)
    creation_date = models.CharField(max_length=300)
    postes = models.CharField(max_length=300)
    mob = models.CharField(max_length=300)
    direction = models.CharField(max_length=300)
    url = models.CharField(max_length=400)

class OfferFranceBleu(models.Model):
    title = models.CharField(max_length=300)
    cat = models.CharField(max_length=300)
    color = models.CharField(max_length=300)
    creation_date = models.CharField(max_length=300)
    postes = models.CharField(max_length=300)
    mob = models.CharField(max_length=300)
    direction = models.CharField(max_length=300)
    ville = models.CharField(max_length=300)
    url = models.CharField(max_length=400)
