from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render


class HomePage(TemplateView):
    template_name = 'home/index.html'

