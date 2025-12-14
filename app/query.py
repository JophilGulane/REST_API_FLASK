from typing import List, Optional, Dict, Any
from .database import get_cursor


def record_exists(table: str, record_id: int) -> bool:
    conn, cursor = get_cursor()
    try:
        cursor.execute(f"SELECT id FROM {table} WHERE id = %s", (record_id,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()


def characters_in_use(field: str, value: int) -> bool:
    conn, cursor = get_cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) AS cnt FROM characters WHERE {field} = %s", (value,))
        row = cursor.fetchone()
        return row["cnt"] > 0
    finally:
        cursor.close()
        conn.close()


def row_class(row: Dict[str, Any]) -> Dict[str, Any]:
    return {"id": row["id"], "name": row["name"], "description": row["description"]}


def row_weapon(row: Dict[str, Any]) -> Dict[str, Any]:
    return {"id": row["id"], "name": row["name"], "type": row["type"], "description": row["description"]}


def row_stat(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "strength": row["strength"],
        "intelligence": row["intelligence"],
        "dexterity": row["dexterity"],
        "stamina": row["stamina"],
        "faith": row["faith"],
        "agility": row["agility"],
    }


def row_character(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "stat_id": row["stat_id"],
        "class_id": row["class_id"],
        "weapon_id": row["weapon_id"],
    }


def list_classes() -> List[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, name, description FROM classes ORDER BY id")
        return [row_class(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()


def get_class(class_id: int) -> Optional[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, name, description FROM classes WHERE id = %s", (class_id,))
        row = cursor.fetchone()
        return row_class(row) if row else None
    finally:
        cursor.close()
        conn.close()


def create_class(name: str, description: str) -> Dict[str, Any]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("INSERT INTO classes (name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        return get_class(cursor.lastrowid)
    finally:
        cursor.close()
        conn.close()


def update_class(class_id: int, name: str, description: str) -> Optional[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("UPDATE classes SET name = %s, description = %s WHERE id = %s", (name, description, class_id))
        conn.commit()
        if cursor.rowcount == 0:
            return None
        return get_class(class_id)
    finally:
        cursor.close()
        conn.close()


def delete_class(class_id: int) -> (bool, str):
    if not record_exists("classes", class_id):
        return False, "not_found"
    if characters_in_use("class_id", class_id):
        return False, "in_use"
    conn, cursor = get_cursor()
    try:
        cursor.execute("DELETE FROM classes WHERE id = %s", (class_id,))
        conn.commit()
        return cursor.rowcount > 0, ""
    finally:
        cursor.close()
        conn.close()


def list_weapons() -> List[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, name, type, description FROM weapons ORDER BY id")
        return [row_weapon(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()


def get_weapon(weapon_id: int) -> Optional[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, name, type, description FROM weapons WHERE id = %s", (weapon_id,))
        row = cursor.fetchone()
        return row_weapon(row) if row else None
    finally:
        cursor.close()
        conn.close()


def create_weapon(name: str, weapon_type: str, description: str) -> Dict[str, Any]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("INSERT INTO weapons (name, type, description) VALUES (%s, %s, %s)", (name, weapon_type, description))
        conn.commit()
        return get_weapon(cursor.lastrowid)
    finally:
        cursor.close()
        conn.close()


def update_weapon(weapon_id: int, name: str, weapon_type: str, description: str) -> Optional[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("UPDATE weapons SET name = %s, type = %s, description = %s WHERE id = %s", (name, weapon_type, description, weapon_id))
        conn.commit()
        if cursor.rowcount == 0:
            return None
        return get_weapon(weapon_id)
    finally:
        cursor.close()
        conn.close()


def delete_weapon(weapon_id: int) -> (bool, str):
    if not record_exists("weapons", weapon_id):
        return False, "not_found"
    if characters_in_use("weapon_id", weapon_id):
        return False, "in_use"
    conn, cursor = get_cursor()
    try:
        cursor.execute("DELETE FROM weapons WHERE id = %s", (weapon_id,))
        conn.commit()
        return cursor.rowcount > 0, ""
    finally:
        cursor.close()
        conn.close()


def list_stats() -> List[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, strength, intelligence, dexterity, stamina, faith, agility FROM stats ORDER BY id")
        return [row_stat(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()


def get_stat(stat_id: int) -> Optional[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, strength, intelligence, dexterity, stamina, faith, agility FROM stats WHERE id = %s", (stat_id,))
        row = cursor.fetchone()
        return row_stat(row) if row else None
    finally:
        cursor.close()
        conn.close()


def create_stat(values: Dict[str, int]) -> Dict[str, Any]:
    conn, cursor = get_cursor()
    try:
        cursor.execute(
            "INSERT INTO stats (strength, intelligence, dexterity, stamina, faith, agility) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                values["strength"],
                values["intelligence"],
                values["dexterity"],
                values["stamina"],
                values["faith"],
                values["agility"],
            ),
        )
        conn.commit()
        return get_stat(cursor.lastrowid)
    finally:
        cursor.close()
        conn.close()


def update_stat(stat_id: int, values: Dict[str, int]) -> Optional[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute(
            "UPDATE stats SET strength = %s, intelligence = %s, dexterity = %s, stamina = %s, faith = %s, agility = %s WHERE id = %s",
            (
                values["strength"],
                values["intelligence"],
                values["dexterity"],
                values["stamina"],
                values["faith"],
                values["agility"],
                stat_id,
            ),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None
        return get_stat(stat_id)
    finally:
        cursor.close()
        conn.close()


def delete_stat(stat_id: int) -> (bool, str):
    if not record_exists("stats", stat_id):
        return False, "not_found"
    if characters_in_use("stat_id", stat_id):
        return False, "in_use"
    conn, cursor = get_cursor()
    try:
        cursor.execute("DELETE FROM stats WHERE id = %s", (stat_id,))
        conn.commit()
        return cursor.rowcount > 0, ""
    finally:
        cursor.close()
        conn.close()


def list_characters(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    filters = filters or {}
    join_stats = any(filters.get(f"{stat}_min") is not None for stat in ["strength", "intelligence", "dexterity", "stamina", "faith", "agility"])
    query = "SELECT c.id, c.name, c.stat_id, c.class_id, c.weapon_id FROM characters c"
    if join_stats:
        query += " JOIN stats s ON c.stat_id = s.id"
    conditions = []
    params = []
    if filters.get("name"):
        conditions.append("c.name LIKE %s")
        params.append(f"%{filters['name']}%")
    if filters.get("class_id") is not None:
        conditions.append("c.class_id = %s")
        params.append(filters["class_id"])
    if filters.get("weapon_id") is not None:
        conditions.append("c.weapon_id = %s")
        params.append(filters["weapon_id"])
    for stat in ["strength", "intelligence", "dexterity", "stamina", "faith", "agility"]:
        key = f"{stat}_min"
        if filters.get(key) is not None:
            conditions.append(f"s.{stat} >= %s")
            params.append(filters[key])
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY c.id"
    conn, cursor = get_cursor()
    try:
        cursor.execute(query, tuple(params))
        return [row_character(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()


def get_character(character_id: int) -> Optional[Dict[str, Any]]:
    conn, cursor = get_cursor()
    try:
        cursor.execute("SELECT id, name, stat_id, class_id, weapon_id FROM characters WHERE id = %s", (character_id,))
        row = cursor.fetchone()
        return row_character(row) if row else None
    finally:
        cursor.close()
        conn.close()


def create_character(name: str, stat_id: int, class_id: int, weapon_id: int) -> (Optional[Dict[str, Any]], Optional[str]):
    if not record_exists("stats", stat_id) or not record_exists("classes", class_id) or not record_exists("weapons", weapon_id):
        return None, "invalid_foreign"
    conn, cursor = get_cursor()
    try:
        cursor.execute("INSERT INTO characters (name, stat_id, class_id, weapon_id) VALUES (%s, %s, %s, %s)", (name, stat_id, class_id, weapon_id))
        conn.commit()
        return get_character(cursor.lastrowid), None
    finally:
        cursor.close()
        conn.close()


def update_character(character_id: int, name: str, stat_id: int, class_id: int, weapon_id: int) -> (Optional[Dict[str, Any]], Optional[str]):
    if not record_exists("stats", stat_id) or not record_exists("classes", class_id) or not record_exists("weapons", weapon_id):
        return None, "invalid_foreign"
    conn, cursor = get_cursor()
    try:
        cursor.execute(
            "UPDATE characters SET name = %s, stat_id = %s, class_id = %s, weapon_id = %s WHERE id = %s",
            (name, stat_id, class_id, weapon_id, character_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None, "not_found"
        return get_character(character_id), None
    finally:
        cursor.close()
        conn.close()


def delete_character(character_id: int) -> bool:
    conn, cursor = get_cursor()
    try:
        cursor.execute("DELETE FROM characters WHERE id = %s", (character_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()