from django.urls import path
from .views import HomePage, BashSandbox, PowershellSandbox, ZshTerminal, BashTerminal, PowershellTerminal, powershell_checklist_update, bash_checklist_update

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path('bash-sandbox/', BashSandbox.as_view(), name='bash_sandbox'),
    path('powershell-sandbox/', PowershellSandbox.as_view(), name='powershell_sandbox'),
    path('zsh-terminal/', ZshTerminal.as_view(), name='zsh_terminal'),
    path('bash-terminal/', BashTerminal.as_view(), name='bash_terminal'),
    path('powershell-terminal/', PowershellTerminal.as_view(), name='powershell_terminal'),
    path("powershell-terminal/checklist-update/", powershell_checklist_update, name="powershell_checklist_update"),
    path("bash-terminal/checklist-update/", bash_checklist_update, name="bash_checklist_update"),
]
