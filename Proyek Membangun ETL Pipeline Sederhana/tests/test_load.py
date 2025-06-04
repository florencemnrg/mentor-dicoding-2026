import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from etl.load import save_data_with_retry

class TestLoad(unittest.TestCase):

    @patch('pandas.DataFrame.to_sql')
    @patch('etl.load.create_engine')
    def test_save_data_success_first_try(self, mock_create_engine, mock_to_sql):
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_create_engine.return_value = mock_engine

        df = pd.DataFrame({'a': [1, 2]})

        # Simulasi to_sql sukses (tidak error)
        mock_to_sql.return_value = None

        try:
            save_data_with_retry(df, mock_engine, 'test_table', max_retries=3)
        except Exception:
            self.fail("save_data_with_retry raised Exception unexpectedly!")

        mock_to_sql.assert_called_once_with('test_table', con=mock_conn, if_exists='replace', index=False)

    @patch('pandas.DataFrame.to_sql')
    @patch('etl.load.create_engine')
    def test_save_data_retry_and_fail(self, mock_create_engine, mock_to_sql):
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_create_engine.return_value = mock_engine

        df = pd.DataFrame({'a': [1, 2]})

        # Simulasi to_sql error selalu dilempar
        mock_to_sql.side_effect = Exception("DB error")

        with self.assertRaises(Exception) as context:
            save_data_with_retry(df, mock_engine, 'test_table', max_retries=3)

        self.assertIn("DB error", str(context.exception))
        self.assertEqual(mock_to_sql.call_count, 3)  # harus dipanggil 3 kali

if __name__ == '__main__':
    unittest.main()
