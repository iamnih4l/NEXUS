# seed_data.py
from database import get_connection

conn = get_connection()
c = conn.cursor()

# =========================
# TABLES
# =========================
c.execute("""
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    food_type TEXT,
    quantity INTEGER,
    perishability REAL,
    expiry_days INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS ngos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    capacity INTEGER,
    latitude REAL,
    longitude REAL,
    trust REAL
)
""")

# =========================
# SAMPLE FOOD DATA (10+)
# =========================
foods = [
    ("Apples", "Fruit", 50, 0.3, 7),
    ("Bananas", "Fruit", 40, 0.6, 3),
    ("Tomatoes", "Vegetable", 30, 0.7, 4),
    ("Potatoes", "Vegetable", 100, 0.2, 30),
    ("Bread", "Bakery", 25, 0.5, 2),
    ("Milk", "Dairy", 20, 0.9, 1),
    ("Rice", "Grain", 200, 0.1, 180),
    ("Cooked Meals", "Prepared", 15, 0.95, 1),
    ("Cheese", "Dairy", 10, 0.4, 10),
    ("Yogurt", "Dairy", 18, 0.8, 2)
]

# =========================
# SAMPLE NGO DATA
# =========================
ngos = [
    ("Helping Hands", 30, 12.91, 74.85, 3.8),
    ("Food For All", 50, 12.92, 74.88, 4.2),
    ("Care & Share", 20, 12.89, 74.83, 2.9),
    ("Hope Foundation", 40, 12.95, 74.90, 4.5)
]

# =========================
# INSERT (SAFE)
# =========================
c.executemany("""
INSERT OR IGNORE INTO foods (name, food_type, quantity, perishability, expiry_days)
VALUES (?, ?, ?, ?, ?)
""", foods)

c.executemany("""
INSERT OR IGNORE INTO ngos (name, capacity, latitude, longitude, trust)
VALUES (?, ?, ?, ?, ?)
""", ngos)

conn.commit()
conn.close()

print("✅ Sample food & NGO dataset created successfully.")
