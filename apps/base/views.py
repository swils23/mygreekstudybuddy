import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .tasks import get_user_id
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from celery.result import AsyncResult


class IndexView(generic.TemplateView):
    template_name = "index.html"


def http_500(request):
    raise Exception


def http_404(request):
    return render(request, "404.html")


@method_decorator(csrf_exempt, name="dispatch")
class TriggerGetUserIDView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        gs_email = data.get("gs_email")
        gs_password = data.get("gs_password")
        task = get_user_id.delay(gs_email, gs_password)
        return JsonResponse({"task_id": task.id})


class GetTaskResultView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get("task_id")
        task = AsyncResult(task_id)
        if task.ready():
            return JsonResponse({"result": task.result})
        else:
            return JsonResponse({"status": "pending"})
