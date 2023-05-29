from typing import Any

import utils


class Contract:
    abi: dict = None
    event_mappings: dict[str, dict] = None

    def __init__(self, abi: dict) -> None:
        self.abi = abi
        self.event_mappings = {}

        # parse events
        for entry in self.abi:
            if entry["type"].lower() != "event":
                continue

            inputs = ",".join([row["type"] for row in entry["inputs"]])
            event_name: str = entry["name"]
            event_topic: str = utils.keccak256(f"{event_name}({inputs})").removeprefix(
                "0x"
            )

            event_data: dict = {
                "name": event_name,
                "params": entry["inputs"],
            }
            self.event_mappings[event_topic] = event_data

    def can_decode(self, log: dict) -> bool:
        topics = log["topics"]
        event_topic = topics[0]
        return event_topic in self.event_mappings

    def decode_log(self, log: dict) -> tuple[str, dict[str, Any]]:
        topics = log["topics"]
        data = log.get("data", [])
        event_topic = topics[0]
        event_data = self.event_mappings[event_topic]
        input_names = [row["name"] for row in event_data["params"]]
        input_types = [row["type"] for row in event_data["params"]]

        values = topics[1:]
        types_to_decode = input_types[len(values) :]
        if types_to_decode:
            decoded_values = utils.decode_params(data, types_to_decode)
            values += decoded_values

        for t, v in zip(input_types, values):
            value = utils.to_base58(v[-40:]) if t == "address" else v
            values.append(value)
        return event_data["name"], dict(zip(input_names, values))
