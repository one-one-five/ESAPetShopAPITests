STORE_JSON = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer",
            "format": "int32"
        },
        "delivered": {
            "type": "integer",
            "format": "int32"
        },
        "placed": {
            "type": "integer",
            "format": "int32"
        }
    },
    "required": ["approved", "delivered", "placed"],
    "additionalProperties": False
}

ORDER_JSON = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "format": "int64"
        },
        "petId": {
            "type": "integer",
            "format": "int64"
        },
        "quantity": {
            "type": "integer",
            "format": "int32"
        },
        "shipDate": {
            "type": "string",
            "format": "date-time"
        },
        "status": {
            "type": "string",
            "enum": ["placed", "approved", "delivered"]
        },
        "complete": {
            "type": "boolean"
        }
    },
    "required": ["id", "petId", "quantity", "status", "complete"],
    "additionalProperties": False
}
