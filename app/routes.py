from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from .utils import (
    format_response,
    parse_format,
    validate_class_payload,
    validate_weapon_payload,
    validate_stats_payload,
    validate_character_payload,
    parse_int,
)
from .query import (
    list_classes,
    get_class,
    create_class,
    update_class,
    delete_class,
    list_weapons,
    get_weapon,
    create_weapon,
    update_weapon,
    delete_weapon,
    list_stats,
    get_stat,
    create_stat,
    update_stat,
    delete_stat,
    list_characters,
    get_character,
    create_character,
    update_character,
    delete_character,
)
from .config import Config


api_bp = Blueprint("api", __name__)


@api_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if username == Config.API_USER and password == Config.API_PASSWORD:
        token = create_access_token(identity=username)
        return {"access_token": token}, 200
    return {"message": "Invalid credentials"}, 401


@api_bp.get("/classes")
@jwt_required()
def get_classes():
    output_format = parse_format(request)
    items = list_classes()
    return format_response({"classes": items}, 200, output_format)


@api_bp.get("/classes/<int:class_id>")
@jwt_required()
def get_class_route(class_id):
    output_format = parse_format(request)
    item = get_class(class_id)
    if not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.post("/classes")
@jwt_required()
def create_class_route():
    output_format = parse_format(request)
    is_valid, result = validate_class_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item = create_class(result["name"], result["description"])
    return format_response(item, 201, output_format)


@api_bp.put("/classes/<int:class_id>")
@jwt_required()
def update_class_route(class_id):
    output_format = parse_format(request)
    is_valid, result = validate_class_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item = update_class(class_id, result["name"], result["description"])
    if not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.delete("/classes/<int:class_id>")
@jwt_required()
def delete_class_route(class_id):
    output_format = parse_format(request)
    success, reason = delete_class(class_id)
    if not success and reason == "not_found":
        return format_response({"message": "Not found"}, 404, output_format)
    if not success and reason == "in_use":
        return format_response({"message": "Class is referenced by characters"}, 400, output_format)
    return format_response({"deleted": True}, 200, output_format)


@api_bp.get("/weapons")
@jwt_required()
def get_weapons():
    output_format = parse_format(request)
    items = list_weapons()
    return format_response({"weapons": items}, 200, output_format)


@api_bp.get("/weapons/<int:weapon_id>")
@jwt_required()
def get_weapon_route(weapon_id):
    output_format = parse_format(request)
    item = get_weapon(weapon_id)
    if not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.post("/weapons")
@jwt_required()
def create_weapon_route():
    output_format = parse_format(request)
    is_valid, result = validate_weapon_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item = create_weapon(result["name"], result["type"], result["description"])
    return format_response(item, 201, output_format)


@api_bp.put("/weapons/<int:weapon_id>")
@jwt_required()
def update_weapon_route(weapon_id):
    output_format = parse_format(request)
    is_valid, result = validate_weapon_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item = update_weapon(weapon_id, result["name"], result["type"], result["description"])
    if not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.delete("/weapons/<int:weapon_id>")
@jwt_required()
def delete_weapon_route(weapon_id):
    output_format = parse_format(request)
    success, reason = delete_weapon(weapon_id)
    if not success and reason == "not_found":
        return format_response({"message": "Not found"}, 404, output_format)
    if not success and reason == "in_use":
        return format_response({"message": "Weapon is referenced by characters"}, 400, output_format)
    return format_response({"deleted": True}, 200, output_format)


@api_bp.get("/stats")
@jwt_required()
def get_stats_route():
    output_format = parse_format(request)
    items = list_stats()
    return format_response({"stats": items}, 200, output_format)


@api_bp.get("/stats/<int:stat_id>")
@jwt_required()
def get_stat_route(stat_id):
    output_format = parse_format(request)
    item = get_stat(stat_id)
    if not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.post("/stats")
@jwt_required()
def create_stat_route():
    output_format = parse_format(request)
    is_valid, result = validate_stats_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item = create_stat(result)
    return format_response(item, 201, output_format)


@api_bp.put("/stats/<int:stat_id>")
@jwt_required()
def update_stat_route(stat_id):
    output_format = parse_format(request)
    is_valid, result = validate_stats_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item = update_stat(stat_id, result)
    if not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.delete("/stats/<int:stat_id>")
@jwt_required()
def delete_stat_route(stat_id):
    output_format = parse_format(request)
    success, reason = delete_stat(stat_id)
    if not success and reason == "not_found":
        return format_response({"message": "Not found"}, 404, output_format)
    if not success and reason == "in_use":
        return format_response({"message": "Stats are referenced by characters"}, 400, output_format)
    return format_response({"deleted": True}, 200, output_format)


@api_bp.get("/characters")
@jwt_required()
def get_characters_route():
    output_format = parse_format(request)
    filters = {
        "name": request.args.get("q"),
        "class_id": parse_int(request.args.get("class_id")),
        "weapon_id": parse_int(request.args.get("weapon_id")),
        "strength_min": parse_int(request.args.get("strength_min")),
        "intelligence_min": parse_int(request.args.get("intelligence_min")),
        "dexterity_min": parse_int(request.args.get("dexterity_min")),
        "stamina_min": parse_int(request.args.get("stamina_min")),
        "faith_min": parse_int(request.args.get("faith_min")),
        "agility_min": parse_int(request.args.get("agility_min")),
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    items = list_characters(filters)
    return format_response({"characters": items}, 200, output_format)


@api_bp.get("/characters/<int:character_id>")
@jwt_required()
def get_character_route(character_id):
    output_format = parse_format(request)
    item = get_character(character_id)
    if not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.post("/characters")
@jwt_required()
def create_character_route():
    output_format = parse_format(request)
    is_valid, result = validate_character_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item, error = create_character(result["name"], result["stat_id"], result["class_id"], result["weapon_id"])
    if error == "invalid_foreign":
        return format_response({"message": "Invalid foreign key"}, 400, output_format)
    return format_response(item, 201, output_format)


@api_bp.put("/characters/<int:character_id>")
@jwt_required()
def update_character_route(character_id):
    output_format = parse_format(request)
    is_valid, result = validate_character_payload(request.get_json(silent=True) or {})
    if not is_valid:
        return format_response({"message": result}, 400, output_format)
    item, error = update_character(character_id, result["name"], result["stat_id"], result["class_id"], result["weapon_id"])
    if error == "invalid_foreign":
        return format_response({"message": "Invalid foreign key"}, 400, output_format)
    if error == "not_found" or not item:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response(item, 200, output_format)


@api_bp.delete("/characters/<int:character_id>")
@jwt_required()
def delete_character_route(character_id):
    output_format = parse_format(request)
    success = delete_character(character_id)
    if not success:
        return format_response({"message": "Not found"}, 404, output_format)
    return format_response({"deleted": True}, 200, output_format)