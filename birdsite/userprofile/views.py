from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import RegisterUserForm, ProfileUpdateForm
from .models import Profile, User


def profile_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("userprofile:profile_pk", pk=request.user.id)
    return redirect(reverse("userprofile:login"))

class ProfileView(DetailView):
    template_name = "userprofile/profile.html"
    # model = Profile
    queryset = (
        User.objects.select_related("profile")
    )
    context_object_name = "profile"
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['group_exists'] = self.request.user.groups.filter(name='Moderators').exists()
        return context


def login_view(request: HttpRequest):
    if request.method == 'GET':  # проверяем метод запроса
        if request.user.is_authenticated:  # проверяем авторизован ли
            return redirect("userprofile:profile")  # перенапрявляем если уже да
        return render(request, 'userprofile/login.html')
    # если запрос POST
    username = request.POST["username"]
    password = request.POST["password"]
    # авторизация
    user = authenticate(request, username=username, password=password)

    if user is not None: # если авторизавался, то открываем другое
        login(request, user)
        return redirect("userprofile:profile_pk", pk=user.pk)

    # возвращаем ошибку если ты хуй знает кто
    return render(
        request,
        "userprofile/login.html",
        {"error": "Неверный логин или пароль"}
    )

class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = "userprofile/registration.htmL"
    success_url = reverse_lazy("userprofile:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)

        return response

def logout_view(request: HttpRequest):
    logout(request)
    return redirect("userprofile:login")


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    template_name = "userprofile/profile_update.html"
    model = Profile
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("userprofile:profile")

    def test_func(self):
        obj = super().get_object()
        return self.request.user.id == obj.user_id