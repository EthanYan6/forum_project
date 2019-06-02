from django.shortcuts import render
from django.http import HttpResponse
from boards.models import Board


# Create your views here.



def home(request):
    boards = Board.objects.all()
    boards_names = list()

    return render(request, 'home.html', {'boards': boards})
