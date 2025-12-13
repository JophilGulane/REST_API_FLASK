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


def dict_to_xml(tag, data):
    elem = ET.Element(tag)

    def build(parent, key, val):
        if isinstance(val, list):
            list_elem = ET.SubElement(parent, key)
            for item in val:
                item_elem = ET.SubElement(list_elem, "item")
                if isinstance(item, dict):
                    for k, v in item.items():
                        build(item_elem, k, v)
                else:
                    item_elem.text = "" if item is None else str(item)
        elif isinstance(val, dict):
            child = ET.SubElement(parent, key)
            for k, v in val.items():
                build(child, k, v)
        else:
            child = ET.SubElement(parent, key)
            child.text = "" if val is None else str(val)

    if isinstance(data, dict):
        for k, v in data.items():
            build(elem, k, v)
    elif isinstance(data, list):
        for item in data:
            item_elem = ET.SubElement(elem, "item")
            if isinstance(item, dict):
                for k, v in item.items():
                    build(item_elem, k, v)
            else:
                item_elem.text = "" if item is None else str(item)
    else:
        elem.text = "" if data is None else str(data)
    return elem


def format_response(data, status=200, output_format="json"):
    if output_format == "xml":
        root = dict_to_xml("response", data if isinstance(data, (dict, list)) else {"data": data})
        xml_str = ET.tostring(root, encoding="utf-8")
        return xml_str, status, {"Content-Type": "application/xml"}
    return jsonify(data), status


def parse_format(request):
    fmt = request.args.get("format", "json").lower()
    return "xml" if fmt == "xml" else "json"