import logging

from anymail.signals import tracking
from django.db.models import F
from django.dispatch import receiver

from envergo.evaluations.models import RecipientStatus, RegulatoryNoticeLog
from envergo.evaluations.tasks import warn_admin_of_email_error

logger = logging.getLogger(__name__)

# Those are the events we want to receive from the ESP and track
# There is also an order of priority, and the latest status in not
# necessarily the one we want to keep
# E.g if a message is already "clicked", and later the recipient
# opens it again and we receive an "opened" event, we want the status
# to stay "clicked"
TRACKED_EVENTS = ["queued", "delivered", "opened", "clicked"]

# Those are the events that mean the message was not delivered
ERROR_EVENTS = [
    "deferred",
    "rejected",
    "bounced",
    "failed",
]

ALL_EVENTS = TRACKED_EVENTS + ERROR_EVENTS


@receiver(tracking)
def handle_mail_event(sender, event, esp_name, **kwargs):
    event_name = event.event_type
    recipient = event.recipient
    message_id = event.message_id
    timestamp = event.timestamp
    reject_reason = event.reject_reason

    logger.info(f"Received event {event.event_type} for message id {message_id}")
    if event_name not in ALL_EVENTS:
        return

    try:
        regulatory_notice_log = RegulatoryNoticeLog.objects.get(message_id=message_id)
    except RegulatoryNoticeLog.DoesNotExist:
        logger.warning(f"Could not find message id {message_id}")
        return

    logger.info(
        f"Received event {event_name} for {recipient} on notice {regulatory_notice_log.pk}"
    )
    on_error = event_name in ERROR_EVENTS
    warn_of_email_error = False
    status, _created = RecipientStatus.objects.get_or_create(
        regulatory_notice_log=regulatory_notice_log,
        recipient=recipient,
        defaults={
            "status": event_name,
            "latest_status": timestamp,
            "on_error": False,
        },
    )

    status_index = ALL_EVENTS.index(event_name)
    current_status_index = ALL_EVENTS.index(status.status)
    if status_index > current_status_index:
        status.status = event_name
        status.latest_status = timestamp

    if event_name == "opened":
        status.nb_opened = F("nb_opened") + 1
        status.latest_opened = timestamp
    elif event_name == "clicked":
        status.nb_clicked = F("nb_clicked") + 1
        status.latest_clicked = timestamp

    if on_error:
        status.reject_reason = reject_reason
        # We only warn admin if it's the first time we receive an error status
        if not status.on_error:
            warn_of_email_error = True
            status.on_error = True

    status.save()

    if warn_of_email_error:
        warn_admin_of_email_error.delay(status.id)
