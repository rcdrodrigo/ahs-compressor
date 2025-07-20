import os


class MyClass:
    """A simple class for demonstration."""

    def __init__(self, name):
        self.name = name  # Store the name

    def greet(self):
        # This method prints a greeting
        print(f"Hello from {self.name}!")


def calculate_sum(a: int, b: int) -> int:
    """
    Calculates the sum of two numbers.
    This function is pure.
    """
    return a + b

MY_CONSTANT = 123  # A global constant

