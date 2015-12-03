from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(requrest):
    return HttpResponse("<html><title>To-Do list</title></html>")
