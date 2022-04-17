import unittest
import app

class TestApp(unittest.TestCase):
    """ This class run the tests for the App Module """
    def test_validate_qty(self):
        """ This method runs the test  for the validate_qty function in the App Module """
        self.assertEqual(app.validate_qty("100"), 100)
        self.assertEqual(app.validate_qty("-1"), 10)
        self.assertEqual(app.validate_qty("d"), 10)

if __name__ == "__main__":
    unittest.main()