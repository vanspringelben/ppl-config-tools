from schemas.schemas import deviceSchemas
from helpers.typing import validateType, expectedTypeToString
from validators.result import ValidationResult


def validate_devices(devices: list[dict]) -> ValidationResult:
    result = ValidationResult([])

    ids = set()

    for idx, device in enumerate(devices):
        device_id = device.get("id", f"device[{idx}]")

        if device_id in ids:
            result.add("error", f"Duplicate device id '{device_id}'")
        ids.add(device_id)

        dtype = device.get("type")
        if dtype not in deviceSchemas:
            if dtype is None:
                result.add("error", f"Device '{device_id}' missing 'type'")
            else:
                result.add("error", f"Device '{device_id}' has unknown device type '{dtype}'")
            
            continue

        schema = deviceSchemas[dtype]

        for field, expected in schema["required"].items():
            if field not in device:
                result.add("error", f"Device '{device_id}' missing '{field}'")
            elif not validateType(device[field], expected):
                result.add("error", f"Device '{device_id}' field '{field}' expected {expectedTypeToString(expected)}")

        for field, expected in schema["optional"].items():
            if field in device and not validateType(device[field], expected):
                result.add("warning", f"Device '{device_id}' optional field '{field}' expected {expectedTypeToString(expected)}")

    return result