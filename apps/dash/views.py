import json
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import generic

from ..base.utils.gs import GreekStudy
from .forms import GreekStudyAccountSetupForm
from .models import GreekStudyUser


class GreekStudyIndexView(LoginRequiredMixin, generic.TemplateView):
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

    def post(self, request, *args, **kwargs):
        hours = request.POST.get("hours")

        if hours and hours.isdigit() and (0 < int(hours)):
            # if the user is a superuser, no limits
            if request.user.is_superuser:
                # random mins to avoid detection
                GreekStudy().post_hours(
                    sentUserID=request.user.gs_userID, hours=int(hours), minutes=random.randint(0, 19)  # nosec
                )
            elif request.user.hours >= int(hours):
                request.user.hours -= int(hours)
                request.user.save()
                # random mins to avoid detection
                GreekStudy().post_hours(
                    sentUserID=request.user.gs_userID, hours=int(hours), minutes=random.randint(0, 19)  # nosec
                )

        return redirect("hours")


class GreekStudyUsersView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dash/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gs = GreekStudy()
        gs.login(email=self.request.user.gs_email, password=self.request.user.gs_password)
        context["users"] = gs.get_users()

        for user in context["users"]:
            GreekStudyUser.objects.get_or_create(
                gs_id=user["id"], first=user["first"].strip(), last=user["last"].strip()
            )

        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("dash_index")
        return super().dispatch(request, *args, **kwargs)


class TaskGetUserIDView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        gs_email = data.get("gs_email")
        gs_password = data.get("gs_password")

        if not gs_email or not gs_password:
            return "Email and password are required."
        gs = GreekStudy()
        gs.login(email=gs_email, password=gs_password)
        return JsonResponse({"result": gs.get_user_id()})
