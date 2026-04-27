from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self._stream_id = stream_id
        self._processed_count = int(0)
        self._error_count = int(0)

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria is None:
            return data_batch
        return [
            item for item in data_batch
            if criteria.lower() in str(item).lower()
        ]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self._stream_id,
            "processed": self._processed_count,
            "errors": self._error_count,
        }


class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self._stream_type = "Environmental Data"

    def process_batch(self, data_batch: List[Any]) -> str:
        numeric = [
            x for x in data_batch
            if isinstance(x, (int, float))
        ]
        self._processed_count += len(numeric)
        if not numeric:
            self._error_count += 1
            return "No valid sensor readings"
        avg_temp = sum(numeric) / len(numeric)
        return (
            f"Sensor analysis: {len(numeric)} readings processed, "
            f"avg temp: {avg_temp:.1f}\u00b0C"
        )

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria == "critical":
            return [x for x in data_batch
                    if isinstance(x, (int, float)) and x > 30]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        stats = super().get_stats()
        stats["type"] = self._stream_type
        return stats


class TransactionStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self._stream_type = "Financial Data"
        self._net_flow = float(0)

    def process_batch(self, data_batch: List[Any]) -> str:
        operations = [
            x for x in data_batch
            if isinstance(x, dict) and "type" in x and "amount" in x
        ]
        self._processed_count += len(operations)
        if not operations:
            self._error_count += 1
            return "No valid transactions"
        net = sum(
            op["amount"] if op["type"] == "buy" else -op["amount"]
            for op in operations
        )
        self._net_flow += net
        sign = "+" if net >= 0 else ""
        return (
            f"Transaction analysis: {len(operations)} operations, "
            f"net flow: {sign}{net} units"
        )

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria == "large":
            return [
                x for x in data_batch
                if isinstance(x, dict) and x.get("amount", 0) > 100
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        stats = super().get_stats()
        stats["type"] = self._stream_type
        stats["net_flow"] = self._net_flow
        return stats


class EventStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self._stream_type = "System Events"
        self._error_events = int(0)

    def process_batch(self, data_batch: List[Any]) -> str:
        events = [x for x in data_batch if isinstance(x, str)]
        self._processed_count += len(events)
        errors = [e for e in events if "error" in e.lower()]
        self._error_events += len(errors)
        if not events:
            self._error_count += 1
            return "No valid events"
        return (
            f"Event analysis: {len(events)} events, "
            f"{len(errors)} error detected"
        )

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria == "high-priority":
            return [
                x for x in data_batch
                if isinstance(x, str) and (
                    "error" in x.lower() or "critical" in x.lower()
                )
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        stats = super().get_stats()
        stats["type"] = self._stream_type
        stats["error_events"] = self._error_events
        return stats


class StreamProcessor:

    def __init__(self) -> None:
        self._streams: List[DataStream] = []

    def register_stream(self, stream: DataStream) -> None:
        self._streams.append(stream)

    def process_all(self, data_batch: List[Any]) -> None:
        print(
            "Processing mixed stream types through unified interface..."
        )
        for stream in self._streams:
            try:
                result = stream.process_batch(data_batch)
                name = stream.__class__.__name__
                print(f"  {name}: {result}")
            except Exception as e:
                print(f"  Stream error: {e}")

    def filter_all(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> Dict[str, List[Any]]:
        results: Dict[str, List[Any]] = {}
        for stream in self._streams:
            name = stream.__class__.__name__
            results[name] = stream.filter_data(data_batch, criteria)
        return results

    def print_all_stats(self) -> None:
        for stream in self._streams:
            stats = stream.get_stats()
            print(f"  {stats}")


def main() -> None:
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    sensor = SensorStream("SENSOR_001")
    print("\nInitializing Sensor Stream...")
    print(f"Stream ID: {sensor._stream_id}, Type: Environmental Data")
    sensor_batch: List[Any] = [22.5, 65, 1013]
    print(f"Processing sensor batch: {sensor_batch}")
    print(sensor.process_batch(sensor_batch))

    transaction = TransactionStream("TRANS_001")
    print("\nInitializing Transaction Stream...")
    print(f"Stream ID: {transaction._stream_id}, Type: Financial Data")
    trans_batch: List[Any] = [
        {"type": "buy", "amount": 100},
        {"type": "sell", "amount": 150},
        {"type": "buy", "amount": 75}
    ]
    print(f"Processing transaction batch: {trans_batch}")
    print(transaction.process_batch(trans_batch))

    event = EventStream("EVENT_001")
    print("\nInitializing Event Stream...")
    print(f"Stream ID: {event._stream_id}, Type: System Events")
    event_batch: List[Any] = ["login", "error", "logout"]
    print(f"Processing event batch: {event_batch}")
    print(event.process_batch(event_batch))

    print("\n=== Polymorphic Stream Processing ===")
    processor = StreamProcessor()
    processor.register_stream(SensorStream("SENSOR_002"))
    processor.register_stream(TransactionStream("TRANS_002"))
    processor.register_stream(EventStream("EVENT_002"))

    mixed_batch: List[Any] = [
        21.0, 19.5,
        {"type": "buy", "amount": 50},
        {"type": "sell", "amount": 200},
        {"type": "buy", "amount": 75},
        {"type": "buy", "amount": 120},
        "login", "error", "logout"
    ]
    processor.process_all(mixed_batch)

    print("\nStream filtering active: High-priority data only")
    filtered = processor.filter_all(mixed_batch, "high-priority")
    for name, items in filtered.items():
        print(f"  {name} filtered: {items}")

    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
