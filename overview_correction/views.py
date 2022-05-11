
from typing import List

from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic.edit import FormMixin, FormView
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
)

from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag

from overview_correction.filter import GuestHouseFilter
from overview_correction.models import GHInfo, GHRooms, Comment, Reply, LikeDislike
from overview_correction.forms import GHCreateForm, RoomsCreateForm,  CommentForm, EmailPostForm

# def about(request):
#     return render(request=request, template_name="overview_correction/about.html")

# ...
class GHListView(ListView):
    paginate_by = 2
    template_name = "overview_correction/list_detail/gh_list.html"

    # ...
    login_user_id = None
    is_login_user = False

    def get(self, request, *args, **kwargs):
        self.login_user_id = request.user.id
        self.is_login_user = request.user.is_authenticated
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = GHInfo.published.all()
        tag_slug = self.kwargs.get("tag_slug")
        query = self.request.GET.get("query")
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        if query:
            search_vector = SearchVector("name", weight="A") + SearchVector(
                "specifications", weight="B"
            )
            search_query = SearchQuery(query)
            queryset = (
                GHInfo.published.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.3)
                .order_by("-rank")
            )
        return queryset

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            if request.user.is_authenticated:
                if request.POST.get("action"):
                    post_id = request.POST.get("post_id")
                    user_id = request.POST.get("user_id")
                    action = request.POST.get("action")
                    if action == "like":
                        LikeDislike.objects.update_or_create_like(post_id, user_id)
                    elif action == "unlike":
                        LikeDislike.objects.delete_after_unlike(post_id, user_id)
                    elif action == "dislike":
                        LikeDislike.objects.update_or_create_dislike(post_id, user_id)
                    elif action == "undislike":
                        LikeDislike.objects.delete_after_undislike(post_id, user_id)
                    else:
                        return None
                    count_likes = LikeDislike.objects.filter(
                        post__id=post_id, rating_action=1
                    ).count()
                    count_dislikes = LikeDislike.objects.filter(
                        post__id=post_id, rating_action=0
                    ).count()
                    return JsonResponse(
                        {"likes": count_likes, "dislikes": count_dislikes}
                    )
                return None
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["is_login_user"] = self.is_login_user
        if self.login_user_id is not None:
            context["login_user_id"] = self.login_user_id

        context["tag"] = self.kwargs.get("tag_slug")
        context["query"] = self.request.GET.get("query")
        return context


class GHDetailView(FormMixin, DetailView):
    form_class = CommentForm
    queryset = GHInfo.published.all()
    template_name = "overview_correction/list_detail/gh_details.html"

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    # ...
    login_user_id = None
    is_login_user = False

    def get(self, request, *args, **kwargs):
        self.login_user_id = request.user.id
        self.is_login_user = request.user.is_authenticated
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            if request.user.is_authenticated:
                if request.POST.get("action"):
                    post_id = request.POST.get("post_id")
                    user_id = request.POST.get("user_id")
                    action = request.POST.get("action")
                    if action == "like":
                        LikeDislike.objects.update_or_create_like(post_id, user_id)
                    elif action == "unlike":
                        LikeDislike.objects.delete_after_unlike(post_id, user_id)
                    elif action == "dislike":
                        LikeDislike.objects.update_or_create_dislike(post_id, user_id)
                    elif action == "undislike":
                        LikeDislike.objects.delete_after_undislike(post_id, user_id)
                    else:
                        return None
                    count_likes = LikeDislike.objects.filter(
                        post__id=post_id, rating_action=1
                    ).count()
                    count_dislikes = LikeDislike.objects.filter(
                        post__id=post_id, rating_action=0
                    ).count()
                    return JsonResponse(
                        {"likes": count_likes, "dislikes": count_dislikes}
                    )
            else:
                return None

        form = self.get_form()
        if form.is_valid():
            form.instance.user = self.request.user
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.save()
            return self.form_valid(form)
        return self.delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(
            GHInfo,
            slug=self.kwargs.get("slug"),
        )
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = GHInfo.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-modified_at"
        )[:4]
        comments = Comment.objects.filter(post=post, active=True)

        context["is_login_user"] = self.is_login_user
        if self.login_user_id is not None:
            context["login_user_id"] = self.login_user_id

        context["similar_posts"] = similar_posts
        context["comments"] = comments
        context["form"] = self.get_form()
        return context


# ...GH
class UserGHListView(ListView):
    model = GHInfo
    paginate_by = 2
    context_object_name = "gh_user_list"
    template_name = "overview_correction/list_detail/gh_user_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = GHInfo.objects.filter(author=user)
        return queryset

class UserGHDetailView(DetailView):
    model = GHInfo
    template_name = "overview_correction/list_detail/gh_user_detail.html"

    def get_queryset(self):
        user = self.request.user
        queryset = GHInfo.objects.filter(author=user)
        return queryset


# ...Rooms
class UserRoomsListView(ListView):
    model = GHRooms
    paginate_by = 2
    context_object_name = "room_user_list"
    template_name = "overview_correction/list_detail/rooms_user_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = GHRooms.objects.filter(author=user)
        return queryset

class UserRoomsDetailView(DetailView):
    model = GHRooms
    template_name = "overview_correction/list_detail/room_user_detail.html"

    def get_queryset(self):
        user = self.request.user
        queryset = GHRooms.objects.filter(author=user)
        return queryset


# ... User GH
class UserGHCreateView(LoginRequiredMixin, FormView):
    template_name = "overview_correction/form/gh_form.html"
    form_class = GHCreateForm
    success_url = reverse_lazy("overview_correction:gh_user_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        post.save()

        # Send Email
        got_message = form.cleaned_data
        post_url = reverse_lazy("overview_correction:gh_detail", args=[post.slug])
        subject = f"{got_message['name']}"
        message = (
            f"Publication at: {post_url}\n\n"
            f"Publication (name): {got_message['name']}"
        )
        from_email = "web_site@gmail.com"
        recipient_list = [
            "mail@gmail.com",
        ]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = GHCreateForm(request.POST, request.FILES)
        messages.success(
            request,
            "the post passes verification",
        )
        return super().post({"form": form}, request, *args, **kwargs)

class UserGHUpdate(LoginRequiredMixin, UserPassesTestMixin, FormView):
    model = GHInfo
    form_class = GHCreateForm
    template_name = "overview_correction/form/gh_update_form.html"
    success_url = "/gh-user-list/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        form.save()

        # Send Email
        got_message = form.cleaned_data
        post_url = reverse_lazy("overview_correction:gh_detail", args=[post.slug])
        subject = f"{got_message['name']}"
        message = (
            f"Publication at: {post_url}\n\n"
            f"Publication (name): {got_message['name']}"
        )
        from_email = "web_site@gmail.com"
        recipient_list = [
            "mail@gmail.com",
        ]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = GHCreateForm(request.POST, request.FILES)
        messages.success(
            request,
            "the post passes verification",
        )
        return super().post({"form": form}, request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserGHDelete(LoginRequiredMixin, DeleteView):
    model = GHInfo
    template_name = "overview_correction/form/gh_delete.html"
    success_url = "/gh-user-list/"


# ... User Room
class UserRoomCreateView(LoginRequiredMixin, FormView):
    template_name = "overview_correction/form/gh_form.html"
    form_class = RoomsCreateForm
    success_url = reverse_lazy("overview_correction:rooms_user_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        post.save()

        # Send Email
        got_message = form.cleaned_data
        post_url = reverse_lazy("overview_correction:room_detail", args=[post.slug])
        subject = f"{got_message['name']}"
        message = (
            f"Publication at: {post_url}\n\n"
            f"Publication (name): {got_message['name']}"
        )
        from_email = "web_site@gmail.com"
        recipient_list = [
            "mail@gmail.com",
        ]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = RoomsCreateForm(request.POST, request.FILES)
        messages.success(
            request,
            "the post passes verification",
        )
        return super().post({"form": form}, request, *args, **kwargs)

class UserRoomUpdate(LoginRequiredMixin, UserPassesTestMixin, FormView):
    model = GHRooms
    form_class = RoomsCreateForm
    template_name = "overview_correction/form/room_update_form.html"
    success_url = "/rooms-user-list/"
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

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        form.save()

        # Send Email
        got_message = form.cleaned_data
        post_url = reverse_lazy("overview_correction:room_detail", args=[post.slug])
        subject = f"{got_message['name']}"
        message = (
            f"Publication at: {post_url}\n\n"
            f"Publication (name): {got_message['name']}"
        )
        from_email = "web_site@gmail.com"
        recipient_list = [
            "mail@gmail.com",
        ]
        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = RoomsCreateForm(request.POST, request.FILES)
        messages.success(
            request,
            "the post passes verification",
        )
        return super().post({"form": form}, request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserRoomDelete(LoginRequiredMixin, DeleteView):
    model = GHRooms
    template_name = "overview_correction/form/room_delete.html"
    success_url = "/rooms-user-list/"


class PostShareView(FormView):
    form_class = EmailPostForm
    template_name = "overview_correction/gh_share.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(GHInfo, id=self.kwargs.get("post_id"))
        context["sent"] = False
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        goo_message = form.cleaned_data
        post = context["post"]
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        user = self.request.user
        subject = f"{user} recommends you read {post.name}"
        message = (
            f"Read - {post.name} at {post_url}\n\n"
            f"from - {user}\n\n"
            f"COMMENTS: {goo_message['comments']}"
        )

        from_email = "web@gmail.com"
        recipient_list = [goo_message["to"]]
        send_mail(subject, message, from_email, recipient_list)

        context["sent"] = True
        context["form"] = form
        return self.render_to_response(context)


# ...
class SliderGHListView(ListView):
    model = GHInfo
    template_name = "user/filter_gh.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = GuestHouseFilter(
            self.request.GET, queryset=GHInfo.objects.all()
        )
        return context

class SliderGHDetailView(DetailView):
    model = GHInfo
    template_name = "user/gh_description.html"


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post.slug
    messages.success(
        request,
        "comment deleted",
    )
    if comment.user == request.user:
        comment.delete()
    return redirect("overview_correction:post_detail", slug=post)

class ReplyView(View):
    def post(self, request, **kwargs):
        post_comment_pk = self.kwargs["pk"]
        post_comment = Comment.objects.get(pk=post_comment_pk)
        reply_comment = post_comment.post.pk
        reply_comment = request.POST["reply_comment"]
        Reply.objects.create(
            comment=post_comment, user=request.user, reply=reply_comment
        )

        return redirect(request.META.get("HTTP_REFERER"), **kwargs)

@login_required
def rply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    post = reply.comment.post.slug
    messages.success(
        request,
        "the response to the comment has been deleted",
    )
    if reply.user == request.user:
        reply.delete()
    return redirect("overview_correction:post_detail", slug=post)
