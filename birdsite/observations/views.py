from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from birdlib.models import Bird
from .models import Observations


class CreateObservationView(LoginRequiredMixin, CreateView):
    model = Observations
    fields = [
        'bird',
        'region',
        'date',
        'reconciliation',
        'image',
        'gender',
    ]
    success_url = reverse_lazy('observations:list')
    extra_context = {
        'birds': Bird.objects.all(),
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.save()
        return super(CreateObservationView, self).form_valid(form)



class ListObservationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.GET.get("sort") == 'old':
            sort = 'date'
        else:
            sort = '-date'

        if request.GET.get("search"):
            observations = Observations.objects.filter(bird__name__icontains=request.GET.get("search")).order_by(sort)
        else:
            observations = Observations.objects.all().order_by(sort)

        context = {
            'observations': observations,
            'sort': request.GET.get("sort"),
            'search': request.GET.get("search"),
        }
        return render(request, 'observations/list_observation.html', context=context)

class DetailObservationView(DetailView):
    model = Observations
    context_object_name = 'observation'