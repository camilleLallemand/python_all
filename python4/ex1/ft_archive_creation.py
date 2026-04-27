OUTPUT_FILE = "new_discovery.txt"

ENTRIES = [
    "[ENTRY 001] New quantum algorithm discovered",
    "[ENTRY 002] Efficiency increased by 347%",
    "[ENTRY 003] Archived by Data Archivist trainee",
]


def create_archive() -> None:
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Initializing new storage unit: {OUTPUT_FILE}")
    try:
        with open(OUTPUT_FILE, 'w') as archive:
            print("Storage unit created successfully...")
            print("Inscribing preservation data...")
            for entry in ENTRIES:
                print(entry)
                archive.write(entry + "\n")
        print("Data inscription complete. Storage unit sealed.")
        print(f"Archive '{OUTPUT_FILE}' ready for long-term preservation.")
    except PermissionError:
        print(f"Error: Permission denied when writing '{OUTPUT_FILE}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_archive()
