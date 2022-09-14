from datetime import datetime, timedelta, timezone
from pprint import pprint
import random
import uuid

import requests

token = '<METRONOME API TOKEN HERE>'
user = '<METRONOME CUSTOMER ID / INGEST ALIAS HERE>'

def ingest(events):
    remainder = events
    while len(remainder) > 0:
        pprint(remainder[:100])

        response = requests.post(
            "https://api.metronome.com/v1/ingest",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=remainder[:100]
        )

        if response.status_code != 200:
            print(f'ERROR {response.status_code}: {response.text}')
        remainder = remainder[100:]

events = []
t = datetime.now(timezone.utc) - timedelta(days=33)
while t < datetime.now(timezone.utc):
    def append_event(event_type, properties):
        events.append({
            "transaction_id": uuid.uuid4().hex,
            "timestamp": t.isoformat(),
            "event_type": event_type,
            "customer_id": user,
            "properties": properties,
        })
    def random_monthly_target(n):
        return random.randint(90*n // 720, 110*n // 720) / 100

    # append_event("some_event_type", {
    #     "gigabytes": random_monthly_target(2_500_000),
    # })

    t += timedelta(hours=1)

ingest(events)
