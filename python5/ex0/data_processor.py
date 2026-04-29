# ex0/data_processor.py

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._next_rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise Exception("No data available")

        value = self._storage.pop(0)
        rank = self._next_rank
        self._next_rank += 1
        return rank, value


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        values = data if isinstance(data, list) else [data]

        for value in values:
            self._storage.append(str(value))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")

        values = data if isinstance(data, list) else [data]
        self._storage.extend(values)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]],
    ) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")

        logs = data if isinstance(data, list) else [data]

        for log in logs:
            level = log.get("log_level", "").strip()
            message = log.get("log_message", "")
            self._storage.append(f"{level}: {message}")


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    numeric = NumericProcessor()
    print("Testing Numeric Processor...")
    print("Trying to validate input '42':", numeric.validate(42))
    print("Trying to validate input 'Hello':", numeric.validate("Hello"))

    print("\nTest invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")  # type: ignore[arg-type]
    except Exception as error:
        print("Got exception:", error)

    print("\nProcessing data: [1, 2, 3, 4, 5]")
    numeric.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print()

    text = TextProcessor()
    print("Testing Text Processor...")
    print("Trying to validate input '42':", text.validate(42))

    print("\nProcessing data: ['Hello', 'Nexus', 'World']")
    text.ingest(["Hello", "Nexus", "World"])

    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print()

    logs = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server",
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!",
        },
    ]

    logger = LogProcessor()
    print("Testing Log Processor...")
    print("Trying to validate input 'Hello':", logger.validate("Hello"))

    print(f"\nProcessing data: {logs}")
    logger.ingest(logs)

    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = logger.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()