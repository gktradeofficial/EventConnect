from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )

    business_name = models.CharField(max_length=200)
    
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150)
    service_area = models.CharField(max_length=300, blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class ProviderService(models.Model):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='provider_services'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='providers'
    )

    starting_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.provider.business_name} - {self.service.name}"


class Package(models.Model):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='packages'
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.business_name} - {self.name}"


class PortfolioItem(models.Model):

    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='portfolio'
    )

    title = models.CharField(max_length=200)
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES
    )

    media_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Availability(models.Model):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='availability'
    )

    date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.business_name} - {self.date}"


class Enquiry(models.Model):

    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate Event'),
        ('engagement', 'Engagement'),
        ('other', 'Other'),
    ]

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPES
    )

    event_date = models.DateField(
        null=True,
        blank=True
    )

    event_location = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer.username} → {self.provider.business_name}"

class Review(models.Model):

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.provider.business_name} - {self.rating}"