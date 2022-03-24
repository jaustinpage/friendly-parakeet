"""Parse logs."""

import re
from collections import defaultdict
from typing import Dict, List, Tuple


def parse_chunk(chunk: str) -> Tuple[str, int]:
    """Parse a chunk for rule name and error count.

    :param chunk: The chunk of logs to process.
    :returns: The rule name and count of errors found.
    :raises ValueError: if a rule was not found.
    """
    lines = chunk.splitlines()
    if not chunk.startswith("Rule"):
        raise ValueError('Chunk must start with "Rule"')
    chunk_name = lines.pop(0)
    count = 0
    for line in lines:
        if line.startswith("ERROR:"):
            count += 1
    return chunk_name, count


def process_chunks(chunks: List[str]) -> Dict[str, int]:
    """Process list of chunks.

    :param chunks: A list of chunks of logs.
    :returns: A dictionary of rules and counts of error.
    """
    results = defaultdict(lambda: 0)
    for chunk in chunks:
        try:
            chunk_name, count = parse_chunk(chunk)
            results[chunk_name] = results[chunk_name] + count
        except ValueError:
            pass
    return results


def parse_logs(logs: str) -> str:
    """Count rule errors in logs.

    :param logs: The logs to process.
    :returns: String formatted output of rule counts.
    """
    rule_chunks = re.split(r"\W(?=Rule)", logs)
    found_rules = process_chunks(rule_chunks)
    results = []
    for key, val in found_rules.items():
        if val == 1:
            results.append(f"{key.strip()} {val} ERROR")
        else:
            results.append(f"{key.strip()} {val} ERRORS")
    return "\n".join(results)
