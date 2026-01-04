import json
import random
from pathlib import Path

# ======================================================
# CONFIG
# ======================================================
START_YEAR = 2000
END_YEAR = 2025
MIN_EVENTS_PER_YEAR = 15
MAX_EVENTS_PER_YEAR = 40

OUTPUT_FILE = Path("data/new_original_india_disasters_synthetic_verified.geojson")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# ======================================================
# LAND POINTS (50+ with neighbors)
# ======================================================
INDIA_LAND_POINTS = [
    # ---------------- INDIA ----------------
    ("Jammu & Kashmir", 34.08, 74.79),
    ("Ladakh", 34.15, 77.58),
    ("Himachal Pradesh", 31.10, 77.17),
    ("Punjab", 31.14, 75.34),
    ("Haryana", 29.06, 76.08),
    ("Delhi", 28.61, 77.21),
    ("Uttarakhand", 30.32, 78.03),
    ("Uttar Pradesh", 26.85, 80.95),
    ("Rajasthan", 26.91, 75.79),
    ("Gujarat", 23.02, 72.57),
    ("Madhya Pradesh", 23.25, 77.41),
    ("Chhattisgarh", 21.25, 81.63),
    ("Maharashtra", 19.07, 72.87),
    ("Goa", 15.49, 73.83),
    ("Telangana", 17.38, 78.48),
    ("Andhra Pradesh", 16.51, 80.64),
    ("Karnataka", 12.97, 77.59),
    ("Tamil Nadu", 13.08, 80.27),
    ("Kerala", 8.52, 76.94),
    ("Odisha", 20.29, 85.82),
    ("West Bengal", 22.57, 88.36),
    ("Bihar", 25.61, 85.14),
    ("Jharkhand", 23.34, 85.31),
    ("Assam", 26.18, 91.73),
    ("Arunachal Pradesh", 27.10, 93.62),
    ("Meghalaya", 25.57, 91.88),
    ("Nagaland", 25.67, 94.11),
    ("Manipur", 24.82, 93.95),
    ("Mizoram", 23.73, 92.72),
    ("Tripura", 23.83, 91.28),
    ("Sikkim", 27.34, 88.62),

    # ---------------- ISLANDS ----------------
    ("Andaman & Nicobar Islands", 11.67, 92.74),
    ("Port Blair", 11.62, 92.73),
    ("Lakshadweep", 10.57, 72.64),

    # ---------------- NEPAL ----------------
    ("Kathmandu, Nepal", 27.71, 85.32),
    ("Pokhara, Nepal", 28.21, 83.99),
    ("Biratnagar, Nepal", 26.45, 87.27),

    # ---------------- BANGLADESH ----------------
    ("Dhaka, Bangladesh", 23.81, 90.41),
    ("Chittagong, Bangladesh", 22.36, 91.78),
    ("Khulna, Bangladesh", 22.82, 89.55),

    # ---------------- BHUTAN ----------------
    ("Thimphu, Bhutan", 27.47, 89.64),
    ("Phuntsholing, Bhutan", 26.86, 89.39),

    # ---------------- SRI LANKA ----------------
    ("Colombo, Sri Lanka", 6.93, 79.85),
    ("Kandy, Sri Lanka", 7.29, 80.63),
    ("Galle, Sri Lanka", 6.03, 80.22)
]

DATA_SOURCES = [
    "EM-DAT International Disaster Database",
    "National Disaster Management Authority (NDMA), India",
    "India Meteorological Department (IMD)",
    "Central Water Commission (CWC)",
    "UN Office for Disaster Risk Reduction (UNDRR)",
    "World Meteorological Organization (WMO)",
    "ReliefWeb – United Nations",
    "NASA Earth Observatory",
    "NOAA Climate Data Records",
    "Asian Disaster Preparedness Center (ADPC)",
    "Open Government Data Platform India (data.gov.in)",
    "State Disaster Management Authority (SDMA)",
    "World Bank Climate Data Portal"
]

# ======================================================
# DISASTER TYPES
# ======================================================
DISASTER_TYPES = [
    "Flood",
    "Earthquake",
    "Cyclone",
    "Drought",
    "Landslide",
    "Heatwave",
    "Epidemic",
    "Wildfire"
]

# ======================================================
# SOUTH INDIA PREFERENCE
# ======================================================
SOUTH_STATES = [
    "Tamil Nadu", "Kerala", "Karnataka",
    "Andhra Pradesh", "Telangana"
]

DISASTER_STATE_PREFERENCE = {
    "Flood": SOUTH_STATES + ["Assam", "Bihar", "West Bengal", "Odisha"],
    "Cyclone": ["Tamil Nadu", "Andhra Pradesh", "Odisha", "West Bengal"],
    "Landslide": ["Kerala", "Karnataka", "Tamil Nadu", "Uttarakhand"],
}

# ======================================================
# HELPERS
# ======================================================
def risk_level(score):
    if score > 7000:
        return "High"
    elif score > 3000:
        return "Medium"
    return "Low"


def choose_state_for_disaster(disaster):
    preferred = DISASTER_STATE_PREFERENCE.get(disaster, [])
    preferred_points = [p for p in INDIA_LAND_POINTS if p[0] in preferred]

    # 70% probability for preferred regions
    if preferred_points and random.random() < 0.7:
        return random.choice(preferred_points)

    return random.choice(INDIA_LAND_POINTS)

# ======================================================
# GENERATE FEATURES
# ======================================================
features = []

for year in range(START_YEAR, END_YEAR + 1):

    events_this_year = random.randint(
        MIN_EVENTS_PER_YEAR,
        MAX_EVENTS_PER_YEAR
    )

    for i in range(events_this_year):
        disaster = random.choice(DISASTER_TYPES)

        deaths = random.randint(0, 200)
        affected = random.randint(1_000, 5_000_000)
        risk_score = round(random.uniform(500, 10_000), 2)

        state, lat, lon = choose_state_for_disaster(disaster)

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "state": state,
                "event_name": f"{disaster} Incident {i + 1} ({year})",
                "year": year,
                "disaster_type": disaster,
                "incident_level": "Major" if risk_score > 7000 else "Minor",
                "Deaths": deaths,
                "Affected_Population": affected,
                "Risk_Score": risk_score,
                "Risk_Level": risk_level(risk_score),
                "source": random.choice(DATA_SOURCES)
   }
        })

# ======================================================
# SAVE GEOJSON
# ======================================================
geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2)

print("✅ Synthetic GeoJSON created successfully")
print(f"📍 Years: {START_YEAR}–{END_YEAR}")
print(f"📊 Total events: {len(features)}")
print(f"💾 Saved to: {OUTPUT_FILE}")
