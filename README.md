[![PyPI](https://img.shields.io/pypi/v/python-yandex-cloud-monitoring)](https://pypi.org/project/python-yandex-cloud-monitoring/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-yandex-cloud-monitoring)
[![PyPI - License](https://img.shields.io/pypi/l/python-yandex-cloud-monitoring)](https://github.com/mcode-cc/python-yandex-cloud-monitoring/blob/main/LICENSE)


# Python Client for Yandex Cloud Monitoring
 
## Supported Python versions

The 0.1.* release line officially supports Python 3.6–3.8 (see `python_requires` and classifiers in `setup.py`). Make sure your dependencies (especially `cryptography`) are installed with versions compatible with your interpreter.


## Installation

    pip3 install python-yandex-cloud-monitoring

[Getting started with Yandex Monitoring](https://cloud.yandex.com/en/docs/monitoring/quickstart)

## Credentials

Service Account Keys only ...

[Access management](https://cloud.yandex.com/en/docs/monitoring/security/)


### Service Account Keys & Roles

For write metrics, add a folder role: _monitoring.editor_

```python
import datetime
import random

from pyclm.monitoring import Monitoring

metrics = Monitoring(
    credentials={
        "service_account_key": {
            "service_account_id": "....",
            "id": "....",
            "private_key": "<PEM>"
        },
        "cloudId": "<CLOUD_ID>",
        "folderId": "<FOLDER_ID>"
    },
    group_id="default",
    resource_type="....", resource_id="....",
    elements=100, period=10, workers=1
)

for n in range(1000):
    #  Numeric value (decimal). It shows the metric value at a certain point in time.
    #  For example, the amount of used RAM
    metrics.dgauge(
        "temperature", 
        random.random(), 
        ts=datetime.datetime.now(datetime.timezone.utc), 
        labels={"building": "office", "room": "openspace"}
    )
    #  Tag. It shows the metric value that increases over time.
    #  For example, the number of days of service continuous running.
    metrics.counter("counter", n, labels={"building": "office", "room": "openspace"})
    #  Numeric value (integer). It shows the metric value at a certain point in time.
    metrics.igauge("number", n, labels={"building": "office", "room": "openspace"})
    #  Derivative value. It shows the change in the metric value over time.
    #  For example, the number of requests per second.
    metrics.rate("rate", random.random(), labels={"building": "office", "room": "openspace"})

```

_credentials.cloudId_ - The ID of the cloud that the resource belongs to.

_credentials.folderId_ - The ID of the folder that the resource belongs to.

_resource_type_ - Resource type, serverless.function, hostname.
Value must match the regular expression ([a-zA-Z][-a-zA-Z0-9_.]{0,63})?.

_resource_id_ - Resource ID, i.e., ID of the function producing metrics.
Value must match the regular expression ([a-zA-Z0-9][-a-zA-Z0-9_.]{0,63})?.

_elements_ - The number of elements before writing, must be in the range 1-100.

_period_ -  Number of seconds to wait for new log entries before writing.

_workers_ - Number of process ingestion.

_timeout_ - Timeouts HTTP requests.

Timeouts can be configured via the `timeout` argument:

```python
from pyclm.monitoring import Monitoring

metrics = Monitoring(
    credentials={...},
    group_id="default",
    resource_type="...",
    resource_id="...",
    elements=100,
    period=10,
    workers=1,
    timeout=(3, 5),  # (connect_timeout, read_timeout) in seconds
)
```

By default, `timeout=(3, 5)` is used for all outgoing HTTP requests (connection timeout 3 seconds, read timeout 5 seconds).
