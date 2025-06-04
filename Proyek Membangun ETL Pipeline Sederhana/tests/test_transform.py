import unittest
import numpy as np
from etl.transform import convert_price_to_rupiah, clean_rating

class TestTransform(unittest.TestCase):

    def test_convert_price_to_rupiah_valid(self):
        self.assertEqual(convert_price_to_rupiah("$10"), 160000)
        self.assertEqual(convert_price_to_rupiah("$0"), 0)
        self.assertAlmostEqual(convert_price_to_rupiah("$123.45"), 123.45 * 16000)

    def test_convert_price_to_rupiah_invalid(self):
        self.assertTrue(np.isnan(convert_price_to_rupiah("Price Unavailable")))
        self.assertTrue(np.isnan(convert_price_to_rupiah(None)))
        self.assertTrue(np.isnan(convert_price_to_rupiah("abc")))

    def test_clean_rating_valid(self):
        self.assertEqual(clean_rating("⭐ 4.9 / 5"), 4.9)
        self.assertEqual(clean_rating("5"), 5.0)
        self.assertEqual(clean_rating("4.2 stars"), 4.2)

    def test_clean_rating_invalid(self):
        self.assertTrue(np.isnan(clean_rating("Invalid Rating / 5")))
        self.assertTrue(np.isnan(clean_rating("Not Rated")))
        self.assertTrue(np.isnan(clean_rating(None)))

if __name__ == '__main__':
    unittest.main()
