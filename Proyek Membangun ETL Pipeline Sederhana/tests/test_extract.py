import unittest
from bs4 import BeautifulSoup
from etl.extract import extract_product_data

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.html = """
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
            <div class="price-container"><span class="price">$123.45</span></div>
            <p>Rating: ⭐ 4.8 / 5</p>
            <p>5 Colors</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.prod_div = self.soup.find("div", class_="product-details")

    def test_extract_product_data(self):
        data = extract_product_data(self.prod_div)
        self.assertEqual(data['Product Name'], "Test Product")
        self.assertEqual(data['Price'], "$123.45")
        self.assertEqual(data['Rating'], "⭐ 4.8 / 5")
        self.assertEqual(data['Size'], "M")
        self.assertEqual(data['Gender'], "Unisex")
        self.assertEqual(data['Color'], 5)

if __name__ == '__main__':
    unittest.main()
