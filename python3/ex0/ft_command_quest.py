import sys


def process_arg() -> None:
    if len(sys.argv) < 1:
        print("No program name found")
        return
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) > 1:
        print(f"Arguments received: {len(sys.argv) - 1}")
        for i, arg in enumerate(sys.argv[1:]):
            print(f"Argument {i + 1}: {arg}")
    else:
        print("No arguments provided!")

    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    print("=== Command Quest ===")
    process_arg()
