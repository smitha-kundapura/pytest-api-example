pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
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
    "required": [ "id","pet_id"],
    "properties": {
        "id": {"type": "string"},
        "pet_id": {"type": ["string", "integer"]},
        "status": {"type": "string", "enum": ["available", "sold", "pending"]}
    }
}
