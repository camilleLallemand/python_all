from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise Exception("Improper numeric data")
        values: List[float] = data if isinstance(data, list) else [data]
        total = sum(values)
        avg = total / len(values)
        return (
            f"Processed {len(values)} numeric values, "
            f"sum={total}, avg={avg}"
        )

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise Exception("Improper text data")
        chars = len(data)
        words = len(data.split())
        return f"Processed text: {chars} characters, {words} words"

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if not isinstance(data, str):
            return False
        return ':' in data

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise Exception("Improper log data")
        parts = data.split(':', 1)
        level = parts[0].strip()
        message = parts[1].strip() if len(parts) > 1 else ""
        return f"[{level}] {level} level detected: {message}"

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


def run_processor(
    processor: DataProcessor,
    label: str,
    data: Any,
    validation_label: str
) -> None:
    print(f"Initializing {label}...")
    print(f"Processing data: {data!r}")
    is_valid = processor.validate(data)
    print(f"Validation: {validation_label}")
    if is_valid:
        result = processor.process(data)
        print(processor.format_output(result))


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    run_processor(
        NumericProcessor(),
        "Numeric Processor",
        [1, 2, 3, 4, 5],
        "Numeric data verified"
    )

    run_processor(
        TextProcessor(),
        "Text Processor",
        "Hello Nexus World",
        "Text data verified"
    )

    run_processor(
        LogProcessor(),
        "Log Processor",
        "ERROR: Connection timeout",
        "Log entry verified"
    )

    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")

    processors: List[DataProcessor] = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]
    demo_data: List[Any] = [
        [1, 2, 3],
        "Hello Nexus",
        "INFO: System ready"
    ]

    for i, (proc, item) in enumerate(zip(processors, demo_data), start=1):
        result = proc.process(item)
        print(f"Result {i}: {result}")

    print("Foundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
