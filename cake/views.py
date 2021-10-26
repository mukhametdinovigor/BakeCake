from django.shortcuts import render
from .forms import ConstructCakeForm


def index(request):
    form = ConstructCakeForm()
    return render(request, 'index.html', {'form': form})
