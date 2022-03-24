"""Test parse log."""

from friendly_parakeet.parse_log import parse_logs

test_input = """## LOG FILE
Rule Apple:
Line 1 message
Line 2 message
ERROR: Input is wrong
Line 3 message
ERROR: Another wrong input
Rule Peach:
Line 1 message
Line 2 message
Rule Kiwi:
ERROR: Fatal Error
Rule Apple:
ERROR: Input is still wrong
"""

expected_out = """Rule Apple: 3 ERRORS
Rule Peach: 0 ERRORS
Rule Kiwi: 1 ERROR"""


def test_log_parse():
    assert parse_logs(test_input) == expected_out
