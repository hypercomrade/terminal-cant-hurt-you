from django.urls import path
<<<<<<< Updated upstream
from .views import HomePage, ZshTerminal, BashTerminal, PowershellTerminal
=======
from .views import HomePage, ZshTerminal, BashTerminal, PowerShell
>>>>>>> Stashed changes

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path('zsh-terminal/', ZshTerminal.as_view(), name='zsh_terminal'),
    path('bash-terminal/', BashTerminal.as_view(), name='bash_terminal'),
<<<<<<< Updated upstream
    path('powershell-terminal/', PowershellTerminal.as_view(), name='powershell_terminal'),
]
=======
    path('powerShell-terminal/', PowerShell.as_view(), name='powerShell_terminal'),
]
>>>>>>> Stashed changes
