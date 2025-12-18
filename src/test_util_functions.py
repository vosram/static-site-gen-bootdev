import unittest

from util_functions import replace_static_to_public_paths


class TestUtilFuncs(unittest.TestCase):
    def test_replace_base_dir(self):
        output0 = replace_static_to_public_paths("static")
        output1 = replace_static_to_public_paths("static/images")
        output2 = replace_static_to_public_paths("static/images/graphics")
        output3 = replace_static_to_public_paths("static/assets")
        self.assertEqual(output0, "public")
        self.assertEqual(output1, "public/images")
        self.assertEqual(output2, "public/images/graphics")
        self.assertEqual(output3, "public/assets")


if __name__ == "__main__":
    unittest.main()
