from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
# from django.db.models.signals import post_save


class Association(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=254, unique=True, null=True)
    numero = models.TextField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    docRecepiss = models.FileField(
        upload_to='VerifyDocument/', null=True, blank=True)
    activitePrincipal = ArrayField(models.CharField(
        max_length=100, default='distribution', blank=True), null=True)
    activiteSecondaire = ArrayField(models.CharField(
        max_length=100, default='sante', blank=True), null=True)
    activiteThird = ArrayField(models.CharField(
        max_length=100, default='assistance', blank=True), null=True)


# Create your models here.
