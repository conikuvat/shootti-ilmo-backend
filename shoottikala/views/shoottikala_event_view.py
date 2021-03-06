from django.shortcuts import get_object_or_404, render

from ..forms import CosplayerForm, PhotographerForm
from ..models import Event, Cosplayer, Photographer


def shoottikala_event_view(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    is_authenticated = request.user.is_authenticated()

    if is_authenticated:
        own_photographer = Photographer.objects.filter(event=event, user=request.user).first()
        is_photographer = own_photographer is not None
        if is_photographer:
            own_photographer_form = PhotographerForm(instance=own_photographer)
        else:
            own_photographer_form = None

        photographers = Photographer.objects.filter(event=event, is_active=True).exclude(user=request.user)

        own_cosplayers = Cosplayer.objects.filter(event=event, user=request.user)
        own_cosplayers_with_forms = [(cosplayer, CosplayerForm(instance=cosplayer)) for cosplayer in own_cosplayers]
        first_own_cosplayer = own_cosplayers.first()

        cosplayers_looking = Cosplayer.objects.filter(event=event, is_active=True).exclude(user=request.user)
    else:
        own_photographer = None
        is_photographer = False
        own_photographer_form = None
        photographers = Photographer.objects.none()
        own_cosplayers = Cosplayer.objects.none()
        own_cosplayers_with_forms = []
        first_own_cosplayer = None
        cosplayers_looking = Cosplayer.objects.none()

    is_cosplayer = own_cosplayers.exists()

    vars = dict(
        cosplayers_looking=cosplayers_looking,
        event=event,
        is_cosplayer=is_cosplayer,
        is_photographer=is_photographer,
        first_own_cosplayer=first_own_cosplayer,
        own_cosplayers=own_cosplayers,
        own_cosplayers_with_forms=own_cosplayers_with_forms,
        own_photographer_form=own_photographer_form,
        own_photographer=own_photographer,
        photographers=photographers,
        show_cosplayer_fragment=event.is_active and is_cosplayer,
        show_inactive_fragment=not event.is_active,
        show_login_fragment=event.is_active and not is_authenticated,
        show_photographer_fragment=event.is_active and is_photographer,
        show_welcome_fragment=event.is_active and is_authenticated and not (is_cosplayer or is_photographer),
    )

    return render(request, 'shoottikala_event_view.jade', vars)
