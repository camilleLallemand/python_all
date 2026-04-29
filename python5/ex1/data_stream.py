# ex1/data_stream.py

from typing import Any
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../ex0",
        )
    )
)

from data_processor import (  # noqa: E402
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._processed_count: dict[str, int] = {}

    def register_processor(self, processor: DataProcessor) -> None:
        processor_name = processor.__class__.__name__
        self._processors.append(processor)
        self._processed_count[processor_name] = 0

    def _get_processed_items_count(self, data: Any) -> int:
        if isinstance(data, list):
            return len(data)
        return 1

    def _format_processor_name(self, processor: DataProcessor) -> str:
        name = processor.__class__.__name__
        return name.replace("Processor", " Processor")

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled = False

            for processor in self._processors:
                if processor.validate(element):
                    processor.ingest(element)

                    processor_name = processor.__class__.__name__
                    self._processed_count[
                        processor_name
                    ] += self._get_processed_items_count(element)

                    handled = True
                    break

            if not handled:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for processor in self._processors:
            processor_name = processor.__class__.__name__
            display_name = self._format_processor_name(processor)

            total_processed = self._processed_count[processor_name]
            remaining_items = len(processor._storage)

            print(
                f"{display_name}: total {total_processed} "
                f"items processed, remaining "
                f"{remaining_items} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")

    stream = DataStream()

    print("Initialize Data Stream...\n")
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    stream.register_processor(NumericProcessor())

    first_batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print(f"\nSend first batch of data on stream: {first_batch}")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    print("\nSend the same batch again")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )

    numeric = stream._processors[0]
    text = stream._processors[1]
    logs = stream._processors[2]

    for _ in range(3):
        if numeric._storage:
            numeric.output()

    for _ in range(2):
        if text._storage:
            text.output()

    for _ in range(1):
        if logs._storage:
            logs.output()

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
