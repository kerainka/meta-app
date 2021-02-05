def main():
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meta.settings')

    import django
    django.setup()

main()

from meta.settings import API_KEY, API_URL
from metaapp.models import Psychotherapist, PsychotherapistRaw
from django.utils import timezone
import requests

def fetch_data():
    api_url = 'https://api.airtable.com/v0/' + API_URL
    res = requests.get(api_url, headers={'Authorization' : 'Bearer ' + API_KEY})
    res.raise_for_status()
    return res.json()

def save_raw_data(data):
    r = PsychotherapistRaw(
        parsed_at=timezone.now(),
        raw_data=data)
    r.save()

def sync_to_db(records):
    id_list = []
    for record in records:
        Psychotherapist.objects.update_or_create(
            id=record["id"],
            defaults={
                'name': record["fields"].get("Имя", ''), 
                'methods': record["fields"].get("Методы", []), 
                'photo_url': record["fields"].get("Фотография", [{ 'url': '#' }])[0]["url"],
            })
        id_list.append(record["id"])

    objects_to_delete = Psychotherapist.objects.exclude(pk__in=id_list)
    for object_to_delete in objects_to_delete:
        object_to_delete.delete()

data = fetch_data()
save_raw_data(data)
sync_to_db(data['records'])
