"""Test skeleton.py."""
from dataclasses import dataclass
from pathlib import Path

import pytest

import friendly_parakeet
from friendly_parakeet import (
    CircuitFunction,
    State,
    cli,
    known_functions,
    main,
    parse_args,
    parse_circuit,
    parse_input,
    parse_key_value_line,
    resolve_circuits,
)


@pytest.mark.parametrize("true_value", ["yes", "1", "True", "true"])
def test_cast_to_bool_true(true_value):
    assert State.parse(true_value).value is True


@pytest.mark.parametrize("false_value", ["no", "0", "False", "false"])
def test_cast_to_bool_false(false_value):
    assert State.parse(false_value).value is False


@pytest.mark.parametrize("none_value", ["x", "X"])
def test_cast_to_bool_none(none_value):
    assert State.parse(none_value).value is None


@pytest.mark.parametrize("raises_value", ["is not valid", "more junk"])
def test_cast_to_bool_raises(raises_value):
    with pytest.raises(ValueError):  # noqa: PT011
        State.parse(raises_value)


input_text_1 = """\
in1 = [0, 1, 1]
in2 = [1, 0, 1]
in3 = [1, 1, 1]"""

input_text_x = """\
in1 = [0, 1, X]
in2 = [X, X, 1]
in3 = [X, 1, 1]"""

circuit_text = """\
out1 = and2(out4, in2)
out2 = or2(out1, out3)
out3 = and2(in1, in3)
out4 = inv(in1)"""

output_1 = """\
out1 = [1, 0, 0]
out2 = [1, 1, 1]
out3 = [0, 1, 1]
out4 = [1, 0, 0]"""

output_x = """\
out1 = [X, 0, X]
out2 = [X, 1, X]
out3 = [0, 1, X]
out4 = [1, 0, X]"""


def test_parse_input():
    assert parse_input(input_text_1) == {
        "in1": [State(False), State(True), State(True)],
        "in2": [State(True), State(False), State(True)],
        "in3": [State(True), State(True), State(True)],
    }


def test_parse_circuit():
    assert parse_circuit(circuit_text) == [
        ("out1", CircuitFunction("and2", ["out4", "in2"])),
        ("out2", CircuitFunction("or2", ["out1", "out3"])),
        ("out3", CircuitFunction("and2", ["in1", "in3"])),
        ("out4", CircuitFunction("inv", ["in1"])),
    ]


def test_parse_key_value_line():
    assert parse_key_value_line("a = b") == ("a", "b")


def test_parse_key_value_line_raises():
    with pytest.raises(ValueError):  # noqa: PT011
        parse_key_value_line("a = b = c")


def test_circuit_function_raises():
    with pytest.raises(ValueError):  # noqa: PT011
        CircuitFunction.parse("asdfasdfaf, asdfaf)")


@pytest.mark.parametrize(
    ("in_val", "out_val"),
    [
        (None, None),
        (False, False),
        (True, True),
        (State(True), True),
        (State(False), False),
        (State(None), None),
        ("x", None),
        ("X", None),
        ("1", True),
        ("0", False),
    ],
)
def test_state_parse(in_val, out_val):
    assert State.parse(in_val) == State(out_val)


@pytest.mark.parametrize(
    ("in_val", "out_val"),
    [
        (True, False),
        (False, True),
        (None, None),
    ],
)
def test_state_invert(in_val, out_val):
    assert ~State(in_val) == State(out_val)


@pytest.mark.parametrize(
    ("in_1", "in_2", "out_val"),
    [
        (False, False, False),
        (False, True, False),
        (True, False, False),
        (True, True, True),
        (False, None, False),
        (None, False, False),
        (True, None, None),
        (None, True, None),
        (None, None, None),
    ],
)
def test_state_and(in_1, in_2, out_val):
    assert State(in_1) & State(in_2) == State(out_val)


@pytest.mark.parametrize(
    ("in_1", "in_2", "out_val"),
    [
        (False, False, False),
        (False, True, True),
        (True, False, True),
        (True, True, True),
        (False, None, None),
        (None, False, None),
        (True, None, True),
        (None, True, True),
        (None, None, None),
    ],
)
def test_state_or(in_1, in_2, out_val):
    assert State(in_1) | State(in_2) == State(out_val)


@pytest.mark.parametrize(
    ("in_state", "output"),
    [
        (
            [State(True), State(True), State(True)],
            [State(False), State(False), State(False)],
        ),
        (
            [State(False), State(False), State(False)],
            [State(True), State(True), State(True)],
        ),
        (
            [State(True), State(False), State(True)],
            [State(False), State(True), State(False)],
        ),
        (
            [State(False), State(True), State(False)],
            [State(True), State(False), State(True)],
        ),
    ],
)
def test_inv(in_state, output):
    assert known_functions["inv"](in_state) == output


def test_resolve_circuit_1():
    assert resolve_circuits(parse_input(input_text_1), parse_circuit(circuit_text)) == [
        ("out1", [State(True), State(False), State(False)]),
        ("out2", [State(True), State(True), State(True)]),
        ("out3", [State(False), State(True), State(True)]),
        ("out4", [State(True), State(False), State(False)]),
    ]


def test_resolve_circuit_x():
    assert resolve_circuits(parse_input(input_text_x), parse_circuit(circuit_text)) == [
        ("out1", [State(None), State(False), State(None)]),
        ("out2", [State(None), State(True), State(None)]),
        ("out3", [State(False), State(True), State(None)]),
        ("out4", [State(True), State(False), State(None)]),
    ]


def test_resolve_circuit_circle():
    with pytest.raises(ValueError):  # noqa: PT011
        resolve_circuits(
            {},
            [
                ("out1", CircuitFunction("inv", ["out2"])),
                ("out2", CircuitFunction("inv", ["out1"])),
            ],
        )


@pytest.mark.parametrize(
    ("input_text", "output_text"), [(input_text_1, output_1), (input_text_x, output_x)]
)
def test_main(input_text, output_text):
    assert main(input_text, circuit_text) == output_text


@dataclass
class FakeArgs:
    """Fake arguments class."""

    input_f: Path
    circuit_f: Path


@pytest.mark.parametrize(
    ("input_text", "circuit_t", "output"),
    [
        (input_text_1, circuit_text, output_1),
        (input_text_x, circuit_text, output_x),
    ],
)
def test_input_parser_files(
    input_text, circuit_t, output, tmp_path, monkeypatch, capsys
):
    input_file = tmp_path / "input.txt"
    input_file.write_text(input_text)
    circuit_file = tmp_path / "circuit.txt"
    circuit_file.write_text(circuit_t)

    monkeypatch.setattr(
        friendly_parakeet, "parse_args", lambda x: FakeArgs(input_file, circuit_file)
    )
    capsys.readouterr()
    cli()
    out = capsys.readouterr()

    assert out.out == output + "\n"


def test_parse_args():
    args = parse_args(["input.txt", "circuit.txt"])
    assert args.input_f == Path("input.txt")
    assert args.circuit_f == Path("circuit.txt")
