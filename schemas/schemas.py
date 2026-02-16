"""
Schema definitions used by both configurator and validator.
Divided into:
- Device Schemas
- Address Map Schemas
"""

# ===== DEVICE SCHEMAS =====

# Common fields shared by all device types
requiredDeviceFields = {
    "id": str,
    "type": str,
    "addressMap": str,
    "disabled": bool,
}

requiredDeviceFieldsWithProtocol = {
    **requiredDeviceFields,
    "protocol": ["Modbus TCP/IP", "MQTT", "CANbus"],
}

# Protocol-specific fields
requiredModbusDeviceFields = {
    "ipAddress": str,
    "port": int,
    "slaveId": int,
    "controlMap": str,
}

requiredMQTTDeviceFields = {
    "topic": str,
}

requiredCANbusDeviceFields = {}

# Precharge device-specific fields
requiredPrechargeDeviceFields = {
    "prechargePeriodInSeconds": int,
    "holdonTimeAuxiliaryContactorInSeconds": int,
    "tresholdVoltage": int,
}

# Optional fields per device type
optionalModbusDeviceFields = {
    "forwardMap": str,
    "critical": bool,
    "communicationInterval": (int, float),
    "controlCommands": str,
    "portConfiguration": dict,
}

optionalMQTTDeviceFields = {
    "forward": dict,
}

optionalCANbusDeviceFields = {
    "frameFormat": str
}

optionalDigitalInputOutputDeviceFields = {
    "retainInputs": bool,
    "controlMap": str,
}

optionalAnalogInputOutputDeviceFields = {}

optionalIndicatorsDeviceFields = {
    "controlMap": str,
}

optionalResetDeviceFields = {}

optionalPrechargeDeviceFields = {
    "contactorFeedback": bool,
    "breakerFeedback": bool,
    "maximumVoltage": int,
    "analogMeasurementAddressMap": str,
}

deviceSchemas = {
    "converter": {
        "required": requiredDeviceFieldsWithProtocol,
        "optional": {},
    },
    "battery": {
        "required": requiredDeviceFieldsWithProtocol,
        "optional": {},
    },
    "other": {
        "required": requiredDeviceFieldsWithProtocol,
        "optional": {},
    },
    "digitalInputOutput": {
        "required": requiredDeviceFields,
        "optional": optionalDigitalInputOutputDeviceFields,
    },
    "analogInputOutput": {
        "required": requiredDeviceFields,
        "optional": optionalAnalogInputOutputDeviceFields,
    },
    "indicators": {
        "required": requiredDeviceFields,
        "optional": optionalIndicatorsDeviceFields,
    },
    "reset": {
        "required": requiredDeviceFields,
        "optional": optionalResetDeviceFields,
    },
    "precharge": {
        "required": {**requiredDeviceFields, **requiredPrechargeDeviceFields},
        "optional": optionalPrechargeDeviceFields,
    },
    "breaker": {
        "required": requiredDeviceFields,
        "optional": optionalDigitalInputOutputDeviceFields,
    },
    "contactor": {
        "required": requiredDeviceFields,
        "optional": optionalDigitalInputOutputDeviceFields,
    },
}

# ===== ADDRESS MAP SCHEMAS =====

# Modbus address map schema
requiredModbusAddressFields = {
    "address": int,
    "numberOfRegisters": int,
    "name": str,
    "datatype": ["int8", "uint8", "int16", "uint16", "int32", "uint32", "float32", "int64", "uint64", "float64", "string32"],
    "functionCode": [1, 2, 3, 4, 5, 6, 15, 16],
}

optionalModbusAddressFields = {
    "scaling": (int, float, str),
    "offset": (int, float),
    "direction": ["input", "output"],
    "minimum": (int, float),
    "maximum": (int, float),
    "map": dict,
    "multiRead": bool,
    "wordOrder": ["big", "little"],
    "byteOrder": ["big", "little"],
    "notes": str,
}

# CANbus address map schema
requiredCANbusAddressFields = {
    "canId": int,
    "name": str,
    "startByte": int,
    "startBit": int,
    "bitLength": int,
    "datatype": ["int8", "uint8", "int16", "uint16", "int32", "uint32", "float32", "int64", "uint64", "float64", "string32"],
}

optionalCANbusAddressFields = {
    "scaling": (int, float, str),
    "offset": (int, float),
    "direction": ["input", "output"],
    "minimum": (int, float),
    "maximum": (int, float),
    "map": dict,
    "byteOrder": ["big", "little"],
    "notes": str,
}

# MQTT address map schema
requiredMQTTAddressFields = {
    "name": str,
    "key": str,
    "pathToReadings": str,
    "pathToKey": str,
    "pathToValue": str,
    "valueIncludesUnit": bool,
}

optionalMQTTAddressFields = {}

# Digital I/O address map schema
requiredDioAddressFields = {
    "name": str,
    "address": int,
    "type": ["input", "output"],
}

optionalDioAddressFields = {
    "invert": bool,
    "notes": str,
}

# Analog I/O address map schema
requiredAioAddressFields = {
    "name": str,
    "address": int,
    "type": ["input", "output"],
}

optionalAioAddressFields = {
    "scaling": (int, float),
    "offset": (int, float),
    "notes": str,
}

addressMapSchemas = {
    "Modbus TCP/IP": {
        "required": requiredModbusAddressFields,
        "optional": optionalModbusAddressFields,
    },
    "CANbus": {
        "required": requiredCANbusAddressFields,
        "optional": optionalCANbusAddressFields,
        "constraints": {
            "startByte": {"min": 0, "max": 7},
            "startBit": {"min": 0, "max": 7},
            "bitLength": {"min": 1, "max": 64},
        },
    },
    "MQTT": {
        "required": requiredMQTTAddressFields,
        "optional": optionalMQTTAddressFields,
    },
    "Digital I/O": {
        "required": requiredDioAddressFields,
        "optional": optionalDioAddressFields,
    },
    "Precharge": {
        "required": requiredDioAddressFields,
        "optional": optionalDioAddressFields,
    },
    "Breaker": {
        "required": requiredDioAddressFields,
        "optional": optionalDioAddressFields,
    },
    "Contactor": {
        "required": requiredDioAddressFields,
        "optional": optionalDioAddressFields,
    },
    "Analog I/O": {
        "required": requiredAioAddressFields,
        "optional": optionalAioAddressFields,
    },
}

# Expression schema
expressionSchema = {
    "expression": str,
}

# ===== CONTROL MAP SCHEMA =====

controlMapSchema = {
    "name": str,
    "commands": str,
}

# ===== CONFIG SCHEMA =====

configSchema = {
    "required": {
        "plcnext": {
            "required": {
                "ipAddress": str,
            },
            "optional": {
                "username": str,
                "password": str,
            },
        },
        "mqtt": {
            "required": {
                "broker": {
                    "required": {
                        "ipAddress": str,
                    },
                    "optional": {
                        "port": int,
                    },
                },
            },
            "optional": {},
        },
        "telegram": {
            "required": {
                "chatId": str,
                "botToken": str,
            },
            "optional": {},
        },
        "nats": {
            "required": {
                "local": {
                    "required": {
                        "username": str,
                        "password": str,
                    },
                    "optional": {},
                },
            },
            "optional": {
                "cloud": {
                    "required": {},
                    "optional": {
                        "username": str,
                        "password": str,
                        "ipAddress": str,
                        "bucket": str,
                    },
                },
            },
        },
    },
    "optional": {
        "dcide": {
            "required": {},
            "optional": {
                "baseUrl": str,
                "projectId": str,
                "secret": str,
            },
        },
    },
}