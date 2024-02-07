from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import GreekStudyAccountSetupForm

from ..base.utils.gs import GreekStudy


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dash/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GreekStudyAccountSetupView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dash/greek_study_account_setup.html"

    def get_initial(self):
        initial = {}
        initial["gs_email"] = self.request.user.gs_email
        initial["gs_password"] = self.request.user.gs_password
        initial["gs_userID"] = self.request.user.gs_userID
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GreekStudyAccountSetupForm(initial=self.get_initial())
        return context

    def post(self, request, *args, **kwargs):
        form = GreekStudyAccountSetupForm(request.POST)

        if form.is_valid():
            request.user.gs_email = form.cleaned_data["gs_email"]
            request.user.gs_password = form.cleaned_data["gs_password"]
            request.user.gs_userID = form.cleaned_data["gs_userID"]
            request.user.save()
            return redirect("dash_index")
        print(form)
        print(str(form.errors) + "#####################")
        return render(request, self.template_name, {"form": form})


class GreekStudyHoursView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dash/hours.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gs = GreekStudy()
        gs.login(email=self.request.user.gs_email, password=self.request.user.gs_password)
        gs.get_users()
        user = gs.get_user(self.request.user.gs_userID)
        context["user"] = user
        if user:
            context["hours"] = user["hours"]
        else:
            context["hours"] = "unknown"
        return context
