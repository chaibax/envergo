import logging

from django.db import transaction

from config.celery_app import app
from envergo.geodata.models import Map
from envergo.geodata.utils import extract_shapefile

logger = logging.getLogger(__name__)


@app.task(bind=True)
def process_shapefile_map(task, map_id):
    """Send a Mattermost notification to confirm the evaluation request."""

    logger.info(f"Starting import on map {map_id}")

    map = Map.objects.get(pk=map_id)

    with transaction.atomic():
        map.zones.all().delete()
        extract_shapefile(map, map.file)
