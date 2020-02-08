from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")

def create_transaction(request):
    return HttpResponse("Creating a transaction")
# Create your views here.
