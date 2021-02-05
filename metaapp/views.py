from django.shortcuts import render

# Create your views here.

from metaapp.models import Psychotherapist, PsychotherapistRaw

def frontend(request):
    psychotherapists = Psychotherapist.objects.all()

    data ={
        "psychotherapists": psychotherapists,
    }

    return render(request, "metaapp/template.html", data)
