from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string

from ..models import Event, Photographer, Cosplayer
from ..forms import PhotographerForm, CosplayerForm, MessageForm
from ..utils import initialize_form
from ..exceptions import AccessDenied


@login_required
def shoottikala_send_message_view(request, event_slug, photographer_id, cosplayer_id):
    event = get_object_or_404(Event, slug=event_slug)
    photographer = get_object_or_404(Photographer, event=event, id=int(photographer_id))
    cosplayer = get_object_or_404(Cosplayer, event=event, id=int(cosplayer_id))

    if request.user == photographer.user:
        sender = photographer
        recipient = cosplayer
    elif request.user == cosplayer.user:
        sender = cosplayer
        recipient = photographer
    else:
        raise AccessDenied()

    photographer_form = PhotographerForm(instance=photographer)
    cosplayer_form = CosplayerForm(instance=cosplayer)
    message_form = initialize_form(MessageForm, request)

    if request.method == 'POST':
        if message_form.is_valid():
            message_context = dict(
                cosplayer=cosplayer,
                photographer=photographer,
                sender=sender,
                message_text=message_form.cleaned_data['message_text'],
            )

            body = render_to_string('shoottikala_message_template.eml', message_context, request=request)
            subject = '{event.name}: Photoshoot-ehdotus ({sender.display_name})'.format(event=event, sender=sender)

            if settings.DEBUG:
                print(body)

            EmailMessage(
                subject=subject,
                body=body,
                to=[recipient.user.email],
                reply_to=[sender.user.email],
            ).send()

            messages.success(request, 'Viesti lähetettiin.')

            return redirect('shoottikala_event_view', event.slug)
        else:
            messages.error(request, 'Ole hyvä ja tarkista lomake.')

    vars = dict(
        event=event,
        photographer=photographer,
        cosplayer=cosplayer,
        photographer_form=photographer_form,
        cosplayer_form=cosplayer_form,
        message_form=message_form,
    )

    return render(request, 'shoottikala_send_message_view.jade', vars)