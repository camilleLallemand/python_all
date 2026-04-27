VAULT_FILE = "ancient_fragment.txt"


def ancien_text():
    file = VAULT_FILE
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{file}'")
    try:
        with open(file, 'r') as f:
            text = f.read()
            print(text)
        print(f"File {file} closed.")
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for file '{file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    ancien_text()
