from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.find_professionals,
        name='find_professionals'
    ),

    path(
        'dashboard/',
        views.professional_dashboard,
        name='professional_dashboard'
    ),

    path(
        'dashboard/services/add/',
        views.add_service,
        name='add_service'
    ),

    path(
        'dashboard/packages/add/',
        views.add_package,
        name='add_package'
    ),

    path(
        'dashboard/portfolio/add/',
        views.add_portfolio,
        name='add_portfolio'
    ),

    path(
        'dashboard/availability/add/',
        views.add_availability,
        name='add_availability'
    ),

    path(
        'dashboard/enquiries/<int:enquiry_id>/read/',
        views.mark_enquiry_read,
        name='mark_enquiry_read'
    ),

    path(
        '<int:provider_id>/',
        views.professional_detail,
        name='professional_detail'
    ),

    path(
        '<int:provider_id>/contact/',
        views.contact_professional,
        name='contact_professional'
    ),

    path(
        'dashboard/profile-image/',
        views.update_profile_image,
        name='update_profile_image'
    ),

    path(
        'dashboard/edit-profile/',
        views.edit_professional_profile,
        name='edit_professional_profile'
    ),

    path(
        'dashboard/portfolio/<int:portfolio_id>/delete/',
        views.delete_portfolio,
        name='delete_portfolio'
    ),

    path(
        'dashboard/package/<int:package_id>/delete/',
        views.delete_package,
        name='delete_package'
    ),

    path(
        'dashboard/package/<int:package_id>/edit/',
        views.edit_package,
        name='edit_package'
    ),
    path(
        'dashboard/enquiry/<int:enquiry_id>/read/',
        views.mark_enquiry_read,
        name='mark_enquiry_read'
    ),

    path(
        'services/<int:service_id>/edit/',
        views.edit_service,
        name='edit_service'
    ),

    path(
        'services/<int:service_id>/delete/',
        views.delete_service,
        name='delete_service'
    ),

    path(
        'portfolio/<int:portfolio_id>/edit/',
        views.edit_portfolio,
        name='edit_portfolio'
    ),

    path(
        'availability/<int:availability_id>/edit/',
        views.edit_availability,
        name='edit_availability'
    ),

    path(
        'availability/<int:availability_id>/delete/',
        views.delete_availability,
        name='delete_availability'
    ),

    path(
        'portfolio/<int:portfolio_id>/edit/',
        views.edit_portfolio,
        name='edit_portfolio'
),

    path(
        'portfolio/<int:portfolio_id>/delete/',
        views.delete_portfolio,
        name='delete_portfolio'
),

]