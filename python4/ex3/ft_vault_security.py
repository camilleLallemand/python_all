def secure_archive(filename: str, mode: int, s: str):
    try:
        if (mode == 1):
            with open(filename, 'r') as data:
                content = data.read()
            return (True, content)
        elif (mode == 2):
            with open(filename, 'w') as data:
                data.write(s)
            return (True, 'Content successfully written to file')
        else:
            return (False, "Invalid mode")
    except Exception as e:
        return (False, str(e))


if __name__ == "__main__":
    print("=== Cyber Archives Security ===")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file", 1, ""))

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("test1", 1, ""))

    print("Using 'secure_archive' to read from a regular file:")
    success, data = secure_archive("test2", 1, "")
    print((success, data))

    print("Using 'secure_archive' to write previous content to a new file:")
    if success:
        print(secure_archive("new_file.txt", 2, data))
