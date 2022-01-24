import os
import time
import datetime
import random

from pyclm.monitoring import Monitoring, Chrono


SERVICE_ACCOUNT_ID = os.environ.get("SERVICE_ACCOUNT_ID")
SERVICE_ACCOUNT_KEY_ID = os.environ.get("SERVICE_ACCOUNT_KEY_ID")
FOLDER_ID = os.environ.get("FOLDER_ID")
CLOUD_ID = os.environ.get("CLOUD_ID")


def test_metrics(mon: Monitoring, n):
    _t = datetime.datetime.now(datetime.timezone.utc)
    mon.dgauge("temperature", random.random() * 100, ts=_t, labels={"building": "office", "room": "openspace"})
    mon.counter("number", n, ts=_t, labels={"building": "office", "room": "openspace"})


if __name__ == '__main__':

    _mon = Monitoring(
        credentials={
            "service_account_key": {
                "service_account_id": SERVICE_ACCOUNT_ID,
                "id": SERVICE_ACCOUNT_KEY_ID,
                "private_key": open(os.path.join(os.path.dirname(__file__), "private.key"), "rb").read().decode()
            },
            "cloudId": CLOUD_ID,
            "folderId": FOLDER_ID
        },
        workers=1
    )

    for n in range(1000):
        with Chrono(_mon, labels={"with": "workers"}, mul=10**3):
            test_metrics(_mon, n)
            time.sleep(0.3)
