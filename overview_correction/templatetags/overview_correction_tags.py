
from django import template
from overview_correction.models import GHInfo, Comment

register = template.Library()

@register.simple_tag
def total_posts():
    return GHInfo.objects.count()
@register.simple_tag
def total_published():
    return GHInfo.published.count()

# ...
@register.simple_tag
def quantity_comments():
    return Comment.objects.count()


@register.inclusion_tag("overview_correction/partials/_latest_posts.html")
def show_latest_posts(count=1):
    latest_posts = GHInfo.published.order_by("-modified_at")[:count]
    return {"latest_posts": latest_posts}

@register.inclusion_tag("overview_correction/partials/_max_commets.html")
def max_commets_posts(count=1):
    max_commets = GHInfo.published.order_by("-gh_comments")[:count]
    return {"max_commets": max_commets}
