
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.models import User

from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("report")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("report")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True


@login_required
def report_view(request):
    context = {
        "total_users": User.objects.count(),
        "current_user": request.user,
        "users": User.objects.order_by("-date_joined")[:10],
    }

    return render(request, "accounts/report.html", context)


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")
