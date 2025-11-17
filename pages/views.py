from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HomePage(TemplateView):
    template_name = "home.html"
    

class ZshTerminal(TemplateView):
    template_name = "zsh_terminal.html"

class BashTerminal(TemplateView):
    template_name = "bash_terminal.html"


