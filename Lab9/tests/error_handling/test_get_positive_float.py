import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from inventory_manager import get_positive_float


class TestGetPositiveFloat(unittest.TestCase):

    def test_asks_again_until_value_is_valid(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            value = get_positive_float("Price: ")

        self.assertEqual(value, 12.5)
        self.assertIn("Please enter a valid number, e.g. 12.50", output.getvalue())
        self.assertIn("Please enter a number greater than zero.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
