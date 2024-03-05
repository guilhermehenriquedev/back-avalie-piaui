from django.shortcuts import render, redirect, reverse
from django.conf import settings 
from django.http import JsonResponse


def index(request):

    return render(request, "index.html", {
        'debug':settings.DEBUG,
        'environment':settings.ENVIRONMENT
        })
