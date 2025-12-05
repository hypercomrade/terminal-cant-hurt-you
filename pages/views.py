from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from account.models import PowerShellChecklist, BashChecklist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.


class HomePage(TemplateView):
    template_name = "home.html"


class BashSandbox(TemplateView):
    template_name = "bash_sandbox.html"


class PowershellSandbox(TemplateView):
    template_name = "powershell_sandbox.html"


class ZshTerminal(TemplateView):
    template_name = "zsh_terminal.html"


@method_decorator(login_required, name='dispatch')
class BashTerminal(TemplateView):
    template_name = "bash_terminal.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        checklist, _ = BashChecklist.objects.get_or_create(
            user=self.request.user
        )
        ctx["checklist"] = checklist
        return ctx


@method_decorator(login_required, name='dispatch')
class PowershellTerminal(TemplateView):
    template_name = "powershell_terminal.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        checklist, _ = PowerShellChecklist.objects.get_or_create(
            user=self.request.user
        )
        ctx["checklist"] = checklist
        return ctx


@login_required
@require_POST
@csrf_exempt
def powershell_checklist_update(request):
    print("Debug: Received PowerShell checklist update request", request.body)
    data = json.loads(request.body.decode("utf-8"))
    key = data.get("key")
    value = bool(data.get("value", True))

    checklist, _ = PowerShellChecklist.objects.get_or_create(user=request.user)

    allowed_fields = {
        "list_files",
        "system_info",
        "move_location",
        "read_write",
        "manipulate_files",
        "navigate",
    }

    if key not in allowed_fields:
        return JsonResponse({"ok": False, "error": "Invalid field"}, status=400)

    setattr(checklist, key, value)
    checklist.save()
    return JsonResponse({"success": True})


@login_required
@require_POST
@csrf_exempt
def bash_checklist_update(request):
    print("Debug: Received Bash checklist update request", request.body)
    data = json.loads(request.body.decode("utf-8"))
    key = data.get("key")
    value = bool(data.get("value", True))

    checklist, _ = BashChecklist.objects.get_or_create(user=request.user)

    allowed_fields = {
        "list_files",
        "system_info",
        "move_location",
        "read_write",
        "manipulate_files",
        "navigate",
    }

    if key not in allowed_fields:
        return JsonResponse({"ok": False, "error": "Invalid field"}, status=400)

    setattr(checklist, key, value)
    checklist.save()
    return JsonResponse({"success": True})
