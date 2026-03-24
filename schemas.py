pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "integer"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        },
    }
}

order = {
    "type": "object",
    "required": ["pet_id"],
    "properties": {
        "id": {
            "type": "string",
            "description": "The order ID (UUID)"
        },
        "pet_id": {
            "type": "integer",
            "description": "The ID of the pet in the order"
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"],
            "description": "The status of the order"
        }
    }
}
