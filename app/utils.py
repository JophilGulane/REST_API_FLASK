import xml.etree.ElementTree as ET
from flask import jsonify


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def validate_class_payload(payload):
    if not isinstance(payload, dict):
        return False, "Invalid payload"
    name = payload.get("name")
    description = payload.get("description", "")
    if not name or not isinstance(name, str):
        return False, "Name is required"
    if description is None:
        description = ""
    return True, {"name": name.strip(), "description": str(description).strip()}


def validate_weapon_payload(payload):
    if not isinstance(payload, dict):
        return False, "Invalid payload"
    name = payload.get("name")
    weapon_type = payload.get("type")
    description = payload.get("description", "")
    if not name or not isinstance(name, str):
        return False, "Name is required"
    if not weapon_type or not isinstance(weapon_type, str):
        return False, "Type is required"
    if description is None:
        description = ""
    return True, {"name": name.strip(), "type": weapon_type.strip(), "description": str(description).strip()}


def validate_stats_payload(payload):
    if not isinstance(payload, dict):
        return False, "Invalid payload"
    fields = ["strength", "intelligence", "dexterity", "stamina", "faith", "agility"]
    values = {}
    for field in fields:
        val = parse_int(payload.get(field))
        if val is None:
            return False, f"{field} is required"
        values[field] = val
    return True, values


def validate_character_payload(payload):
    if not isinstance(payload, dict):
        return False, "Invalid payload"
    name = payload.get("name")
    stat_id = parse_int(payload.get("stat_id"))
    class_id = parse_int(payload.get("class_id"))
    weapon_id = parse_int(payload.get("weapon_id"))
    if not name or not isinstance(name, str):
        return False, "Name is required"
    if stat_id is None or class_id is None or weapon_id is None:
        return False, "stat_id, class_id, and weapon_id are required"
    return True, {"name": name.strip(), "stat_id": stat_id, "class_id": class_id, "weapon_id": weapon_id}


