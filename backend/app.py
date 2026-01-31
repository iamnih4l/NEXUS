from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import date, timedelta
import math
import random
from typing import List
from pydantic import BaseModel
from datetime import datetime


# =============================
# APP SETUP
# =============================
app = FastAPI(title="NexusGo Backend – Trust & Risk Aware Allocation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "NexusGo backend running",
        "message": "Decision Intelligence API is live"
    }

# Priority alert structure
class PriorityAlert(BaseModel):
    message: str
    level: str  # 'urgent', 'warning', 'info'
    timestamp: str

# In-memory storage for priority messages
priority_alerts: List[PriorityAlert] = []

# =============================
# DATABASE CONNECTION
# =============================
conn = sqlite3.connect("nexusgo.db", check_same_thread=False)
conn.row_factory = sqlite3.Row 
c = conn.cursor()

# =============================
# DATABASE SCHEMA
# =============================
c.execute("""
CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    food_type TEXT,
    quantity INTEGER,
    perishability REAL,
    uncertainty REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS ngos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    trust REAL,
    capacity INTEGER,
    latitude REAL,
    longitude REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS farms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    latitude REAL,
    longitude REAL,
    capacity INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS allocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_name TEXT,
    receiver TEXT,
    quantity INTEGER,
    decision TEXT,
    allocation_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS rewards (
    ngo_name TEXT PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    streak INTEGER DEFAULT 0,
    last_donation TEXT,
    total_allocations INTEGER DEFAULT 0
)
""")

conn.commit()

# =============================
# PREPOPULATE SAMPLE DATA
# =============================
def prepopulate():
    # Resources
    c.execute("SELECT COUNT(*) FROM resources")
    if c.fetchone()[0] == 0:
        resources = [
            ("Milk", "Dairy", 10, 0.95, 0.1),
            ("Bread", "Bakery", 15, 0.3, 0.05),
            ("Tomatoes", "Vegetable", 12, 0.7, 0.2),
            ("Rice", "Grain", 20, 0.1, 0.05),
            ("Eggs", "Poultry", 18, 0.9, 0.15),
            ("Cheese", "Dairy", 8, 0.85, 0.1),
            ("Carrots", "Vegetable", 14, 0.6, 0.1),
            ("Apples", "Fruit", 25, 0.5, 0.05),
            ("Yogurt", "Dairy", 12, 0.95, 0.1),
            ("Lettuce", "Vegetable", 10, 0.8, 0.2)
        ]
        c.executemany("INSERT INTO resources (name, food_type, quantity, perishability, uncertainty) VALUES (?, ?, ?, ?, ?)", resources)

    # NGOs
    c.execute("SELECT COUNT(*) FROM ngos")
    if c.fetchone()[0] == 0:
        ngos = [
            ("Helping Hands", 4.2, 10, 12.91, 74.85),
            ("Food For All", 3.8, 8, 12.89, 74.87),
            ("Care & Share", 2.9, 6, 12.88, 74.83),
        ]
        c.executemany("INSERT INTO ngos (name, trust, capacity, latitude, longitude) VALUES (?, ?, ?, ?, ?)", ngos)

        for ngo in ngos:
            c.execute("INSERT OR IGNORE INTO rewards (ngo_name) VALUES (?)", (ngo[0],))

    # Farms
    c.execute("SELECT COUNT(*) FROM farms")
    if c.fetchone()[0] == 0:
        farms = [
            ("GreenCycle Farm", 12.86, 74.90, 100),
            ("BioGrow Unit", 12.84, 74.88, 80)
        ]
        c.executemany("INSERT INTO farms (name, latitude, longitude, capacity) VALUES (?, ?, ?, ?)", farms)

    conn.commit()

prepopulate()

# =============================
# MODELS
# =============================
class PriorityAlert(BaseModel):
    id: int
    title: str
    message: str
    severity: str  # LOW | MEDIUM | HIGH | CRITICAL
    created_at: str
priority_alerts: List[PriorityAlert] = [
    PriorityAlert(
        id=1,
        title="Flood Emergency – Coastal Region",
        message="Severe flooding reported. Food redistribution to affected zones is prioritized.",
        severity="CRITICAL",
        created_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ),
    PriorityAlert(
        id=2,
        title="Heatwave Alert",
        message="Extreme temperatures expected. Perishable food must be allocated urgently.",
        severity="HIGH",
        created_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )
]

class Resource(BaseModel):
    name: str
    food_type: str
    quantity: int
    perishability: float
    uncertainty: float

class NGO(BaseModel):
    name: str
    trust: float
    capacity: int
    latitude: float
    longitude: float

# =============================
# HELPERS
# =============================
def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def calculate_level(xp):
    return (xp // 100) + 1

def update_rewards(ngo_name, qty):
    today = date.today().isoformat()
    cur = conn.cursor()   # NEW CURSOR

    cur.execute("""
        SELECT xp, streak, last_donation, total_allocations
        FROM rewards WHERE ngo_name=?
    """, (ngo_name,))
    row = cur.fetchone()

    xp, streak, last, total = row if row else (0, 0, None, 0)

    if last == (date.today() - timedelta(days=1)).isoformat():
        streak += 1
    elif last != today:
        streak = 1

    xp += qty * 10
    total += qty
    level = calculate_level(xp)

    cur.execute("""
        UPDATE rewards
        SET xp=?, level=?, streak=?, last_donation=?, total_allocations=?
        WHERE ngo_name=?
    """, (xp, level, streak, today, total, ngo_name))

    cur.execute("""
        UPDATE ngos SET trust = MIN(trust + 0.03, 5.0)
        WHERE name=?
    """, (ngo_name,))

    conn.commit()

# =============================
# ENDPOINTS
# =============================

# --- Add Resource ---
@app.get("/priority_alerts")
def get_priority_alerts():
    return priority_alerts

class PriorityAlertCreate(BaseModel):
    title: str
    message: str
    severity: str


@app.post("/priority_alerts")
def create_priority_alert(alert: PriorityAlertCreate):
    new_alert = PriorityAlert(
        id=len(priority_alerts) + 1,
        title=alert.title,
        message=alert.message,
        severity=alert.severity.upper(),
        created_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )
    priority_alerts.insert(0, new_alert)  # newest first
    return {"status": "alert_created", "alert": new_alert}


@app.post("/add_resource")
def add_resource(res: Resource):
    c.execute("INSERT INTO resources (name, food_type, quantity, perishability, uncertainty) VALUES (?, ?, ?, ?, ?)",
              (res.name, res.food_type, res.quantity, res.perishability, res.uncertainty))
    conn.commit()
    return {"status": "Resource added"}

# --- Add NGO ---
@app.post("/add_ngo")
def add_ngo(ngo: NGO):
    c.execute("INSERT INTO ngos (name, trust, capacity, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
              (ngo.name, ngo.trust, ngo.capacity, ngo.latitude, ngo.longitude))
    c.execute("INSERT OR IGNORE INTO rewards (ngo_name) VALUES (?)", (ngo.name,))
    conn.commit()
    return {"status": "NGO added"}

# --- Get Resources ---
@app.get("/resources")
def get_resources():
    c.execute("SELECT name, food_type, quantity, perishability, uncertainty FROM resources")
    return [
        {"name": n, "food_type": ft, "quantity": q, "perishability": p, "uncertainty": u} 
        for n, ft, q, p, u in c.fetchall()
    ]

# --- Get NGOs ---
@app.get("/ngos")
def get_ngos():
    c.execute("SELECT id, name, trust, capacity, latitude, longitude FROM ngos")
    return [{"id": i, "name": n, "trust": round(t,2), "capacity": cap, "lat": lat, "lon": lon} 
            for i, n, t, cap, lat, lon in c.fetchall()]

# --- Allocation ---
@app.post("/allocate")
def allocate():
    today = date.today().isoformat()
    c.execute("SELECT * FROM resources WHERE quantity>0 ORDER BY perishability DESC")
    resources = c.fetchall()

    for r in resources:
        rid, name, ftype, qty, perish, uncert = r
        while qty > 0:
            # High risk → farm
            if perish > 0.8:
                c.execute("SELECT name FROM farms ORDER BY RANDOM() LIMIT 1")
                farm = c.fetchone()[0]
                c.execute("INSERT INTO allocations (resource_name, receiver, quantity, decision, allocation_date) VALUES (?, ?, ?, ?, ?)",
                          (name, farm, 1, "BIO-DEGRADATION", today))
                qty -= 1
                continue

            # NGO selection
            c.execute("SELECT name, trust, capacity, latitude, longitude FROM ngos WHERE capacity>0")
            ngos = c.fetchall()
            if not ngos:
                break

            scored = []
            for ngo in ngos:
                n, trust, cap, lat, lon = ngo
                risk_penalty = uncert * random.uniform(0.8, 1.2)
                score = trust + cap*0.1 - risk_penalty
                scored.append((score, n))
            scored.sort(reverse=True)
            selected = scored[0][1]

            c.execute("INSERT INTO allocations (resource_name, receiver, quantity, decision, allocation_date) VALUES (?, ?, ?, ?, ?)",
                      (name, selected, 1, "NGO-ALLOCATION", today))
            update_rewards(selected, 1)
            c.execute("UPDATE ngos SET capacity = capacity - 1 WHERE name=?", (selected,))
            qty -= 1

        c.execute("UPDATE resources SET quantity=? WHERE id=?", (qty, rid))

    conn.commit()
    return {"status": "Risk-aware allocation completed"}

# --- Allocation Log ---
@app.get("/allocation_log")
def allocation_log():
    c.execute("""
        SELECT resource_name, receiver, quantity, decision, allocation_date
        FROM allocations
        ORDER BY id DESC
        LIMIT 50
    """)
    rows = c.fetchall()
    return [dict(row) for row in rows]  # convert sqlite Row to dict

# --- Rewards ---
@app.get("/rewards")
def rewards():
    c.execute("SELECT r.ngo_name, n.trust, r.streak, r.xp, r.level, r.total_allocations FROM rewards r JOIN ngos n ON r.ngo_name=n.name")
    return [{"ngo": ngo, "trust": round(trust,2), "streak": streak, "xp": xp, "level": level, "total_allocations": total} 
            for ngo, trust, streak, xp, level, total in c.fetchall()]

# --- AI Analysis ---
@app.get("/agentic_analysis")
def agentic_analysis():
    local_cursor = conn.cursor()
    
    # Fetch NGO performance and trust
    local_cursor.execute("""
        SELECT r.ngo_name, n.trust, r.total_allocations
        FROM rewards r
        JOIN ngos n ON r.ngo_name = n.name
    """)
    
    data = local_cursor.fetchall()
    
    insights = []
    
    for ngo_name, trust, total_allocations in data:
        if trust >= 4.5 and total_allocations < 5:
            text = (
                f"Human insight: {ngo_name} has very high trust ({trust:.2f}) "
                f"but has received few allocations ({total_allocations}). "
                "Recommend increasing support!"
            )
            color = "#4CAF50"  # green
        elif trust < 3.0:
            text = (
                f"Warning: {ngo_name} shows fluctuating trust ({trust:.2f}). "
                "Humans should monitor closely before allocating more resources."
            )
            color = "#FF5722"  # red
        else:
            text = (
                f"{ngo_name} is stable with trust {trust:.2f} and {total_allocations} allocations. "
                "Human managers can maintain current levels."
            )
            color = "#2196F3"  # blue
        
        insights.append({
            "text": text,
            "color": color
        })
    
    return insights
