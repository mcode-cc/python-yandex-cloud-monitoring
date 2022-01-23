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

    _mon0 = Monitoring(
        credentials={
            "service_account_key": {
                "service_account_id": SERVICE_ACCOUNT_ID,
                "id": SERVICE_ACCOUNT_KEY_ID,
                "private_key": open(os.path.join(os.path.dirname(__file__), "private.key"), "rb").read().decode()
            },
            "cloudId": CLOUD_ID,
            "folderId": FOLDER_ID
        }
    )
    _mon1 = Monitoring(
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

    #DGAUGE: Числовой показатель. Задается дробным числом.
    #IGAUGE: Числовой показатель. Задается целым числом.
    #COUNTER: Счетчик.
    #RATE: Производная.

    _ptns = time.process_time_ns()
    _tns = time.time_ns()
    for n in range(100):
        with Chrono(_mon1, labels={"with": "workers"}, mul=1):
            test_metrics(_mon0, n)
    print((time.process_time_ns() - _ptns) / 10 ** 9, (time.time_ns() - _tns) / 10 ** 9)

    # 0.122077 0.758518  elements=100, period = 10, workers = 0 (default)
    # 1.05552 65.05855 elements=1, period = 10, workers = 0
    # ~ 0.045114 0.043375 elements=100, period = 10, workers = 1 with multiprocessing

