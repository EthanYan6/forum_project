from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from boards.forms import NewTopicForm
from .models import Board, Topic, Post


# Create your views here.
def home(request):
    boards = Board.objects.all()
    boards_names = list()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    # do something...
    # try:
    #     board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404

    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first() # TODO: get the currently logged in user

    if request.method == 'POST':
        # subject = request.POST['subject']
        # message = request.POST['message']
        #
        # user = User.objects.first() # TODO: 临时使用一个账号作为登录用户
        #
        # topic = Topic.objects.create(
        #     subject=subject,
        #     board=board,
        #     starter=user
        # )
        #
        # post = Post.objects.create(
        #     message=message,
        #     topic=topic,
        #     created_by=user
        # )
        #
        # return redirect('board_topics', pk=board.pk) # TODO:redirect to the created topic page

        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk) # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board})

