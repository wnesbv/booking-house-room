

from django import forms
import django_filters
from .models import GHInfo


class GuestHouseFilter(django_filters.FilterSet):
    code_g_f = django_filters.MultipleChoiceFilter(
        field_name="code_g_f",
        choices=(
            ("01|one|gallery|filter", "01|one|gallery|filter"),
            ("02|two|gallery|filter", "02|two|gallery|filter"),
            ("03|three|gallery|filter", "03|three|gallery|filter"),
            ("04|four|gallery|filter", "04|four|gallery|filter"),
            ("05|five|gallery|filter", "05|five|gallery|filter"),
        ),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = GHInfo
        fields = ["code_g_f"]
