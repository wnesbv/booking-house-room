

from django import forms
from main.models import Feedback


class ReservationForm(forms.Form):
    start_date = forms.DateTimeField(input_formats=["%d/%m/%Y, %H:%M"])
    end_date = forms.DateTimeField(input_formats=["%d/%m/%Y, %H:%M"])

    # ...
    number_rooms = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form_input",
                "placeholder": "number rooms",
            }
        )
    )
    number_children = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form_input",
                "placeholder": "number children",
            }
        )
    )
    number_adults = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form_input",
                "placeholder": "number adults",
            }
        )
    )


class FeedbackForm(forms.ModelForm):
    feed = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form_input",
                "placeholder": "Write Here",
            }
        )
    )

    class Meta:
        model = Feedback
        fields = ["feed"]
