import unittest
from unittest.mock import patch, MagicMock
from app import insert_alert, fetch_alerts

class TestDatabaseOperations(unittest.TestCase):

    @patch('WeatherMonitoring.db.session')
    def test_insert_alert(self, mock_session):
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()

        insert_alert('Weather Warning', 'City Name', 'Severe weather warning for City Name.')

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        print("Test for insert_alert passed!")

    @patch('WeatherMonitoring.db.session')
    def test_fetch_alerts(self, mock_session):
        mock_query = MagicMock()
        mock_query.all.return_value = [
            {'alert_id': 1, 'alert_type': 'Weather Warning', 'city': 'City Name', 'message': 'Severe weather warning.', 'created_at': '2024-10-23'}
        ]
        mock_session.query.return_value = mock_query

        results = fetch_alerts()
        mock_session.query.assert_called_once()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['alert_type'], 'Weather Warning')
        print("Test for fetch_alerts passed!")

if __name__ == '__main__':
    unittest.main()
