
from django import forms
from .models import GHInfo, GHRooms, Comment


class GHCreateForm(forms.ModelForm):
    class Meta:
        model = GHInfo
        fields = [
            "name",
            "figuratively",
            "specifications",
            "functionality_gh",
            "number_rooms",
            "number_children",
            "number_adults",
            "tags",
            "status",
            "image",
            "image_2",
            "image_3",
            "image_4",
            "image_5",
        ]


class RoomsCreateForm(forms.ModelForm):
    class Meta:
        model = GHRooms
        fields = [
            "name",
            "guesthouse",
            "functionality_rm",
            "room_services",
            "room_type",
            "room_specifications",
            "price",
            "img_logo",
            "image",
            "image_2",
            "image_3",
            "image_4",
            "image_5",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["room_specifications"].widget.attrs.update({"class": "special"})


class EmailPostForm(forms.ModelForm):
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)

    class Meta:
        model = Comment
        fields = ["to", "comments"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
