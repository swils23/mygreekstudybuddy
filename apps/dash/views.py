from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import GreekStudyAccountSetupForm


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dash/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GreekStudyAccountSetupView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dash/greek_study_account_setup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GreekStudyAccountSetupForm()
        return context

    def post(self, request, *args, **kwargs):
        form = GreekStudyAccountSetupForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
        return super().get(request, *args, **kwargs)


