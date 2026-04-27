import sys


def ancien_text():
    if len(sys.argv) != 2:
        print("Usage: python3 ft_ancient_text.py <text>")
        return

    file = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file}'")
    print("---\n")

    try:
        with open(file, 'r') as f:
            text = f.read()
            print(text)

        print(f"File '{file}' closed.")

    except FileNotFoundError:
        print(
            f"[STDERR] Error opening file '{file}': [Errno 2] No such file or directory: '{file}'",
            file=sys.stderr)
        return

    except PermissionError:
        print(
            f"[STDERR] Error opening file '{file}': [Errno 13] Permission denied: '{file}'",
            file=sys.stderr)
        return

    except Exception as e:
        print(f"[STDERR] Error opening file '{file}': {e}", file=sys.stderr)
        return

    print("\nTransform data:")
    print("---\n")

    transformed = [line.rstrip() + "#" for line in text.splitlines()]

    for line in transformed:
        print(line)

    print("\n---")

    # remplacement input() → stdin
    print("Enter new file name (or empty): ", end="")
    save = sys.stdin.readline().strip()

    if not save:
        print("Not saving data.")
        return

    try:
        print(f"Saving data to '{save}'")
        with open(save, 'w') as f:
            f.write("\n".join(transformed))

        print(f"Data saved in file '{save}'")

    except Exception as e:
        print(f"[STDERR] Error saving file '{save}': {e}", file=sys.stderr)
