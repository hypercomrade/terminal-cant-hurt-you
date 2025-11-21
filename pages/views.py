from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HomePage(TemplateView):
    template_name = "home.html"
    

class ZshTerminal(TemplateView):
    template_name = "zsh_terminal.html"

class BashTerminal(TemplateView):
    template_name = "bash_terminal.html"

<<<<<<< Updated upstream
class PowershellTerminal(TemplateView):
    template_name = "powershell_terminal.html"

=======
class PowerShell(TemplateView):
    template_name = "powerShell.html"
>>>>>>> Stashed changes

