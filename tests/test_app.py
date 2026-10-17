"""API regression checks using the actual trained model."""
from unittest import TestCase, main
from unittest.mock import patch

from app import app


class PredictionTests(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_prediction(self):
        response = self.client.post('/api/predict', json={'temperature_c': 30, 'humidity_percent': 70, 'wind_speed_ms': 2})
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.json['pm25'], 32.3, delta=.1)

    def test_invalid_values(self):
        for value in (None, '30', True, float('nan'), float('inf'), 101, -1):
            response = self.client.post('/api/predict', json={'temperature_c': 30, 'humidity_percent': value, 'wind_speed_ms': 2})
            self.assertEqual(response.status_code, 400)

    def test_non_object(self):
        self.assertEqual(self.client.post('/api/predict', json=[]).status_code, 400)
        self.assertEqual(self.client.post('/api/predict', data='bad').status_code, 400)

    def test_extrapolation_and_negative_result(self):
        response = self.client.post('/api/predict', json={'temperature_c': 60, 'humidity_percent': 100, 'wind_speed_ms': 60})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json['pm25'])
        self.assertLess(response.json['raw_prediction'], 0)
        self.assertTrue(response.json['warnings'])

    def test_missing_model(self):
        with patch('app.load_bundle', return_value=None):
            self.assertEqual(self.client.post('/api/predict', json={}).status_code, 503)
            self.assertEqual(self.client.get('/').status_code, 200)

    def test_pages(self):
        for url in ('/', '/static/style.css', '/static/app.js', '/evaluation.png'):
            self.assertEqual(self.client.get(url).status_code, 200)


if __name__ == '__main__':
    main()
