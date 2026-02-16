def validateType(value, expectedType):
    if isinstance(expectedType, list):
        return value in expectedType
    return isinstance(value, expectedType)

def expectedTypeToString(expectedType):
    if isinstance(expectedType, tuple):
        return ", ".join([type.__name__ for type in expectedType])
    elif isinstance(expectedType, list):
        return ", ".join([type for type in expectedType])
    else:
        return expectedType.__name__

def formatActualValue(value, expectedType):
    if isinstance(expectedType, list):
        return value
    else:
        return type(value).__name__