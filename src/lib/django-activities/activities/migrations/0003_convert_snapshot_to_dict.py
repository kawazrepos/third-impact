# -*- coding: utf-8 -*-
import pickle
from django.db import migrations
from ..registry import registry


def convert_snapshots(apps, schema_editor):
    Activity = apps.get_model('activities', 'Activity')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    for activity in Activity.objects.all():
        content_type = ContentType.objects.get(pk=activity.content_type_id)
        activity._content_object = content_type.get_object_fot_this_type(
            pk=activity.object_id
        )
        mediator = registry.get(activity)
        snapshot = pickle.loads(activity._snapshot)
        if isinstance(snapshot, dict):
            # Model instalce => dictionary instance convertion was already
            # applied. Skip.
            continue
        snapshot_dict = mediator.serialize_snapshot(snapshot)
        activity._snapshot = pickle.dumps(snapshot_dict)
        activity.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('activities', '0002_test'),
    ]

    operations = [
        migrations.RunPython(convert_snapshots),
    ]
