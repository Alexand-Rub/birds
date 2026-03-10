from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView

from .models import Discussions, Message
from .forms import MessageForm


class ListDiscussionView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.GET.get("sort") == 'old':
            sort = 'date'
        else:
            sort = '-date'

        if request.GET.get("search"):
            discussions = Discussions.objects.filter(title__icontains=request.GET.get("search")).order_by(sort)
        else:
            discussions = Discussions.objects.all().order_by(sort)

        context = {
            'sort': request.GET.get("sort"),
            'search': request.GET.get("search"),
            'discussions': discussions,
        }
        return render(request, 'discussions/list_discussion.html', context=context)

class MyListDiscussionView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.GET.get("sort") == 'old':
            sort = 'date'
        else:
            sort = '-date'

        if request.GET.get("search"):
            discussions = Discussions.objects.filter(
                title__icontains=request.GET.get("search"),
                user=request.user
            ).order_by(sort)
        else:
            discussions = Discussions.objects.filter(user=request.user).order_by(sort)

        context = {
            'sort': request.GET.get("sort"),
            'search': request.GET.get("search"),
            'discussions': discussions,
        }
        return render(request, 'discussions/list_discussion.html', context=context)

class CreateDiscussionView(LoginRequiredMixin, CreateView):
    model = Discussions
    fields = ['title', 'content', 'image']
    template_name = 'discussions/create_discussion.html'
    success_url = reverse_lazy("discussions:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.save()
        return super(CreateDiscussionView, self).form_valid(form)

class DetailDiscussionView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        context = {
            'discussion': Discussions.objects.get(pk=pk),
            'massages': Message.objects.all().filter(discussion=pk),
            'form': MessageForm(),
            'group_exists': request.user.groups.filter(name='Moderators').exists(),
            'login': request.user.is_authenticated,
        }
        return render(
            request,
            'discussions/detail_discussion.html',
            context=context
        )
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('userprofile:login')
        form = MessageForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            author = request.user
            discussion = Discussions.objects.get(pk=pk)
            Message.objects.create(
                text=text,
                discussion=discussion,
                author=author
            )
        return redirect('discussions:detail', pk=pk)

class DeleteDiscussionView(UserPassesTestMixin, DeleteView):
    pass

class DeleteMessageView(UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("discussions:list")
    template_name = 'birdlib/delete.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Moderators').exists()
