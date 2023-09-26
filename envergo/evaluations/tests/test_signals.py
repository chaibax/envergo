import pytest
from anymail.signals import AnymailTrackingEvent, tracking
from django.utils import timezone

from envergo.evaluations.models import RecipientStatus
from envergo.evaluations.tests.factories import RegulatoryNoticeLogFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def event():
    data = {
        "event_type": "opened",
        "recipient": "example@domain.com",
        "message_id": "test_message_id",
        "timestamp": timezone.now(),
    }
    event = AnymailTrackingEvent(**data)
    return event


def test_webhook_event_catching(event):
    statuses_qs = RecipientStatus.objects.all()
    assert statuses_qs.count() == 0

    log = RegulatoryNoticeLogFactory(message_id="test_message_id")
    tracking.send(sender=None, event=event, esp_name="sendinblue")
    assert statuses_qs.count() == 1

    log_event = statuses_qs[0]
    assert log_event.recipient == event.recipient
    assert log_event.regulatory_notice_log == log