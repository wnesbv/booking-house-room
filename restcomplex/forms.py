

from django import forms
from .models import *


class ReservationForm(forms.Form):
    start_date = forms.DateTimeField(input_formats=["%d/%m/%Y, %H:%M"])
    end_date = forms.DateTimeField(input_formats=["%d/%m/%Y, %H:%M"])


class FeedbackFormRest(forms.ModelForm):
    feed = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form_input", "placeholder": "Write Here",}
        )
    )

    class Meta:
        model = FeedbackRest
        fields = ["feed"]
