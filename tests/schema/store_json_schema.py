STORE_JSON = STORE_JSON = {
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
