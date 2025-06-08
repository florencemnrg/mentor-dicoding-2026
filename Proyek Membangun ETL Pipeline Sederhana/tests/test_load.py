import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

# Import the new function from the correct module
from etl.load_postgresql import save_to_postgresql_with_retry

class TestLoad(unittest.TestCase):

    @patch('pandas.DataFrame.to_sql')
    def test_save_data_success_first_try(self, mock_to_sql):
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn


        df = pd.DataFrame({'a': [1, 2]})

        # Simulate successful to_sql call (no error)
        mock_to_sql.return_value = None

        try:
            save_to_postgresql_with_retry(df, mock_engine, 'test_table', max_retries=3)
        except Exception:
            self.fail("save_to_postgresql_with_retry raised Exception unexpectedly!")

        mock_to_sql.assert_called_once_with('test_table', con=mock_conn, if_exists='replace', index=False)

    @patch('pandas.DataFrame.to_sql')
    def test_save_data_retry_and_fail(self, mock_to_sql):
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        df = pd.DataFrame({'a': [1, 2]})

        # Simulate to_sql always raising exception
        mock_to_sql.side_effect = Exception("DB error")

        with self.assertRaises(Exception) as context:
            save_to_postgresql_with_retry(df, mock_engine, 'test_table', max_retries=3)

        self.assertIn("DB error", str(context.exception))
        self.assertEqual(mock_to_sql.call_count, 3)  # must be called 3 times

if __name__ == '__main__':
    unittest.main()
