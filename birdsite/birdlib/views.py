from pyclbr import Class

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from .models import Bird


# class ListBirdView(ListView):
#     model = Bird
#     template_name = 'birdlib/list_bird.html'
#     context_object_name = 'birds'

class ListBirdView(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        if request.GET.get("bird"):
            birds = (
                Bird.objects.filter(name__icontains=request.GET.get("bird"))
                | Bird.objects.filter(squad__icontains=request.GET.get("bird"))
                | Bird.objects.filter(family__icontains=request.GET.get("bird"))
                | Bird.objects.filter(genus__icontains=request.GET.get("bird"))
                | Bird.objects.filter(protection__icontains=request.GET.get("bird"))
            )
        else:
            birds = Bird.objects.all()
        context = {
            'search': request.GET.get("bird"),
            'birds': birds,
        }
        return render(request, 'birdlib/list_bird.html', context=context)

class FavouritesListBirdView(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        if request.GET.get("bird"):
            birds = (
                Bird.objects.filter(name__icontains=request.GET.get("bird"))
                | Bird.objects.filter(squad__icontains=request.GET.get("bird"))
                | Bird.objects.filter(family__icontains=request.GET.get("bird"))
                | Bird.objects.filter(genus__icontains=request.GET.get("bird"))
                | Bird.objects.filter(protection__icontains=request.GET.get("bird"))
            )
        else:
            birds = request.user.favourites.all()
            # birds = Bird.objects.all()
        context = {
            'search': request.GET.get("bird"),
            'birds': birds,
        }
        return render(request, 'birdlib/list_bird.html', context=context)


class CreateBirdView(UserPassesTestMixin, CreateView):
    model = Bird
    fields = [
        'name', 'lat_name', 'squad',
        'family', 'genus', 'habitat',
        'description', 'audio', 'logo_men', 'logo_woman'
    ]
    template_name = 'birdlib/create_bird.html'
    success_url = reverse_lazy("userprofile:login")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Moderators').exists()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.save()
        return super(CreateBirdView, self).form_valid(form)

# class DetailBirdView(DetailView):
#     model = Bird
#     template_name = 'birdlib/detail_bird.html'
#     context_object_name = 'bird'

class DetailBirdView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        if request.user.is_authenticated:
            favourites = request.user.favourites.filter(pk=pk).first()
        else:
            favourites = False
        context = {
            'group_exists': request.user.groups.filter(name='Moderators').exists(),
            'favourites': favourites,
            'bird': Bird.objects.get(pk=pk),
        }
        return render(request, 'birdlib/detail_bird.html', context=context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("userprofile:login"))
        favourites = request.user.favourites.filter(pk=pk).first()
        if not favourites:
            bird = Bird.objects.get(pk=pk)
            user = request.user
            bird.favourites.add(user)
            print('добавили избранное')
            flag = True
        else:
            bird = Bird.objects.get(pk=pk)
            user = request.user
            bird.favourites.remove(user)
            flag = False

        context = {
            'group_exists': request.user.groups.filter(name='Moderators').exists(),
            'favourites': flag,
            'bird': Bird.objects.get(pk=pk),
        }
        return render(request, 'birdlib/detail_bird.html', context=context)

class DeleteBirdView(UserPassesTestMixin, DeleteView):
    model = Bird
    success_url = reverse_lazy("birdlib:list")
    template_name = 'discussions/delete.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Moderators').exists()