from util_functions import (
    copy_static_to_output,
    generate_pages_recursively,
)
import sys


def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    copy_static_to_output("docs")
    generate_pages_recursively("content", "template.html", "docs", basepath)


main()
