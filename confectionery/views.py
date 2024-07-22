from django.shortcuts import render
from django.views import generic

class HomePage(generic.TemplateView):
    template_name = 'index.html'

