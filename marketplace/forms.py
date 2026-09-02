from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment',
        ]

        widgets = {

            'rating': forms.Select(
                choices=[
                    (5, '★★★★★  Excellent'),
                    (4, '★★★★☆  Very Good'),
                    (3, '★★★☆☆  Good'),
                    (2, '★★☆☆☆  Average'),
                    (1, '★☆☆☆☆  Poor'),
                ],
                attrs={
                    'class': 'form-control'
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Share your experience...',
                    'rows': 4
                }
            ),
        }