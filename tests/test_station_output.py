"""Station names must not crash Windows consoles using a legacy encoding."""
import io
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from scripts import find_stations


class StationOutputTests(TestCase):
    def test_emoji_on_legacy_console(self):
        response = Mock(status_code=200)
        response.json.return_value = {'results': [{
            'id': 1, 'name': 'Station 🏠', 'sensors': [
                {'id': 2, 'parameter': {'name': 'pm25', 'units': 'µg/m³'}}]}]}
        buffer = io.BytesIO()
        console = io.TextIOWrapper(buffer, encoding='cp874')
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(find_stations, 'ROOT', Path(folder)), \
                 patch.object(find_stations, 'load_dotenv'), \
                 patch.dict('os.environ', {'OPENAQ_API_KEY': 'test-key'}), \
                 patch.object(find_stations.requests, 'get', return_value=response), \
                 patch('sys.stdout', console):
                self.assertEqual(find_stations.main(), 0)
            console.flush()
            self.assertIn('Station 🏠', buffer.getvalue().decode('utf-8'))
            self.assertTrue((Path(folder) / 'data/station_candidates.csv').exists())
