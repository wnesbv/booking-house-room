
import django.dispatch

likes_enabled_test = django.dispatch.Signal()
can_vote_test = django.dispatch.Signal()

# signal that is sent when an object is liked
object_liked = django.dispatch.Signal()
