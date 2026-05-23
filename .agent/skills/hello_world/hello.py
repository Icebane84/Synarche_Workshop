import sys


def say_hello(name="World"):
    """
    Returns a standardized greeting.
    """
    print(f"Systems Online. Hello, {name}. The Forge is Hot.")


if __name__ == "__main__":
    target_name = sys.argv[1] if len(sys.argv) > 1 else "Traveler"
    say_hello(target_name)
