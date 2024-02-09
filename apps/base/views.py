from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "index.html"


def http_500(request):
    raise Exception


def http_404(request):
    return render(request, "404.html")
