from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ValidationMessage:
    """
    Single validation message produced by a validator.
    """
    level: str     # "error", "warning", "success"
    message: str

@dataclass
class ValidationResult:
    """
    Aggregated validation result for a file or validation unit.
    """
    messages: List[ValidationMessage]
    has_errors: bool = False
    has_warnings: bool = False

    def add(self, level: str, message: str):
        self.messages.append(ValidationMessage(level, message))
        if level == "error":
            self.has_errors = True
        if level == "warning":
            self.has_warnings = True

def merge_validation_results(*results: ValidationResult) -> ValidationResult:
    messages: List[ValidationMessage] = []
    has_errors = False
    has_warnings = False

    for r in results:
        if r is None:
            continue
        messages.extend(r.messages)
        has_errors = has_errors or r.has_errors
        has_warnings = has_warnings or r.has_warnings

    return ValidationResult(messages, has_errors, has_warnings)
