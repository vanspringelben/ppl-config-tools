import re
from schemas.schemas import addressMapSchemas, expressionSchema
from helpers.typing import validateType, expectedTypeToString
from validators.registers import validate_required_registers, build_registers_by_name
from validators.result import merge_validation_results
from validators.result import ValidationResult


def validate_address_map(
    registers: list[dict],
    map_type: str,
    precharge_contactor_feedback: bool = False,
) -> ValidationResult:
    result = ValidationResult([])

    if map_type not in addressMapSchemas:
        result.add("error", f"Invalid map type '{map_type}'")
        return result

    required = addressMapSchemas[map_type]["required"]
    optional = addressMapSchemas[map_type]["optional"]
    constraints = addressMapSchemas[map_type].get("constraints", {})

    seen_names = set()
    expressions = []

    for idx, reg in enumerate(registers):
        name = reg.get("name", f"register[{idx}]")

        if name in seen_names:
            result.add("error", f"Duplicate register '{name}'")
        seen_names.add(name)

        if "expression" in reg:
            if validateType(reg["expression"], expressionSchema["expression"]):
                expressions.append((name, reg["expression"]))
            else:
                result.add("error", f"Invalid expression in register '{name}'")
            continue

        for field, expected in required.items():
            if field not in reg:
                result.add("error", f"Register '{name}' missing '{field}'")
            elif not validateType(reg[field], expected):
                result.add("error", f"Register '{name}' field '{field}' expected {expectedTypeToString(expected)}")

        for field, rule in constraints.items():
            if field not in reg:
                continue

            value = reg[field]
            if not isinstance(value, (int, float)):
                continue

            if "min" in rule and value < rule["min"]:
                result.add("error", f"Register '{name}' field '{field}' must be between {rule.get('min')} and {rule.get('max')}")
            elif "max" in rule and value > rule["max"]:
                result.add("error", f"Register '{name}' field '{field}' must be between {rule.get('min')} and {rule.get('max')}")

        for field, expected in optional.items():
            if field in reg and not validateType(reg[field], expected):
                result.add("warning", f"Register '{name}' optional field '{field}' expected {expectedTypeToString(expected)}")

        unknown = set(reg) - set(required) - set(optional)
        if unknown:
            result.add("warning", f"Register '{name}' unknown fields: {', '.join(unknown)}")

    # Expression cross-check
    for name, expr in expressions:
        refs = re.findall(r"{([^}]+)}", expr)
        missing = [r for r in refs if r not in seen_names]
        if missing:
            result.add("error", f"Expression '{name}' references missing registers: {missing}")

    if map_type == "Modbus TCP/IP" and "communicationCheck" not in seen_names:
        result.add("error", "Missing required register 'communicationCheck' for Modbus TCP/IP")

    if map_type == "Precharge":
        required_registers = [
            ("control.contactor.main", "type", "output"),
            ("control.contactor.auxiliary", "type", "output"),
        ]

        if precharge_contactor_feedback is True:
            required_registers = required_registers + [
                ("measure.contactor.main", "type", "input"),
                ("measure.contactor.auxiliary", "type", "input"),
            ]

        registers_by_name = build_registers_by_name(registers)

        regs_result = validate_required_registers(registers_by_name, required_registers)
        result = merge_validation_results(result, regs_result)

    if map_type == "Breaker":
        required_registers = [("measure.breaker", "type", "input")]

        registers_by_name = build_registers_by_name(registers)
        regs_result = validate_required_registers(registers_by_name, required_registers)
        result = merge_validation_results(result, regs_result)

    if map_type == "Contactor":
        required_registers = [("measure.contactor", "type", "input")]

        registers_by_name = build_registers_by_name(registers)
        regs_result = validate_required_registers(registers_by_name, required_registers)
        result = merge_validation_results(result, regs_result)

    return result


def get_precharge_contactor_feedback(devices_payload, address_map_file) -> bool:
    precharge_contactor_feedback = False

    address_map_ref = address_map_file[:-5] if address_map_file.endswith(".json") else address_map_file
    for device in devices_payload:
        if not isinstance(device, dict):
            continue
        if device.get("type") != "precharge":
            continue
        if device.get("addressMap") != address_map_ref:
            continue

        if device.get("contactorFeedback") is True:
            precharge_contactor_feedback = True
        break

    return precharge_contactor_feedback