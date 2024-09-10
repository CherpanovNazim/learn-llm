import re

from langchain.document_loaders.parsers.language.python import PythonSegmenter
import unittest


def contains_class(code: str) -> bool:
    """Checks if class definition is within the code"""

    return "\nclass " in "\n" + code.lstrip(" \n")


def contains_function(code: str) -> bool:
    """Checks if function definition is within the code"""

    return "\ndef " in "\n" + code.lstrip(" \n")


def extract_code(
    text,
    extract_only_funcs_and_classes: bool = True,
    remove_starting_code: bool = True
    ):

    code_blocks = []
    pattern = r'```python\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        code_blocks.append(match)
    
    code = "\n\n".join(code_blocks)

    if remove_starting_code or extract_only_funcs_and_classes:
            code = code.split("if __name__")[0]
            code = code.split("unittest.main(")[0]

    code = code.rstrip(" \n")

    return code


def wrap_code(code: str) -> str:
    """Wraping the code as a markdown python block"""

    return f"\n```python\n{code}\n```"


class FakeStream:
    """Suppresses output to console"""

    @staticmethod
    def write(m):
        pass

    @staticmethod
    def flush():
        pass


def run_unit_tests(
    code_with_unit_tests: str,
    scope_namespace: dict,
) -> (bool, list[str]):
    """Runs unit tests and returns the list of issues descriptions"""

    # Load the code with unit tests
    try:
        exec(code_with_unit_tests, scope_namespace)
        tests_were_runnable = True
    except Exception as ex:
        # If tests contain compile error, then repeat that error several times,
        #   to guarantee that we start with a high count of issues,
        #   since we are minimizing the number of the issues during the bug-fix.
        tests_were_runnable = False
        return tests_were_runnable, [str(ex)]

    # Extract tests class name
    class_name_pattern = r"class\s+(\w+)\("
    class_name_match = re.search(class_name_pattern, code_with_unit_tests)
    unit_tests_class_name = class_name_match.group(1)

    # Get unit tests class
    unit_tests_class = scope_namespace[unit_tests_class_name]

    # Run the unit tests
    test_suite = unittest.TestLoader().loadTestsFromTestCase(unit_tests_class)
    unit_tests_results = unittest.TextTestRunner(
        verbosity=0,
        stream=FakeStream,
    ).run(test_suite)

    # Prepare the list of unit tests issues
    unit_tests_issues = unit_tests_results.errors + unit_tests_results.failures

    # Cast all issue parts as strings
    unit_tests_issues = [
        [
            str(issue_part).strip(" \n")
            for issue_part in issue_tuple
        ]
        for issue_tuple in unit_tests_issues
    ]
    # Shortening too long texts
    unit_tests_issues = [
        (
            header + "\n"
            + (description if len(description) <= 512 else f"{description[:512]}...")
        )
        for header, description in unit_tests_issues
    ]

    return tests_were_runnable, unit_tests_issues
