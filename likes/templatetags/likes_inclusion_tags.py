
from django import template
from likes.utils import can_vote, likes_enabled

register = template.Library()

@register.inclusion_tag("likes/inclusion_tags/likes_extender.html", takes_context=True)
def likes(context, obj, template=None):
    if template is None:
        template = "likes/inclusion_tags/likes.html"
    request = context["request"]

    try:
        model_name = obj._meta.model_name
    except AttributeError:
        model_name = obj._meta.module_name
    context.update(
        {
            "template": template,
            "content_obj": obj,
            "likes_enabled": likes_enabled(obj, request),
            "can_vote": can_vote(obj, request.user, request),
            "content_type": "-".join((obj._meta.app_label, model_name)),
        }
    )
    return context
