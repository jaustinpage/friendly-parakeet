"""Skeleton init file."""
import argparse
import sys
from argparse import Namespace
from dataclasses import dataclass
from distutils.util import strtobool
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError  # pragma: no cover
    from importlib.metadata import version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError  # pragma: no cover
    from importlib_metadata import version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "friendly-parakeet"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


@dataclass
class CircuitFunction:
    """A circuit function.

    Represents a circuit function and it's corresponding arguments.
    """

    name: str
    args: List[str]

    @classmethod
    def parse(cls, func_str: str) -> "CircuitFunction":
        """Parse a function call.

        parses a function into a function call.
        :param func_str: The function call string.
        :returns: The Circuit function of the string.
        :raises ValueError: If the parsing of the line does not succeed.
        """
        name_args = func_str.split("(")
        if len(name_args) != 2:
            raise ValueError(
                "Parsing of input line failed. Expecting 1 '(' in: %s", func_str
            )

        func_name = name_args[0].strip()
        args_string = name_args[1].strip().rstrip(")")
        args = [s.strip() for s in args_string.split(",")]
        return cls(func_name, args)


@dataclass
class State:
    """Boolean State of a bit.

    This is special because it also supports a floating state or indeterminate state.
    This state is represented by None.
    """

    value: Optional[bool]

    def __str__(self) -> str:
        """Cast to string.

        :returns: String of State.
        """
        if self.value is None:
            return "X"
        if self.value:
            return "1"
        return "0"

    @classmethod
    def parse(cls, in_str: Optional[Union[str, bool, "State"]]) -> "State":
        """Parse a string into a boolean.

        Also accepts "X" or "x" as a None

        :param in_str: The input string.
        :returns: A boolean.
        """
        if in_str is None:
            return cls(None)
        if isinstance(in_str, cls):
            return in_str
        if isinstance(in_str, bool):
            return cls(in_str)

        in_str = in_str.strip()
        if any(x in in_str for x in ["x", "X"]):
            return cls(None)
        return cls(bool(strtobool(in_str)))

    @classmethod
    def parse_list(cls, list_str: str) -> List["State"]:
        """Parse a list in string form.

        Coerces string of list into list of booleans or None.
        :param list_str: The string version of the list.
        :returns: The parsed list.
        """
        return [
            cls.parse(s) for s in list_str.strip().lstrip("[").rstrip("]").split(",")
        ]

    def __and__(self, other: Union["State", bool, str]) -> "State":
        """Compute and of state.

        :param other: The other state to and with.
        :returns: and of state.
        """
        other = self.parse(other)
        if self.value is None and other.value is None:
            return self.parse(None)
        if self.value is None or other.value is None:
            if self.value or other.value:
                return self.parse(None)
            return self.parse(False)
        return self.parse(self.value and other.value)

    def __or__(self, other: Union["State", bool, str]) -> "State":
        """Compute or of state.

        :param other: The other state to or with.
        :returns: or of new state.
        """
        other = self.parse(other)
        if self.value is None and other.value is None:
            return self.parse(None)
        if self.value is None or other.value is None:
            if self.value or other.value:
                return self.parse(True)
            return self.parse(None)
        return self.parse(self.value or other.value)

    def __invert__(self) -> "State":
        """Invert a state.

        :returns: Inverted state.
        """
        if self.value is None:
            return self.parse(None)
        return self.parse(not self.value)


def parse_key_value_line(
    input_line: str, value_parser: Callable[[str], Any] = None
) -> Tuple[str, Any]:
    """Parse input line.

    Expects input line to be key = value.

    :param input_line: The line to parse the key and value from.
    :param value_parser: A function to use to parse the value of the key.
    :returns: A key and parsed Value.
    :raises ValueError: If the line does not have exactly 1 '=' in it.
    """
    if value_parser is None:

        def value_parser(x: Any) -> Any:
            return x

    key_val = input_line.split("=")
    if len(key_val) != 2:
        raise ValueError(
            "Parsing of input file line failed. Expecting 1 '=' in: %s", input_line
        )

    return key_val[0].strip(), value_parser(key_val[1].strip())


def parse_input(input_str: str) -> Dict[str, List[State]]:
    """Parse input.

    :param input_str: The string of input to parse.
    :returns: The parsed input.
    """
    return {
        k: v
        for k, v in [
            parse_key_value_line(i, State.parse_list) for i in input_str.splitlines()
        ]
    }


def parse_circuit(circuit: str) -> List[Tuple[str, CircuitFunction]]:
    """Parse a circuit.

    :param circuit: The string of the circuit to parse.
    :returns: The parsed circuit.
    """
    return [
        (k, v)
        for k, v in [
            parse_key_value_line(i, CircuitFunction.parse) for i in circuit.splitlines()
        ]
    ]


known_functions = {
    "inv": lambda x_list: [~x for x in x_list],
    "and2": lambda x_list, y_list: [x & y for x, y in zip(x_list, y_list)],
    "or2": lambda x_list, y_list: [x | y for x, y in zip(x_list, y_list)],
}


def resolve_circuits(
    inputs: Dict[str, List[State]], circuits: List[Tuple[str, CircuitFunction]]
) -> List[Tuple[str, List[State]]]:
    """Resolve circuits.

    :param inputs: the inputs to use.
    :param circuits: The circuits to resolve.
    :returns: The resolved circuits.
    :raises ValueError: If it could not resolve all the circuits.
    """
    resolved_tokens = {k: v for k, v in inputs.items()}

    circuits_to_evaluate = circuits.copy()

    while circuits_to_evaluate:
        for i, (output, func) in enumerate(circuits_to_evaluate):
            try:
                args = [resolved_tokens[arg] for arg in func.args]
                resolved_tokens[output] = known_functions[func.name](*args)
                circuits_to_evaluate.pop(i)
                break
            except KeyError:
                continue
        else:
            raise ValueError(
                "Could not resolve all circuits. Is there a circular dependency?"
            )

    return [(out, resolved_tokens[out]) for out, _ in circuits]


def resolved_token_to_string(resolved: Tuple[str, List[State]]) -> str:
    """Convert resolved state to string.

    :param resolved: The resolved state.
    :returns: A string representation of the resolved state.
    """
    return f"{resolved[0]} = [{', '.join([str(s) for s in resolved[1]])}]"


def main(input_str: str, circuit_str: str) -> str:
    """Parse input and circuit.

    :param input_str: The input string.
    :param circuit_str: The circuit to test.
    :returns: The results of simulation
    """
    resolved = resolve_circuits(parse_input(input_str), parse_circuit(circuit_str))
    return "\n".join([resolved_token_to_string(r) for r in resolved])


def parse_args(args: List[str]) -> Namespace:
    """Parse arguments on command line.

    :param args: The arguments to parse.
    :returns: The parsed arguments.
    """
    parser = argparse.ArgumentParser(prog="sim.py")
    parser.add_argument(
        "input_f",
        type=Path,
        default=Path(__file__).absolute().parent / "input.txt",
        help="input.txt file. Defaults to ./input.txt",
    )
    parser.add_argument(
        "circuit_f",
        type=Path,
        default=Path(__file__).absolute().parent / "circuit.txt",
        help="circuit.txt file. Defaults to ./circuit.txt",
    )
    return parser.parse_args(args)


def cli() -> None:
    """Do Main function.

    Handle the user input files.
    Print results.
    """
    args = parse_args(sys.argv[1:])

    input_text = args.input_f.read_text()
    circuit_text = args.circuit_f.read_text()

    print(main(input_text, circuit_text))  # noqa: T001


if __name__ == "__main__":
    cli()
