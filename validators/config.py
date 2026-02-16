from schemas.schemas import configSchema
from helpers.typing import validateType, expectedTypeToString
from validators.result import ValidationResult


def validate_config(config) -> ValidationResult:
    result = ValidationResult([])

    def _join_path(base: str, key: str) -> str:
        if not base:
            return key
        return f"{base}.{key}"

    def _validate_node(value, schema, path: str):
        if not isinstance(schema, dict):
            if not validateType(value, schema):
                result.add("error", f"Field '{path}' expected {expectedTypeToString(schema)}")
            return

        required = schema.get("required", {})
        optional = schema.get("optional", {})

        if not isinstance(value, dict):
            result.add("error", f"Field '{path}' must be an object")
            return

        for key, expected in required.items():
            if key not in value:
                container = path if path else "root"
                result.add("error", f"Missing '{key}' in '{container}'")
                continue

            child_path = _join_path(path, key)
            _validate_node(value[key], expected, child_path)

        for key, expected in optional.items():
            if key not in value:
                continue
            child_path = _join_path(path, key)
            _validate_node(value[key], expected, child_path)

        unknown = set(value) - set(required) - set(optional)
        if unknown:
            container = path if path else "root"
            result.add("warning", f"Unknown fields at '{container}': {', '.join(sorted(unknown))}")

    if not isinstance(config, dict):
        result.add("error", "Config must be an object")
        return result

    _validate_node(config, configSchema, "")

    return result
