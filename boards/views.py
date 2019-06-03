from django.http import Http404
from django.shortcuts import render
from .models import Board


# Create your views here.



def home(request):
    boards = Board.objects.all()
    boards_names = list()

    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    # do something...
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404

    return render(request, 'topics.html', {'board': board})

