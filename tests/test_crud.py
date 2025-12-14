import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app import routes as routes_module


@pytest.fixture(autouse=True)
def mock_queries(monkeypatch):
    classes = [{"id": 1, "name": "Knight", "description": "Heavy"}, {"id": 2, "name": "Mage", "description": "Magic"}]
    weapons = [{"id": 1, "name": "Sword", "type": "Melee", "description": "Sharp"}, {"id": 2, "name": "Staff", "type": "Magic", "description": "Wood"}]
    stats = [
        {"id": 1, "strength": 15, "intelligence": 5, "dexterity": 8, "stamina": 12, "faith": 4, "agility": 6},
        {"id": 2, "strength": 6, "intelligence": 14, "dexterity": 9, "stamina": 8, "faith": 10, "agility": 7},
    ]
    characters = [
        {"id": 1, "name": "Artorias", "stat_id": 1, "class_id": 1, "weapon_id": 1},
        {"id": 2, "name": "Lucatiel", "stat_id": 2, "class_id": 2, "weapon_id": 2},
    ]

    def next_id(items):
        return max((item["id"] for item in items), default=0) + 1

    def list_classes():
        return list(classes)

    def get_class(class_id):
        return next((c for c in classes if c["id"] == class_id), None)

    def create_class(name, description):
        item = {"id": next_id(classes), "name": name, "description": description}
        classes.append(item)
        return item

    def update_class(class_id, name, description):
        item = get_class(class_id)
        if not item:
            return None
        item.update({"name": name, "description": description})
        return item

    def delete_class(class_id):
        if not get_class(class_id):
            return False, "not_found"
        if any(ch["class_id"] == class_id for ch in characters):
            return False, "in_use"
        classes[:] = [c for c in classes if c["id"] != class_id]
        return True, ""

    def list_weapons():
        return list(weapons)

    def get_weapon(weapon_id):
        return next((w for w in weapons if w["id"] == weapon_id), None)

    def create_weapon(name, weapon_type, description):
        item = {"id": next_id(weapons), "name": name, "type": weapon_type, "description": description}
        weapons.append(item)
        return item

    def update_weapon(weapon_id, name, weapon_type, description):
        item = get_weapon(weapon_id)
        if not item:
            return None
        item.update({"name": name, "type": weapon_type, "description": description})
        return item

    def delete_weapon(weapon_id):
        if not get_weapon(weapon_id):
            return False, "not_found"
        if any(ch["weapon_id"] == weapon_id for ch in characters):
            return False, "in_use"
        weapons[:] = [w for w in weapons if w["id"] != weapon_id]
        return True, ""

    def list_stats():
        return list(stats)

    def get_stat(stat_id):
        return next((s for s in stats if s["id"] == stat_id), None)

    def create_stat(values):
        item = {"id": next_id(stats), **values}
        stats.append(item)
        return item

    def update_stat(stat_id, values):
        item = get_stat(stat_id)
        if not item:
            return None
        item.update(values)
        return item

    def delete_stat(stat_id):
        if not get_stat(stat_id):
            return False, "not_found"
        if any(ch["stat_id"] == stat_id for ch in characters):
            return False, "in_use"
        stats[:] = [s for s in stats if s["id"] != stat_id]
        return True, ""

    def list_characters(filters=None):
        filters = filters or {}
        result = list(characters)
        if filters.get("name"):
            term = filters["name"].lower()
            result = [c for c in result if term in c["name"].lower()]
        if filters.get("class_id") is not None:
            result = [c for c in result if c["class_id"] == filters["class_id"]]
        if filters.get("weapon_id") is not None:
            result = [c for c in result if c["weapon_id"] == filters["weapon_id"]]
        for stat_field in ["strength", "intelligence", "dexterity", "stamina", "faith", "agility"]:
            key = f"{stat_field}_min"
            if filters.get(key) is not None:
                result = [c for c in result if next(s for s in stats if s["id"] == c["stat_id"])[stat_field] >= filters[key]]
        return list(result)

    def get_character(character_id):
        return next((c for c in characters if c["id"] == character_id), None)

    def create_character(name, stat_id, class_id, weapon_id):
        if not get_stat(stat_id) or not get_class(class_id) or not get_weapon(weapon_id):
            return None, "invalid_foreign"
        item = {"id": next_id(characters), "name": name, "stat_id": stat_id, "class_id": class_id, "weapon_id": weapon_id}
        characters.append(item)
        return item, None

    def update_character(character_id, name, stat_id, class_id, weapon_id):
        if not get_stat(stat_id) or not get_class(class_id) or not get_weapon(weapon_id):
            return None, "invalid_foreign"
        item = get_character(character_id)
        if not item:
            return None, "not_found"
        item.update({"name": name, "stat_id": stat_id, "class_id": class_id, "weapon_id": weapon_id})
        return item, None

    def delete_character(character_id):
        item = get_character(character_id)
        if not item:
            return False
        characters[:] = [c for c in characters if c["id"] != character_id]
        return True

    monkeypatch.setattr(routes_module, "list_classes", list_classes)
    monkeypatch.setattr(routes_module, "get_class", get_class)
    monkeypatch.setattr(routes_module, "create_class", create_class)
    monkeypatch.setattr(routes_module, "update_class", update_class)
    monkeypatch.setattr(routes_module, "delete_class", delete_class)
    monkeypatch.setattr(routes_module, "list_weapons", list_weapons)
    monkeypatch.setattr(routes_module, "get_weapon", get_weapon)
    monkeypatch.setattr(routes_module, "create_weapon", create_weapon)
    monkeypatch.setattr(routes_module, "update_weapon", update_weapon)
    monkeypatch.setattr(routes_module, "delete_weapon", delete_weapon)
    monkeypatch.setattr(routes_module, "list_stats", list_stats)
    monkeypatch.setattr(routes_module, "get_stat", get_stat)
    monkeypatch.setattr(routes_module, "create_stat", create_stat)
    monkeypatch.setattr(routes_module, "update_stat", update_stat)
    monkeypatch.setattr(routes_module, "delete_stat", delete_stat)
    monkeypatch.setattr(routes_module, "list_characters", list_characters)
    monkeypatch.setattr(routes_module, "get_character", get_character)
    monkeypatch.setattr(routes_module, "create_character", create_character)
    monkeypatch.setattr(routes_module, "update_character", update_character)
    monkeypatch.setattr(routes_module, "delete_character", delete_character)


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def auth_token(client):
    resp = client.post("/api/login", json={"username": "admin", "password": "password"})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]


def test_login_failure(client):
    resp = client.post("/api/login", json={"username": "x", "password": "y"})
    assert resp.status_code == 401


def test_requires_auth(client):
    resp = client.get("/api/classes")
    assert resp.status_code == 401


def test_list_classes_json(client):
    token = auth_token(client)
    resp = client.get("/api/classes", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert "classes" in resp.get_json()


def test_create_update_delete_class(client):
    token = auth_token(client)
    create_resp = client.post("/api/classes", json={"name": "Rogue", "description": "Fast"}, headers={"Authorization": f"Bearer {token}"})
    assert create_resp.status_code == 201
    class_id = create_resp.get_json()["id"]
    update_resp = client.put(f"/api/classes/{class_id}", json={"name": "Rogue+", "description": "Faster"}, headers={"Authorization": f"Bearer {token}"})
    assert update_resp.status_code == 200
    delete_resp = client.delete(f"/api/classes/{class_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_resp.status_code == 200


def test_delete_class_in_use(client):
    token = auth_token(client)
    resp = client.delete("/api/classes/1", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400


def test_weapon_crud(client):
    token = auth_token(client)
    create_resp = client.post("/api/weapons", json={"name": "Bow", "type": "Ranged", "description": "Arrows"}, headers={"Authorization": f"Bearer {token}"})
    assert create_resp.status_code == 201
    weapon_id = create_resp.get_json()["id"]
    update_resp = client.put(f"/api/weapons/{weapon_id}", json={"name": "Longbow", "type": "Ranged", "description": "Long range"}, headers={"Authorization": f"Bearer {token}"})
    assert update_resp.status_code == 200
    delete_resp = client.delete(f"/api/weapons/{weapon_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_resp.status_code == 200


def test_delete_weapon_in_use(client):
    token = auth_token(client)
    resp = client.delete("/api/weapons/1", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400


def test_stats_validation_and_crud(client):
    token = auth_token(client)
    invalid_resp = client.post("/api/stats", json={"strength": "x"}, headers={"Authorization": f"Bearer {token}"})
    assert invalid_resp.status_code == 400
    payload = {"strength": 10, "intelligence": 10, "dexterity": 10, "stamina": 10, "faith": 10, "agility": 10}
    create_resp = client.post("/api/stats", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert create_resp.status_code == 201
    stat_id = create_resp.get_json()["id"]
    update_resp = client.put(f"/api/stats/{stat_id}", json={**payload, "strength": 12}, headers={"Authorization": f"Bearer {token}"})
    assert update_resp.status_code == 200
    delete_resp = client.delete(f"/api/stats/{stat_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_resp.status_code == 200


def test_delete_stat_in_use(client):
    token = auth_token(client)
    resp = client.delete("/api/stats/1", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400


def test_character_create_invalid_foreign(client):
    token = auth_token(client)
    resp = client.post("/api/characters", json={"name": "Bad", "stat_id": 999, "class_id": 1, "weapon_id": 1}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400


def test_character_search_and_xml(client):
    token = auth_token(client)
    resp_json = client.get("/api/characters?q=Arto", headers={"Authorization": f"Bearer {token}"})
    assert resp_json.status_code == 200
    assert len(resp_json.get_json()["characters"]) == 1
    resp_xml = client.get("/api/characters?format=xml&strength_min=10", headers={"Authorization": f"Bearer {token}"})
    assert resp_xml.status_code == 200
    assert b"<characters>" in resp_xml.data or b"<item>" in resp_xml.data


def test_character_full_crud(client):
    token = auth_token(client)
    create_resp = client.post("/api/characters", json={"name": "NewChar", "stat_id": 1, "class_id": 1, "weapon_id": 1}, headers={"Authorization": f"Bearer {token}"})
    assert create_resp.status_code == 201
    char_id = create_resp.get_json()["id"]
    update_resp = client.put(f"/api/characters/{char_id}", json={"name": "UpdatedChar", "stat_id": 2, "class_id": 2, "weapon_id": 2}, headers={"Authorization": f"Bearer {token}"})
    assert update_resp.status_code == 200
    delete_resp = client.delete(f"/api/characters/{char_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_resp.status_code == 200
    resp_not_found = client.get(f"/api/characters/{char_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp_not_found.status_code == 404

