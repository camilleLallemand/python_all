from typing import Tuple


def crisis_handler(filename: str) -> Tuple[bool, str]:
    try:
        with open(filename, 'r') as vault:
            content = vault.read().strip()
        return (True, content)
    except FileNotFoundError:
        return (False, "Archive not found in storage matrix")
    except PermissionError:
        return (False, "Security protocols deny access")
    except Exception as e:
        return (False, f"Unexpected system anomaly: {e}")


def handle_access(filename: str, routine: bool = False) -> None:
    if routine:
        print(f"ROUTINE ACCESS: Attempting access to '{filename}'...")
    else:
        print(f"CRISIS ALERT: Attempting access to '{filename}'...")

    success, result = crisis_handler(filename)

    if success:
        print(f"SUCCESS: Archive recovered - \"{result}\"")
        print("STATUS: Normal operations resumed")
    else:
        print(f"RESPONSE: {result}")
        print("STATUS: Crisis handled, system stable")


def main() -> None:
    print("=== Cyber Archives - Crisis Response System ===")

    handle_access("lost_archive.txt")
    handle_access("classified_vault.txt")
    handle_access("standard_archive.txt", routine=True)

    print("All crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    main()
