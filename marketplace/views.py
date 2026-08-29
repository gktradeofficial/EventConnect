from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import (ProviderProfile, Service, Enquiry, 
    ProviderService, Package, PortfolioItem,
    Availability 
)

def find_professionals(request):

    providers = ProviderProfile.objects.filter(
        is_active=True,
        is_verified=True
    ).prefetch_related(
        'provider_services__service',
        'packages',
        'portfolio'
    )

    search = request.GET.get('search', '')
    location = request.GET.get('location', '')
    service = request.GET.get('service', '')

    if search:
        providers = providers.filter(
            Q(business_name__icontains=search) |
            Q(description__icontains=search)
        )

    if location:
        providers = providers.filter(
            location__icontains=location
        )

    if service:
        providers = providers.filter(
            provider_services__service__id=service
        )

    services = Service.objects.filter(
        is_active=True
    )

    return render(
        request,
        'marketplace/professionals.html',
        {
            'providers': providers.distinct(),
            'services': services,
            'search': search,
            'location': location,
            'selected_service': service,
        }
    )
def professional_detail(request, provider_id):

    provider = ProviderProfile.objects.prefetch_related(
        'provider_services__service',
        'packages',
        'portfolio'
    ).get(
        id=provider_id,
        is_active=True,
        is_verified=True
    )

    return render(
        request,
        'marketplace/professional_detail.html',
        {
            'provider': provider,
            'services': provider.provider_services.all(),
            'packages': provider.packages.filter(
                is_active=True
            ),
            'portfolio': provider.portfolio.all()
        }
    )


@login_required
def contact_professional(request, provider_id):

    provider = get_object_or_404(
        ProviderProfile,
        id=provider_id,
        is_active=True,
        is_verified=True
    )

    if request.user == provider.user:
        return redirect(
            'professional_detail',
            provider_id=provider.id
        )

    if request.method == 'POST':

        Enquiry.objects.create(
            provider=provider,
            customer=request.user,
            event_type=request.POST.get('event_type'),
            event_date=request.POST.get('event_date') or None,
            event_location=request.POST.get('event_location'),
            phone=request.POST.get('phone'),
            message=request.POST.get('message'),
        )

        return render(
            request,
            'marketplace/enquiry_success.html',
            {'provider': provider}
        )

    return render(
        request,
        'marketplace/contact_professional.html',
        {
            'provider': provider,
        }
    )


@login_required
def professional_dashboard(request):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    enquiries = provider.enquiries.select_related(
        'customer'
    ).order_by(
        '-created_at'
    )

    unread_enquiries = enquiries.filter(
        is_read=False
    ).count()

    services = provider.provider_services.select_related(
        'service'
    )

    packages = provider.packages.filter(
        is_active=True
    )

    portfolio = provider.portfolio.order_by(
        '-created_at'
    )

    availability = provider.availability.order_by(
        'date'
    )

    return render(
        request,
        'marketplace/professional_dashboard.html',
        {
            'provider': provider,
            'enquiries': enquiries,
            'unread_enquiries': unread_enquiries,
            'services': services,
            'packages': packages,
            'portfolio': portfolio,
            'availability': availability,
        }
    )


@login_required
def add_service(request):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == 'POST':

        service_id = request.POST.get('service')
        starting_price = request.POST.get('starting_price')

        service = get_object_or_404(
            Service,
            id=service_id,
            is_active=True
        )

        ProviderService.objects.create(
            provider=provider,
            service=service,
            starting_price=starting_price
        )

        return redirect('professional_dashboard')

    services = Service.objects.filter(
        is_active=True
    ).select_related('category')

    return render(
        request,
        'marketplace/add_service.html',
        {
            'provider': provider,
            'services': services,
        }
    )


@login_required
def add_package(request):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == 'POST':

        Package.objects.create(
            provider=provider,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            is_active=True
        )

        return redirect('professional_dashboard')

    return render(
        request,
        'marketplace/add_package.html'
    )


@login_required
def add_portfolio(request):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title')
        media_type = request.POST.get('media_type')
        description = request.POST.get('description')

        image = request.FILES.get('image')
        media_url = request.POST.get('media_url')

        PortfolioItem.objects.create(
            provider=provider,
            title=request.POST.get('title'),
            media_type=request.POST.get('media_type'),
            media_url=request.POST.get('media_url'),
            description=request.POST.get('description')
        )

        return redirect('professional_dashboard')

    return render(
        request,
        'marketplace/add_portfolio.html'
    )


@login_required
def add_availability(request):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == 'POST':

        Availability.objects.update_or_create(
            provider=provider,
            date=request.POST.get('date'),
            defaults={
                'is_available':
                    request.POST.get('is_available') == 'true'
            }
        )

        return redirect('professional_dashboard')

    return render(
        request,
        'marketplace/add_availability.html'
    )


@login_required
def edit_professional_profile(request):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == 'POST':

        provider.business_name = request.POST.get(
            'business_name'
        )

        provider.description = request.POST.get(
            'description'
        )

        provider.location = request.POST.get(
            'location'
        )

        provider.service_area = request.POST.get(
            'service_area'
        )

        provider.experience_years = (
            request.POST.get('experience_years') or 0
        )

        profile_image = request.FILES.get(
            'profile_image'
        )

        if profile_image:
            provider.profile_image = profile_image

        provider.save()

        return redirect(
            'professional_dashboard'
        )

    return render(
        request,
        'marketplace/edit_professional_profile.html',
        {
            'provider': provider
        }
    )



@login_required
def update_profile_image(request):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == 'POST':

        image = request.FILES.get('profile_image')

        if image:
            provider.profile_image = image
            provider.save()

        return redirect(
            'professional_dashboard'
        )

    return redirect(
        'professional_dashboard'
    )


@login_required
def delete_portfolio(request, portfolio_id):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    portfolio = get_object_or_404(
        PortfolioItem,
        id=portfolio_id,
        provider=provider
    )

    if request.method == 'POST':
        portfolio.delete()

    return redirect(
        'professional_dashboard'
    )


@login_required
def delete_package(request, package_id):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    package = get_object_or_404(
        Package,
        id=package_id,
        provider=provider
    )

    if request.method == 'POST':
        package.delete()

    return redirect(
        'professional_dashboard'
    )


@login_required
def edit_package(request, package_id):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    package = get_object_or_404(
        Package,
        id=package_id,
        provider=provider
    )

    if request.method == 'POST':

        package.name = request.POST.get('name')
        package.description = request.POST.get('description')
        package.price = request.POST.get('price')

        package.is_active = (
            request.POST.get('is_active') == 'on'
        )

        package.save()

        return redirect(
            'professional_dashboard'
        )

    return render(
        request,
        'marketplace/edit_package.html',
        {
            'package': package
        }
    )


@login_required
def mark_enquiry_read(request, enquiry_id):

    provider = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    enquiry = get_object_or_404(
        Enquiry,
        id=enquiry_id,
        provider=provider
    )

    if request.method == 'POST':
        enquiry.is_read = True
        enquiry.save(update_fields=['is_read'])

    return redirect('professional_dashboard')