from typing import Protocol
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../ex0"
        )
    )
)

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../ex1"
        )
    )
)

from data_processor import (
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)

from data_stream import DataStream

class ExportPlugin(Protocol):
    def process_output(
        self,
        data: list[tuple[int, str]],
    ) -> None:
        ...


class CSVExport:
    def process_output(
        self,
        data: list[tuple[int, str]],
    ) -> None:
        values = [value for _, value in data]

        print("CSV Output:")
        print(",".join(values))


class JSONExport:
    def process_output(
        self,
        data: list[tuple[int, str]],
    ) -> None:
        items = []

        for rank, value in data:
            items.append(f'"item_{rank}": "{value}"')

        print("JSON Output:")
        print("{" + ", ".join(items) + "}")


class PipelineDataStream(DataStream):
    def output_pipeline(
        self,
        amount: int,
        plugin: ExportPlugin,
    ) -> None:
        for processor in self._processors:
            extracted: list[tuple[int, str]] = []

            for _ in range(amount):
                if not processor._storage:
                    break

                extracted.append(processor.output())

            if extracted:
                plugin.process_output(extracted)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")

    stream = PipelineDataStream()

    print("Initialize Data Stream...\n")
    stream.print_processors_stats()

    print("\nRegistering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

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

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExport())
    stream.print_processors_stats()

    second_batch = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]

    print(f"\nSend another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExport())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
