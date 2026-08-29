from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from marketplace.models import Enquiry

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully!"
            )

            return redirect('home')

    else:
        form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if hasattr(user, 'provider_profile'):
                return redirect('professional_dashboard')

            return redirect('customer_dashboard')

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        'accounts/login.html'
    )


@login_required
def customer_dashboard(request):

    enquiries = Enquiry.objects.filter(
        customer=request.user
    ).select_related(
        'provider'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'accounts/customer_dashboard.html',
        {
            'enquiries': enquiries,
        }
    )




def user_logout(request):

    logout(request)

    return redirect('home')

