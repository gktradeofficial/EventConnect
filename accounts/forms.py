from django import forms
from django.contrib.auth.models import User

from .models import Profile
from marketplace.models import (
    ProviderProfile,
    ProviderService,
    Service,
)


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput
    )

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('professional', 'Professional'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    phone = forms.CharField(
        max_length=20,
        required=True
    )

    location = forms.CharField(
        max_length=100,
        required=True
    )

    business_name = forms.CharField(
        max_length=200,
        required=False
    )

    experience_years = forms.IntegerField(
        min_value=0,
        required=False
    )

    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    service_area = forms.CharField(
        max_length=300,
        required=False
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        required=False
    )

    starting_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'role',
            'phone',
            'location',
            'business_name',
            'experience_years',
            'description',
            'service_area',
            'service',
            'starting_price',
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        role = cleaned_data.get('role')

        if password and password_confirm:

            if password != password_confirm:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        if role == 'professional':

            if not cleaned_data.get('business_name'):
                self.add_error(
                    'business_name',
                    'Business name is required.'
                )

            if not cleaned_data.get('service'):
                self.add_error(
                    'service',
                    'Please select a service.'
                )

            if cleaned_data.get('starting_price') is None:
                self.add_error(
                    'starting_price',
                    'Starting price is required.'
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:

            user.save()

            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data['phone'],
                location=self.cleaned_data['location'],
            )

            if self.cleaned_data['role'] == 'professional':

                provider = ProviderProfile.objects.create(

                    user=user,

                    business_name=self.cleaned_data[
                        'business_name'
                    ],

                    description=self.cleaned_data.get(
                        'description',
                        ''
                    ),

                    location=self.cleaned_data[
                        'location'
                    ],

                    service_area=self.cleaned_data.get(
                        'service_area',
                        ''
                    ),

                    experience_years=self.cleaned_data.get(
                        'experience_years'
                    ) or 0,

                    is_verified=False,

                    is_active=True,
                )

                ProviderService.objects.create(

                    provider=provider,

                    service=self.cleaned_data[
                        'service'
                    ],

                    starting_price=self.cleaned_data[
                        'starting_price'
                    ],
                )

        return user