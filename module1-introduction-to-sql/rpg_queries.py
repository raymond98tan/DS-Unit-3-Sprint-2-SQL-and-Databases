import sqlite3


def connect_to_db(db_name='rpg_db.sqlite3'):
    return sqlite3.connect(db_name)


def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


GET_CHARACTERS = """
  SELECT COUNT(*)
  FROM CHARACTERCREATOR_character;
  """

mage = """
  SELECT COUNT(*)
  FROM charactercreator_mage;
"""

thief = """
  SELECT COUNT(*)
  FROM charactercreator_thief;
"""

cleric = """
  SELECT COUNT(*)
  FROM charactercreator_cleric;
"""

fighter = """
  SELECT COUNT(*)
  FROM charactercreator_fighter;
"""

necromancer = """
  SELECT COUNT(*)
  FROM charactercreator_necromancer;
"""

num_items = """
  SELECT COUNT(*)
  FROM armory_item;
"""

num_weapons = """
  SELECT COUNT(*)
  FROM armory_weapon;
"""

num_not_weapons = """
  SELECT COUNT(*) FROM armory_item
  LEFT JOIN armory_weapon
  ON item_ptr_id = item_id
  WHERE power IS NULL;
"""

char_items = """
  SELECT c.name, COUNT(distinct inv.item_id) as item_count FROM charactercreator_character c
  LEFT JOIN charactercreator_character_inventory inv
  ON c.character_id = inv.character_id
  GROUP BY c.name
  ORDER BY COUNT(inv.item_id) DESC
  LIMIT 20;
"""

char_weapons = """
  SELECT c.character_id, COUNT(distinct w.item_ptr_id) as weapon_count 
  FROM charactercreator_character as c
  LEFT JOIN charactercreator_character_inventory inv
  ON c.character_id = inv.character_id
  LEFT JOIN armory_weapon w 
  ON inv.item_id = w.item_ptr_id
  GROUP BY c.character_id
  ORDER BY weapon_count DESC
  LIMIT 20;
"""

avg_item = """
SELECT AVG(item_count) as avg_item_count
FROM(
    SELECT c.name, COUNT(distinct inv.item_id) as item_count 
    FROM charactercreator_character c
    LEFT JOIN charactercreator_character_inventory inv
    ON c.character_id = inv.character_id
    GROUP BY c.name
  ) sub
"""

avg_weapon = """
  SELECT AVG(weapon_count) as avg_weapon
  FROM(
    SELECT c.character_id, COUNT(distinct w.item_ptr_id) as weapon_count 
    FROM charactercreator_character c
    LEFT JOIN charactercreator_character_inventory inv
    ON c.character_id = inv.character_id
    LEFT JOIN armory_weapon w 
    ON inv.item_id = w.item_ptr_id
    GROUP BY c.character_id
  )
"""

if __name__ == "__main__":
    conn = connect_to_db()
    curs = conn.cursor()
    results1 = execute_query(curs, GET_CHARACTERS)
    mages = execute_query(curs, mage)
    thiefs = execute_query(curs, thief)
    clerics = execute_query(curs, cleric)
    fighters = execute_query(curs, fighter)
    necromancers = execute_query(curs, necromancer)
    items = execute_query(curs, num_items)
    weapons = execute_query(curs, num_weapons)
    non_weapons = execute_query(curs, num_not_weapons)
    character_items = execute_query(curs, char_items)
    character_weapons = execute_query(curs, char_weapons)
    avg_items = execute_query(curs, avg_item)
    avg_weapons = execute_query(curs, avg_weapon)
    print('Total Characters: ', results1)
    print('Subclasses: ', mages, thiefs, clerics, fighters, necromancers)
    print('Total Items: ', items)
    print('Number of Weapons and non-weapons: ', weapons, non_weapons)
    print('Number of Items each character has (first 20):', character_items)
    print('Number of weapons each character has (first 20) ', character_weapons)
    print('Average number of items a character has: ', avg_items)
    print('Average number of weapons a character has: ', avg_weapons)