from schemas.schemas import controlMapSchema
from helpers.typing import validateType, expectedTypeToString
from validators.result import ValidationResult


def validate_control_maps(control_maps) -> ValidationResult:
    result = ValidationResult([])

    if isinstance(control_maps, dict):
        control_maps = [control_maps]

    if not isinstance(control_maps, list):
        result.add("error", f"Control map file must be a list (or object), got {type(control_maps).__name__}")
        return result

    seen_names = set()

    for idx, cm in enumerate(control_maps):
        name = cm.get("name", f"register[{idx}]")

        if name in seen_names:
            result.add("error", f"Duplicate control register name '{name}'")
            continue
        seen_names.add(name)

        if not isinstance(cm, dict):
            result.add("error", f"{name} must be an object")
            continue

        for field, expected in controlMapSchema.items():
            if field not in cm:
                result.add("error", f"Control register '{name}' missing '{field}'")
            elif not validateType(cm[field], expected):
                result.add("error", f"Control register '{name}' field '{field}' expected {expectedTypeToString(expected)}")

        if "commands" in cm and isinstance(cm.get("commands"), str):
            if cm["commands"].strip() != "":
                tokens = [t.strip() for t in cm["commands"].split("|")]
                for t_idx, token in enumerate(tokens):
                    if token == "":
                        result.add("error", f"Control register '{name}' field 'commands' contains an empty command at position {t_idx}")
                        continue

                    if token.endswith("?"):
                        if "=" in token:
                            result.add("error", f"Control register '{name}' read command '{token}' must not contain '='")
                            continue

                        base = token[:-1].strip()
                        if base == "":
                            result.add("error", f"Control register '{name}' read command '{token}' must have a command before '?'")
                            continue
                    elif "=" in token:
                        left, right = token.split("=", 1)
                        left = left.strip()
                        right = right.strip()

                        if left == "" or right == "":
                            result.add("error", f"Control register '{name}' write command '{token}' must have a command before '=' and a value after")
                            continue

                        if left.endswith("?"):
                            result.add("error", f"Control register '{name}' write command '{token}' must not have '?' in the command part")
                            continue
                    else:
                        result.add("error", f"Control register '{name}' command '{token}' must end with '?' (read) or contain '=' (write)")

        unknown = set(cm) - set(controlMapSchema)
        if unknown:
            result.add("warning", f"Control register '{name}' unknown fields: {', '.join(unknown)}")

    return result
