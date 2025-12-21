import unittest

from util_functions import replace_static_to_public_paths, extract_title


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

    def test_extract_title(self):
        title1 = extract_title("# My awesome site\n\nHello everyone")
        self.assertEqual(title1, "My awesome site")

    def test_extract_title_after_text(self):
        md = """
some text before heading

# My awesome site

Some paragraph text after
"""
        title1 = extract_title(md)
        self.assertEqual(title1, "My awesome site")

    def test_extract_title_exception(self):
        md = """
This markdown file does not have a title

## there is a secondary heading

but an h2 is not a title
"""
        with self.assertRaises(ValueError):
            title1 = extract_title(md)


if __name__ == "__main__":
    unittest.main()
