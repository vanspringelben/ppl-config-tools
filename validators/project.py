from validators.result import ValidationResult
from validators.registers import build_registers_by_name


def find_missing_device_references(devices, available_files: set[str]) -> ValidationResult:
    result = ValidationResult([])

    if not isinstance(devices, list):
        return result

    for d_idx, device in enumerate(devices):
        if not isinstance(device, dict):
            continue

        device_id = device.get("id", f"device[{d_idx}]")

        address_map = device.get("addressMap")
        if isinstance(address_map, str):
            expected = f"{address_map}.json"
            if expected not in available_files:
                result.add("error", f"Device '{device_id}' references missing address map file '{address_map}.json'")

        control_map = device.get("controlMap")
        if isinstance(control_map, str) and control_map.strip() != "":
            expected = f"{control_map}.json"
            if expected not in available_files:
                result.add("error", f"Device '{device_id}' references missing control map file '{control_map}.json'")

    return result


def validate_control_map_commands(*, control_map_file, control_map, devices, address_maps_by_file) -> ValidationResult:
    result = ValidationResult([])

    if not isinstance(devices, list):
        return result

    if not isinstance(control_map, list):
        return result

    if isinstance(control_map_file, str) and control_map_file.lower().endswith(".json"):
        control_map_ref = control_map_file[:-5]

    for d_idx, device in enumerate(devices):
        if not isinstance(device, dict):
            continue

        device_control_map_ref = device.get("controlMap")
        if not isinstance(device_control_map_ref, str) or device_control_map_ref.strip() == "":
            continue

        if device_control_map_ref != control_map_ref:
            continue

        device_id = device.get("id", f"device[{d_idx}]")

        address_map_ref = device.get("addressMap")
        if not isinstance(address_map_ref, str) or address_map_ref.strip() == "":
            continue

        address_map_file = f"{address_map_ref}.json"
        address_map = address_maps_by_file.get(address_map_file)
        if not isinstance(address_map, list):
            continue

        registers_by_name = build_registers_by_name(address_map)

        for cm_idx, cm in enumerate(control_map):
            if not isinstance(cm, dict):
                continue

            cm_name = cm.get("name", f"register[{cm_idx}]")
            commands = cm.get("commands")
            if not isinstance(commands, str) or commands.strip() == "":
                continue

            tokens = [t.strip() for t in commands.split("|")]
            for token in tokens:
                if token == "":
                    continue

                base = None
                if token.endswith("?"):
                    base = token[:-1].strip()
                elif "=" in token:
                    base = token.split("=", 1)[0].strip()

                if not base:
                    continue

                if base not in registers_by_name:
                    result.add(
                        "warning",
                        f"Device '{device_id}' control register '{cm_name}' references command '{base}' which is missing from address map '{address_map_ref}'",
                    )

    return result