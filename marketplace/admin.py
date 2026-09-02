from django.contrib import admin

from .models import (
    Category,
    Service,
    ProviderProfile,
    ProviderService,
    Package,
    PortfolioItem,
    Availability,
    Enquiry,
    Review,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = (
        'business_name',
        'user',
        'location',
        'experience_years',
        'is_verified',
        'is_active',
    )

    list_filter = (
        'is_verified',
        'is_active',
        'location',
    )

    search_fields = (
        'business_name',
        'location',
        'user__username',
    )


@admin.register(ProviderService)
class ProviderServiceAdmin(admin.ModelAdmin):
    list_display = (
        'provider',
        'service',
        'starting_price',
    )

    list_filter = ('service',)

    search_fields = (
        'provider__business_name',
        'service__name',
    )


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'provider',
        'price',
        'is_active',
    )

    list_filter = ('is_active',)

    search_fields = (
        'name',
        'provider__business_name',
    )


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'provider',
        'media_type',
        'created_at',
    )

    list_filter = ('media_type',)

    search_fields = (
        'title',
        'provider__business_name',
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        'provider',
        'date',
        'is_available',
    )

    list_filter = ('is_available', 'date')

    search_fields = (
        'provider__business_name',
    )


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        'customer',
        'provider',
        'event_type',
        'event_date',
        'is_read',
        'created_at',
    )

    list_filter = (
        'event_type',
        'is_read',
    )

    search_fields = (
        'customer__username',
        'provider__business_name',
        'event_location',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'provider',
        'customer',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'provider__business_name',
        'customer__username',
        'comment',
    )