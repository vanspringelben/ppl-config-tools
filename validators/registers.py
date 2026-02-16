from validators.result import ValidationResult


def build_registers_by_name(registers) -> dict[str, dict]:
    registers_by_name: dict[str, dict] = {}

    if not isinstance(registers, list):
        return registers_by_name

    for reg in registers:
        if not isinstance(reg, dict):
            continue

        name = reg.get("name")
        if isinstance(name, str) and name.strip() != "":
            registers_by_name[name] = reg

    return registers_by_name


def validate_required_registers(registers_by_name, required) -> ValidationResult:
    result = ValidationResult([])

    if not isinstance(required, list):
        return result

    for req in required:
        if not isinstance(req, tuple) or len(req) != 3:
            continue

        register_name, field_name, expected_value = req

        if register_name not in registers_by_name:
            result.add("error", f"Missing required register '{register_name}'")
            continue

        reg = registers_by_name.get(register_name)
        if not isinstance(reg, dict):
            result.add("error", f"Invalid register '{register_name}'")
            continue

        if field_name not in reg:
            result.add("error", f"Register '{register_name}' missing required field '{field_name}'")
            continue

        actual_value = reg.get(field_name)
        if actual_value != expected_value:
            result.add("error", f"Register '{register_name}' field '{field_name}' expected '{expected_value}', got '{actual_value}'")

    return result
