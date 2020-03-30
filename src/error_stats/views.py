from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.views import View
# from .forms import Error_StatForm
from .models import Error_Stat

# Create your views here.
from django.views.generic import (
    DetailView,
    ListView
)

class ErrorStatListView(View):
    template_name = 'error_stats/error_stat_list.html'
    queryset = Error_Stat.objects.all()

    def get_queryset(self):
        return self.queryset
    
    def get(self, request, id = None, *args, **kwargs):
        context = {
            "object_list": self.get_queryset()
        }
        return render(request, self.template_name, context)

class ErrorStatDetailView(View):
    template_name = 'error_stats/error_stat_detail.html'
    query = Error_Stat.objects.all()

    def get(self, request, id = None, *args, **kwargs):
        context = {}
        if id is not None:
            obj = get_object_or_404(Error_Stat,id=id)
            context['object'] = obj
        return render(request, self.template_name, context)

