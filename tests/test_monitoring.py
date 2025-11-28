import time
import unittest
from unittest import mock

from requests import exceptions as req_exc

from pyclm.monitoring import Monitoring, Ingestion, PM


class MonitoringTests(unittest.TestCase):
    @staticmethod
    def _credentials():
        return {
            "service_account_key": {
                "service_account_id": "id",
                "id": "key-id",
                "private_key": "PEM",
            },
            "cloudId": "cloud",
            "folderId": "folder",
        }

    def _ingestion_with_timeout(self):
        credentials = self._credentials()
        ingestion = Ingestion(
            credentials,
            "group",
            "resource_type",
            "resource_id",
            elements=2,
            period=60,
            timeout=(1, 1),
        )
        ingestion.metrics.append({"name": "m1", "value": 1})
        return ingestion

    def test_monitoring_init(self):
        monitor = Monitoring(credentials=self._credentials())
        self.assertIsInstance(monitor, Monitoring)

    def test_ingestion_buffer_and_write_single_process(self):
        credentials = self._credentials()

        ingestion = Ingestion(
            credentials,
            "group",
            "resource_type",
            "resource_id",
            elements=2,
            period=60,
            timeout=None,
        )

        def _fake_post(url, json=None, headers=None, timeout=None):
            class Response:
                def __init__(self, status_code, body):
                    self.status_code = status_code
                    self._body = body

                def json(self):
                    return self._body

            from pyclm.monitoring import API_IAM, API_MONITORING

            if url == API_IAM:
                return Response(200, {"iamToken": "valid-iam-token"})
            if url.startswith(API_MONITORING):
                written = len(json.get("metrics", [])) if json else 0
                return Response(200, {"writtenMetricsCount": written})
            return Response(500, {})

        with mock.patch("pyclm.monitoring.jwt.encode", return_value="jwt-token"), \
                mock.patch("pyclm.monitoring.requests.post", side_effect=_fake_post):
            self.assertEqual(len(ingestion.metrics), 0)
            ingestion({"name": "m1", "value": 1})
            self.assertEqual(len(ingestion.metrics), 1)

            ingestion({"name": "m2", "value": 2})
            self.assertEqual(len(ingestion.metrics), 0)

    def test_monitoring_single_process_client(self):
        monitor = Monitoring(
            credentials=self._credentials(),
            elements=10,
            period=60,
            workers=0,
            timeout=None,
        )
        monitor.dgauge("metric", 1.0)
        self.assertTrue(len(monitor._send.metrics) >= 1)
        monitor._send.finalize(len(monitor._send.metrics))

    def test_monitoring_parallel_workers(self):
        # workers>0 -> PM with separate process, ensure no errors and clean shutdown
        monitor = Monitoring(
            credentials=self._credentials(),
            elements=1000000,
            period=60,
            workers=1,
            timeout=None,
        )
        monitor.dgauge("metric", 1.0)
        # finalize child process gracefully
        if isinstance(monitor._send, PM):
            monitor._send.finalize(0)

    def test_ingestion_write_connection_error(self):
        ingestion = self._ingestion_with_timeout()
        with mock.patch.object(Ingestion, "_write", side_effect=req_exc.ConnectionError):
            with self.assertRaises(req_exc.ConnectionError):
                ingestion._write()
        ingestion.finalize(len(ingestion.metrics))

    def test_ingestion_write_connect_timeout(self):
        ingestion = self._ingestion_with_timeout()
        with mock.patch.object(Ingestion, "_write", side_effect=req_exc.ConnectTimeout):
            with self.assertRaises(req_exc.ConnectTimeout):
                ingestion._write()
        ingestion.finalize(len(ingestion.metrics))

    def test_ingestion_write_read_timeout(self):
        ingestion = self._ingestion_with_timeout()
        with mock.patch.object(Ingestion, "_write", side_effect=req_exc.ReadTimeout):
            with self.assertRaises(req_exc.ReadTimeout):
                ingestion._write()
        ingestion.finalize(len(ingestion.metrics))


if __name__ == "__main__":
    unittest.main()
