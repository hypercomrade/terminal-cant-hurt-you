from django.urls import path
from .views import HomePage, ZshTerminal, BashTerminal, PowershellTerminal

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path('zsh-terminal/', ZshTerminal.as_view(), name='zsh_terminal'),
    path('bash-terminal/', BashTerminal.as_view(), name='bash_terminal'),
    path('powershell-terminal/', PowershellTerminal.as_view(), name='powershell_terminal'),
]
