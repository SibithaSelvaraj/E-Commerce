from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-select rounded-lg'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border rounded-lg',
            'rows': '4',
            'placeholder': 'Write your review here...'
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']