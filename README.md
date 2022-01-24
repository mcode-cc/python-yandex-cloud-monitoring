[![PyPI](https://img.shields.io/pypi/v/python-yandex-cloud-monitoring)](https://pypi.org/project/python-yandex-cloud-monitoring/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-yandex-cloud-monitoring)
[![PyPI - License](https://img.shields.io/pypi/l/python-yandex-cloud-monitoring)](https://github.com/mcode-cc/python-yandex-cloud-monitoring/blob/main/LICENSE)


# Python Client for Yandex Cloud Monitoring
 


## Installation

    pip3 install python-yandex-cloud-monitoring

[Getting started with Yandex Monitoring](https://cloud.yandex.com/en/docs/monitoring/quickstart)

## Credentials

Service Account Keys only ...

[Access management](https://cloud.yandex.com/en/docs/monitoring/security/)

### Service Account Keys


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
    #  Numeric indicator. Specified as a fractional number.
    metrics.dgauge(
        "temperature", 
        random.random(), 
        ts=datetime.datetime.now(datetime.timezone.utc), 
        labels={"building": "office", "room": "openspace"}
    )
    #  Counter.
    metrics.counter("counter", n, labels={"building": "office", "room": "openspace"})
    #  Numeric indicator. Specified as an integer.
    metrics.igauge("number", n, labels={"building": "office", "room": "openspace"})
    #  Derivative.
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


```python
from pyclm.monitoring import Monitoring, Chrono

metrics = Monitoring()

with Chrono(metrics, name="elapsed", labels={"measured": "calculation"}, mul=10**9):
    # ... measured calculation ...

```

_name_ - Name of the metric. The default value is **elapsed**. Additional metric **process_{name}** sum of the kernel and user-space CPU time.

_mul_ - Process time for profiling default as seconds mul = 10^9 .. nanoseconds mul = 1

_labels_ - Metric labels as _key:value_ pairs.