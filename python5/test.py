======= ex0/ data_processor.py =======
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self._data = []
        self._index = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise Exception("No data to output")

        value = self._data.pop(0)
        idx = self._index
        self._index += 1
        return (idx, value)


# =========================
# Numeric
# =========================
class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        if isinstance(data, list):
            for x in data:
                self._data.append(str(x))
        else:
            self._data.append(str(data))


# =========================
# Text
# =========================
class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")

        if isinstance(data, list):
            self._data.extend(data)
        else:
            self._data.append(data)


# =========================
# Log
# =========================
class LogProcessor(DataProcessor):

    def is_log(self, d):
        return isinstance(d, dict) and all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in d.items()
        )

    def validate(self, data: Any) -> bool:
        if self.is_log(data):
            return True
        if isinstance(data, list):
            return all(self.is_log(x) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")

        def format_log(d):
            return f"{d['log_level']}: {d['log_message']}"

        if isinstance(data, list):
            for d in data:
                self._data.append(format_log(d))
        else:
            self._data.append(format_log(data))


def main():
    print("=== Code Nexus - Data Processor ===")

    # -------- Numeric --------
    print("\nTesting Numeric Processor...")
    num = NumericProcessor()

    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")
    except Exception as e:
        print(f"Got exception: {e}")

    print("Processing data: [1, 2, 3, 4, 5]")
    num.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for _ in range(3):
        idx, val = num.output()
        print(f"Numeric value {idx}: {val}")

    # -------- Text --------
    print("\nTesting Text Processor...")
    txt = TextProcessor()

    print(f"Trying to validate input '42': {txt.validate(42)}")

    print("Processing data: ['Hello', 'Nexus', 'World']")
    txt.ingest(['Hello', 'Nexus', 'World'])

    print("Extracting 1 value...")
    idx, val = txt.output()
    print(f"Text value {idx}: {val}")

    # -------- Log --------
    print("\nTesting Log Processor...")
    log = LogProcessor()

    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")

    data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]

    print(f"Processing data: {data}")
    log.ingest(data)

    print("Extracting 2 values...")
    for _ in range(2):
        idx, val = log.output()
        print(f"Log entry {idx}: {val}")


if __name__ == "__main__":
    main()

======= ex1/data_stream.py =======
from abc import ABC, abstractmethod
from typing import Any


# =========================
# BASE PROCESSOR
# =========================
class DataProcessor(ABC):
    def __init__(self):
        self._data = []
        self._index = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise Exception("No data to output")

        value = self._data.pop(0)
        idx = self._index
        self._index += 1
        return idx, value


# =========================
# NUMERIC
# =========================
class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")

        if isinstance(data, list):
            for x in data:
                self._data.append(str(x))
        else:
            self._data.append(str(data))


# =========================
# TEXT
# =========================
class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")

        if isinstance(data, list):
            self._data.extend(data)
        else:
            self._data.append(data)


# =========================
# LOG
# =========================
class LogProcessor(DataProcessor):

    def is_log(self, d):
        return isinstance(d, dict) and all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in d.items()
        )

    def validate(self, data: Any) -> bool:
        if self.is_log(data):
            return True
        if isinstance(data, list):
            return all(self.is_log(x) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")

        def format_log(d):
            return f"{d['log_level']}: {d['log_message']}"

        if isinstance(data, list):
            for d in data:
                self._data.append(format_log(d))
        else:
            self._data.append(format_log(data))


# =========================
# DATA STREAM (FIXED)
# =========================
class DataStream:
    def __init__(self):
        self.processors = []

    def register_processor(self, processor: DataProcessor) -> None:
        self.processors.append(processor)

    def process_stream(self, stream: list[Any]) -> None:
        print(f"Send batch of data on stream: {stream}")

        for item in stream:
            handled = False

            for processor in self.processors:
                if processor.validate(item):
                    try:
                        processor.ingest(item)
                    except Exception as e:
                        print(
                            f"DataStream error - Can't process element in stream: {item}")
                    handled = True
                    break

            if not handled:
                print(
                    f"DataStream error - Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self.processors:
            print("No processor found, no data")
            return

        for processor in self.processors:
            name = processor.__class__.__name__
            processed = len(processor._data)

            print(
                f"{name}: total {processed} items processed, remaining {processed} on processor")


# =========================
# MAIN TEST
# =========================
def main():
    print("=== Code Nexus - Data Stream ===")

    stream = DataStream()

    print("\nInitialize Data Stream...")
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")

    num = NumericProcessor()
    stream.register_processor(num)

    batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING", "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO", "log_message": "User wil is connected"}
        ],
        42,
        ["Hi", "five"]
    ]

    print("\nSend first batch of data on stream:", batch)
    stream.process_stream(batch)

    stream.print_processors_stats()

    print("\nRegistering other data processors")

    txt = TextProcessor()
    log = LogProcessor()

    stream.register_processor(txt)
    stream.register_processor(log)

    print("\nSend the same batch again")
    stream.process_stream(batch)

    stream.print_processors_stats()

    print("\nConsume elements")

    for _ in range(3):
        try:
            num.output()
        except BaseException:
            pass

    for _ in range(2):
        try:
            txt.output()
        except BaseException:
            pass

    try:
        log.output()
    except BaseException:
        pass

    stream.print_processors_stats()


if __name__ == "__main__":
    main()

======= ex2/nexus_pipeline.py =======
from typing import Any, Protocol, List, Tuple
from abc import ABC, abstractmethod
# =========================faudra le recheck et apprendre quand meme je l ai pas fait lui

# =========================
# PROCESSORS (from ex1)
# =========================


class DataProcessor(ABC):
    def __init__(self):
        self._data = []
        self._index = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise Exception("No data to output")

        value = self._data.pop(0)
        idx = self._index
        self._index += 1
        return idx, value


# =========================
# PROCESSORS (simplifiés)
# =========================
class NumericProcessor(DataProcessor):
    def validate(
        self, data): return isinstance(
        data, (int, float)) or isinstance(
            data, list)

    def ingest(self, data):
        if isinstance(data, list):
            self._data.extend([str(x) for x in data])
        else:
            self._data.append(str(data))


class TextProcessor(DataProcessor):
    def validate(
        self,
        data): return isinstance(
        data,
        str) or isinstance(
            data,
        list)

    def ingest(self, data):
        if isinstance(data, list):
            self._data.extend(data)
        else:
            self._data.append(data)


class LogProcessor(DataProcessor):
    def is_log(self, d):
        return isinstance(d, dict) and "log_level" in d and "log_message" in d

    def validate(self, data):
        return self.is_log(data) or (
            isinstance(
                data, list) and all(
                self.is_log(x) for x in data))

    def ingest(self, data):
        def fmt(d): return f"{d['log_level']}: {d['log_message']}"
        if isinstance(data, list):
            self._data.extend([fmt(x) for x in data])
        else:
            self._data.append(fmt(data))


# =========================
# EXPORT PLUGIN (Protocol)
# =========================
class ExportPlugin(Protocol):
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        ...


# =========================
# CSV PLUGIN
# =========================
class CSVExportPlugin:
    def process_output(self, data):
        print("CSV Output:")
        for _, value in data:
            print(value)


# =========================
# JSON PLUGIN
# =========================
class JSONExportPlugin:
    def process_output(self, data):
        print("JSON Output:")
        result = {}

        for i, (_, value) in enumerate(data):
            result[f"item_{i}"] = value

        print("{" + ", ".join(f'"{k}": "{v}"' for k, v in result.items()) + "}")


# =========================
# DATA STREAM
# =========================
class DataStream:
    def __init__(self):
        self.processors = []

    def register_processor(self, p):
        self.processors.append(p)

    def process_stream(self, stream):
        print(f"Send batch of data on stream: {stream}")

        for item in stream:
            handled = False

            for p in self.processors:
                if p.validate(item):
                    p.ingest(item)
                    handled = True
                    break

            if not handled:
                print(
                    f"DataStream error - Can't process element in stream: {item}")

    def print_processors_stats(self):
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return

        for p in self.processors:
            print(
                f"{p.__class__.__name__}: total {len(p._data)} items processed, remaining {len(p._data)} on processor")

    # =========================
    # OUTPUT PIPELINE (NEW)
    # =========================
    def output_pipeline(self, nb: int, plugin: ExportPlugin):
        collected = []

        for p in self.processors:
            for _ in range(min(nb, len(p._data))):
                try:
                    collected.append(p.output())
                except BaseException:
                    pass

        plugin.process_output(collected)


# =========================
# DEMO
# =========================
def main():
    print("=== Code Nexus - Data Pipeline ===")

    stream = DataStream()

    print("Initialize Data Stream...")
    stream.print_processors_stats()

    print("\nRegistering Processors")

    num = NumericProcessor()
    txt = TextProcessor()
    log = LogProcessor()

    stream.register_processor(num)
    stream.register_processor(txt)
    stream.register_processor(log)

    batch = [
        "Hello world",
        [3.14, -1, 2.71],
        {"log_level": "WARNING", "log_message": "Telnet access!"},
        42,
        ["Hi", "five"]
    ]

    print("\nSend first batch of data on stream:", batch)
    stream.process_stream(batch)

    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())

    stream.print_processors_stats()

    batch2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        {"log_level": "ERROR", "log_message": "500 server crash"},
        [32, 42, 64],
        "World hello"
    ]

    print("\nSend another batch of data:", batch2)
    stream.process_stream(batch2)

    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())

    stream.print_processors_stats()


if __name__ == "__main__":
    main()

