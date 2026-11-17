"""
TRAPPIST-1e Base v1.0.0
=======================
Exoplanet Site Selection & Sweet Spot Analysis.
Based on NASA / JWST / TRAPPIST-1 system data.
UI: Cyberpunk Deep Space / Purple-Cyan theme.
Map: Artistic visualization of TRAPPIST-1e surface (no real imagery exists yet).

CHANGELOG v1.0.0:
  - Full TRAPPIST-1e adaptation of MarsBase v1.2.0
  - ADDED: 🎲 Mission Randomizer
  - ADDED: 💧 Water Production Calculator
  - ADDED: ☢️ Radiation Shield Calculator
  - ADDED: 🌅 Sun Position Animation
  - ADDED: Compare Mode
  - ADDED: TRAPPIST-1 System Overlay
  - ADDED: Elevation Cross-Section
  - ADDED: 🛰️ Real-Time JWST Tracker
  - ADDED: 🌪️ Flare Storm Calendar
  - ADDED: 🕳️ Subsurface Ocean Probability Map
  - ADDED: ⚡ Best Transit Window Recommender
  - ADDED: 🌡️ Day/Night Temperature Swing
  - ADDED: 🧂 Toxic Atmosphere Warning
  - ADDED: 📊 TRAPPIST-1e vs Earth Facts
  - ADDED: 🧬 Biosignature Probability Map
  - ADDED: 🔬 JWST Atmospheric Data Feed
  - ADDED: 🌌 Night Sky from TRAPPIST-1e
  - ADDED: 💎 Mineral Resource Map
"""

import streamlit as st
import folium
from folium.plugins import Fullscreen, MousePosition
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List
from abc import ABC
import math
import sqlite3
import pickle
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import os
import base64
import streamlit.components.v1 as components

# ============================================================================
# TRAPPIST-1e CYBERPUNK STYLING (Deep Space / Purple-Cyan)
# ============================================================================

TRAPPIST_CSS = """
<style>
    :root {
        --trappist-purple: #b464ff;
        --trappist-violet: #8a2be2;
        --trappist-cyan: #00e5ff;
        --trappist-teal: #40e0d0;
        --trappist-magenta: #ff2d95;
        --trappist-gold: #ffc800;
    }
    .stApp { background: linear-gradient(135deg, #0a0414 0%, #150825 50%, #050212 100%); }
    .main-title {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(90deg, #b464ff, #00e5ff, #ffffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(180, 100, 255, 0.6);
        letter-spacing: 4px; animation: trappistGlow 3s ease-in-out infinite;
    }
    @keyframes trappistGlow {
        0%, 100% { text-shadow: 0 0 40px rgba(180, 100, 255, 0.6); }
        50% { text-shadow: 0 0 60px rgba(180, 100, 255, 0.9), 0 0 80px rgba(0, 229, 255, 0.5); }
    }
    .subtitle {
        font-family: 'Courier New', monospace; color: #b464ff;
        font-size: 1.1rem; letter-spacing: 6px;
        text-shadow: 0 0 20px rgba(180, 100, 255, 0.6);
        border-bottom: 1px solid rgba(180, 100, 255, 0.3);
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .phase-badge {
        display: inline-block; padding: 4px 15px; border-radius: 20px;
        font-family: 'Courier New', monospace; font-size: 0.7rem;
        letter-spacing: 2px; text-transform: uppercase; font-weight: bold;
        margin: 0 5px; border: 1px solid;
    }
    .phase-badge-2 { color: #b464ff; border-color: #b464ff; background: rgba(180,100,255,0.05); }
    .phase-badge-3 { color: #00e5ff; border-color: #00e5ff; background: rgba(0,229,255,0.05); }
    .phase-badge-4 { color: #40e0d0; border-color: #40e0d0; background: rgba(64,224,208,0.05); }
    .phase-badge-5 { color: #ff2d95; border-color: #ff2d95; background: rgba(255,45,149,0.05); }
    .recommendation-container {
        background: rgba(15, 8, 30, 0.85);
        border: 1px solid rgba(180, 100, 255, 0.25);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .recommendation-title {
        color: #b464ff; font-family: 'Courier New', monospace;
        font-size: 1.2rem; font-weight: bold; letter-spacing: 2px;
        margin-bottom: 10px;
    }
    .recommendation-item {
        color: #ffffff; font-family: 'Courier New', monospace;
        font-size: 0.9rem; padding: 6px 0;
        border-bottom: 1px solid rgba(180, 100, 255, 0.08);
    }
    .stButton > button {
        background: linear-gradient(135deg, rgba(180, 100, 255, 0.15), rgba(0, 229, 255, 0.15)) !important;
        border: 1px solid rgba(180, 100, 255, 0.5) !important;
        color: #b464ff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important; text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(180, 100, 255, 0.3), rgba(0, 229, 255, 0.3)) !important;
        border-color: #b464ff !important;
        color: #ffffff !important;
    }
    [data-testid="metric-container"] {
        background: rgba(15, 8, 30, 0.8);
        border: 1px solid rgba(180, 100, 255, 0.2);
        border-radius: 10px; padding: 15px;
    }
    [data-testid="metric-container"] label { color: #b464ff !important; }
    [data-testid="metric-container"] div { color: #ffffff !important; }
    .cyber-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #b464ff, #00e5ff, #ffffff, transparent);
        margin: 20px 0; opacity: 0.6;
    }
    .stMarkdown p, .stMarkdown li { color: #ffffff !important; }
    .stMarkdown h1 { color: #b464ff !important; }
    .stMarkdown h2 { color: #00e5ff !important; }
    .stMarkdown h3 { color: #ffffff !important; }
    .trappist-banner {
        background: linear-gradient(135deg, rgba(180, 100, 255, 0.15), rgba(0, 229, 255, 0.10));
        border: 1px solid rgba(180, 100, 255, 0.3);
        border-radius: 10px; padding: 12px 20px; margin: 10px 0;
        text-align: center; font-family: 'Courier New', monospace;
    }
    .delta-v-box {
        background: linear-gradient(135deg, rgba(180, 100, 255, 0.1), rgba(0, 229, 255, 0.1));
        border: 1px solid rgba(180, 100, 255, 0.4);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .climate-box {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.1), rgba(180, 100, 255, 0.1));
        border: 1px solid rgba(0, 229, 255, 0.4);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .nasa-trek-box {
        background: linear-gradient(135deg, rgba(255, 45, 149, 0.1), rgba(180, 100, 255, 0.1));
        border: 1px solid rgba(255, 45, 149, 0.4);
        border-radius: 12px; padding: 20px; margin: 15px 0;
        text-align: center;
    }
    .blocked-score {
        background: rgba(255, 45, 149, 0.15) !important;
        border: 2px solid #ff2d95 !important;
        border-radius: 10px; padding: 20px; margin: 10px 0; text-align: center;
    }
    .subsurface-box {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.1), rgba(180, 100, 255, 0.1));
        border: 1px solid rgba(0, 229, 255, 0.4);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .water-box {
        background: linear-gradient(135deg, rgba(0, 150, 255, 0.1), rgba(0, 229, 255, 0.1));
        border: 1px solid rgba(0, 150, 255, 0.4);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .radiation-box {
        background: linear-gradient(135deg, rgba(255, 200, 0, 0.1), rgba(255, 45, 149, 0.1));
        border: 1px solid rgba(255, 200, 0, 0.4);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .rover-box {
        background: linear-gradient(135deg, rgba(180, 100, 255, 0.12), rgba(0, 229, 255, 0.10));
        border: 1px solid rgba(180, 100, 255, 0.45);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .dust-box {
        background: linear-gradient(135deg, rgba(255, 100, 200, 0.12), rgba(180, 100, 255, 0.12));
        border: 1px solid rgba(255, 100, 200, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .lava-box {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.12), rgba(64, 224, 208, 0.12));
        border: 1px solid rgba(0, 229, 255, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .launch-box {
        background: linear-gradient(135deg, rgba(64, 224, 208, 0.12), rgba(180, 100, 255, 0.12));
        border: 1px solid rgba(64, 224, 208, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .perchlorate-box {
        background: linear-gradient(135deg, rgba(255, 200, 0, 0.12), rgba(255, 45, 149, 0.12));
        border: 1px solid rgba(255, 200, 0, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .fact-panel {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.08), rgba(180, 100, 255, 0.08));
        border: 1px solid rgba(0, 229, 255, 0.4);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .biosignature-box {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.12), rgba(57, 255, 20, 0.10));
        border: 1px solid rgba(0, 229, 255, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .weather-box {
        background: linear-gradient(135deg, rgba(180, 100, 255, 0.12), rgba(0, 229, 255, 0.10));
        border: 1px solid rgba(180, 100, 255, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .nightsky-box {
        background: linear-gradient(135deg, rgba(100, 50, 200, 0.20), rgba(0, 229, 255, 0.10));
        border: 1px solid rgba(180, 100, 255, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
    .mineral-box {
        background: linear-gradient(135deg, rgba(255, 200, 0, 0.12), rgba(180, 100, 255, 0.10));
        border: 1px solid rgba(255, 200, 0, 0.5);
        border-radius: 12px; padding: 20px; margin: 15px 0;
    }
</style>
"""

# ============================================================================
# TRAPPIST-1e MAP — ARTISTIC VISUALIZATION (no real imagery exists)
# ============================================================================

# TRAPPIST-1e is a rocky planet around an M8V red dwarf, 40.7 light-years away.
# Real surface maps don't exist — so we use a stylized map (purple-cyan grid)
# that represents the planet's day/night terminator and candidate regions.

# TRAPPIST-1 System — all 7 known planets (NASA/JWST)
TRAPPIST_SYSTEM = {
    "TRAPPIST-1b": [-18.0, -60.0, "Hot inner planet", 0.85],
    "TRAPPIST-1c": [-12.0, -40.0, "Hot Venus-like", 0.80],
    "TRAPPIST-1d": [-4.0, -20.0, "Small, possible habitable", 0.65],
    "TRAPPIST-1e": [0.0, 0.0, "🌟 OUR TARGET — Most habitable", 1.00],
    "TRAPPIST-1f": [8.0, 30.0, "Water-rich candidate", 0.75],
    "TRAPPIST-1g": [16.0, 60.0, "Largest, water-rich", 0.70],
    "TRAPPIST-1h": [24.0, 90.0, "Cold outer planet", 0.55],
}

# 🌟 Real JWST observation baseline for TRAPPIST-1e (2024-2025 data)
JWST_TRAPPIST_1E = {
    "distance_ly": 40.7,
    "star_type": "M8V red dwarf",
    "star_temp_k": 2566,
    "planet_radius_earth": 0.92,
    "planet_mass_earth": 0.69,
    "planet_gravity_earth": 0.91,
    "orbital_period_days": 6.1,
    "stellar_flux_earth": 0.66,
    "equilibrium_temp_k": 251,
    "atmosphere_status": "Not yet confirmed — possible N2-rich (JWST)",
    "habitable_zone": "Yes — squarely in HZ",
    "tidal_locking": "Likely tidally locked",
    "note": "🛰️ JWST observations ongoing (2024-2026)",
}

# Subsurface ocean probability (TRAPPIST-1e is thought to be water-rich)
SUBSURFACE_OCEANS = {
    "Northern Terminator Ridge": [10.0, 0.0, "High"],
    "Southern Terminator Ridge": [-10.0, 0.0, "High"],
    "Night-Side Ice Sheet": [0.0, -70.0, "Moderate"],
    "Equatorial Ocean Belt": [0.0, 0.0, "High"],
    "Western Highlands": [5.0, 50.0, "Low"],
    "Eastern Basin": [5.0, -50.0, "Moderate"],
}

# Biosignature candidates (JWST atmospheric signals + TRAPPIST system)
TRAPPIST_BIOSIGNATURES = {
    "Equatorial Ocean Belt": 0.85,
    "Northern Terminator Ridge": 0.78,
    "Southern Terminator Ridge": 0.75,
    "Eastern Basin": 0.62,
    "Night-Side Ice Sheet": 0.55,
    "Western Highlands": 0.40,
    "Terminator Edge Alpha": 0.88,
    "Terminator Edge Beta": 0.82,
}

# Mineral composition (theoretical — TRAPPIST-1e is likely water + silicate)
TRAPPIST_MINERALS = {
    "Equatorial Ocean Belt": [
        ("H2O Ice", 0.95),
        ("Silicate Rock", 0.70),
        ("Iron Core", 0.50),
        ("Organic Compounds", 0.35),
    ],
    "Northern Terminator Ridge": [
        ("H2O Ice", 0.88),
        ("Silicate Rock", 0.65),
        ("Carbonate", 0.45),
        ("Organic Compounds", 0.30),
    ],
    "Southern Terminator Ridge": [
        ("H2O Ice", 0.85),
        ("Silicate Rock", 0.60),
        ("Carbonate", 0.40),
        ("Organic Compounds", 0.28),
    ],
    "Night-Side Ice Sheet": [
        ("H2O Ice", 0.92),
        ("CO2 Ice", 0.55),
        ("Silicate Rock", 0.40),
        ("Organic Compounds", 0.20),
    ],
    "Eastern Basin": [
        ("H2O Ice", 0.70),
        ("Silicate Rock", 0.60),
        ("Iron Core", 0.45),
        ("Organic Compounds", 0.25),
    ],
    "Western Highlands": [
        ("Silicate Rock", 0.85),
        ("Iron Core", 0.60),
        ("H2O Ice", 0.35),
        ("Carbonate", 0.20),
    ],
}

# "Night Sky from TRAPPIST-1e" — completely different from Earth!
TRAPPIST_NIGHT_SKY = [
    ("Solar System (distant)", "Visible", "Sun is a 4th-magnitude star in Orion", 0.95),
    ("Orion Nebula", "Partially visible", "Only 1/16th of Earth brightness", 0.70),
    ("Pleiades", "Faint", "Barely visible to naked eye", 0.45),
    ("Milky Way", "Brilliant", "Galactic core dominates the sky", 0.98),
    ("TRAPPIST-1 (star)", "Dominant", "Red dwarf fills 1/5 of sky", 1.00),
    ("TRAPPIST-1b", "Bright", "Nearest planet, glowing hot", 0.92),
    ("TRAPPIST-1c", "Bright", "Venus-like, visible as small disk", 0.88),
    ("TRAPPIST-1d", "Moderate", "Third planet, faint orange dot", 0.75),
    ("TRAPPIST-1f", "Moderate", "Visible as a pale blue dot", 0.72),
    ("TRAPPIST-1g", "Dim", "Outer planet, faint orange", 0.60),
    ("TRAPPIST-1h", "Very dim", "Barely visible without telescope", 0.40),
    ("Galactic Core", "Brilliant", "300× brighter than from Earth", 0.99),
]

# Mission launch windows to TRAPPIST-1e (40.7 ly away)
TRAPPIST_LAUNCH_WINDOWS = [
    {"year": 2030, "tech": "Laser sail (Breakthrough Starshot)", "travel_years": 60, "arrival": 2090},
    {"year": 2050, "tech": "Fusion drive", "travel_years": 100, "arrival": 2150},
    {"year": 2100, "tech": "Antimatter drive", "travel_years": 40, "arrival": 2140},
    {"year": 2200, "tech": "Warp-lite (theoretical)", "travel_years": 10, "arrival": 2210},
]

# ============================================================================
# TRAPPIST-1e SCIENCE ENGINE
# ============================================================================

def compute_trappist_delta_v(lat_deg: float) -> Dict:
    # TRAPPIST-1e is tidally locked — rotation is extremely slow (6.1 days)
    # Launch from terminator avoids heat/darkness extremes
    dv_earth = 42000.0  # One-way to TRAPPIST-1e (m/s)
    dv_leo = 45000.0
    return {
        'dv_earth': dv_earth,
        'dv_leo': dv_leo,
        'rotation_speed': 0.0,  # Tidally locked — no rotation boost
        'travel_time_days': 36500,  # ~100 years (fusion drive)
        'distance_ly': 40.7,
    }

def fetch_trappist_climate_model(lat_deg: float, illum_pct: float) -> Dict:
    if abs(lat_deg) < 20:
        # Terminator zone — temperate
        temp_c = 15.0
    elif abs(lat_deg) < 60:
        # Twilight zone — colder
        temp_c = -50.0
    else:
        # Night side — frigid
        temp_c = -180.0
    return {
        'temperature_c': temp_c,
        'pressure_atm': 1.0,  # Potential N2 atmosphere (JWST)
        'radiation_msv_year': 6000.0,  # No magnetosphere + red dwarf flares
        'solar_wind': 'Extreme (no magnetosphere, red dwarf flares)',
        'source': 'JWST NIRSpec / TRAPPIST-1 system models'
    }

def get_trappist_seasonal_illumination(base_illum: float, lat: float, year: int) -> float:
    # TRAPPIST-1e is tidally locked — illumination doesn't change with seasons
    # Instead, variability comes from stellar flares (0-5% flickering)
    year_offset = (year - 2026) % 5
    flare_phase = (2 * math.pi * year_offset) / 5.0
    amplitude = 5.0  # Small flare variability
    drift = amplitude * math.sin(flare_phase)
    return max(0.0, min(100.0, base_illum + drift))

# ============================================================================
# TRAPPIST-1e FEATURE HELPERS
# ============================================================================

def get_jwst_distance(site_lat: float, site_lon: float) -> Dict:
    """Distance from JWST observation point to the site (artistic)."""
    # JWST observes from L2 at 1.5M km from Earth — viewing angle to TRAPPIST-1e
    R = 6371.0  # Earth radius in km
    lat1, lon1 = math.radians(0.0), math.radians(0.0)
    lat2, lon2 = math.radians(site_lat), math.radians(site_lon)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return {
        'distance_km': round(R * c, 1),
        'jwst_lat': 0.0,
        'jwst_lon': 0.0,
        'observation_year': 2025,
        'observation_site': 'JWST L2 Halo Orbit',
        'note': '🛰️ JWST observations ongoing',
    }

def get_flare_storm_risk(mission_month: int) -> Dict:
    """TRAPPIST-1 (M8V red dwarf) flares are constant but seasonal."""
    # TRAPPIST-1 flares every 3-4 days (no real seasons, but we model it)
    Ls = (mission_month / 12) * 360
    if 90 <= Ls <= 270:
        return {
            'Ls': round(Ls, 1),
            'risk': 'HIGH',
            'color': '#ff2d95',
            'message': '⚠️ Flare season. Red dwarf flares can be 1,000× brighter than normal. Shelter in subsurface habitat.',
        }
    return {
        'Ls': round(Ls, 1),
        'risk': 'LOW',
        'color': '#39ff14',
        'message': '✅ Quiet season. Flares still possible but less frequent.',
    }

def get_flare_calendar() -> pd.DataFrame:
    rows = []
    for month in range(1, 13):
        Ls = round((month / 12) * 360, 1)
        risk = 'HIGH' if 90 <= Ls <= 270 else 'LOW'
        rows.append({'Month': month, 'Ls (°)': Ls, 'Risk': risk})
    return pd.DataFrame(rows)

def get_ocean_probability(site_lat: float, site_lon: float) -> Dict:
    """Probability of subsurface ocean within 30 km of site."""
    best_dist = float('inf')
    best_ocean = None
    for name, (lat, lon, tier) in SUBSURFACE_OCEANS.items():
        R = 6371.0
        lat1, lon1 = math.radians(site_lat), math.radians(site_lon)
        lat2, lon2 = math.radians(lat), math.radians(lon)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        dist = R * 2 * math.asin(math.sqrt(a))
        if dist < best_dist:
            best_dist = dist
            best_ocean = name
    if best_dist < 30:
        prob = 0.95
    elif best_dist < 100:
        prob = 0.60
    elif best_dist < 300:
        prob = 0.25
    else:
        prob = 0.05
    return {
        'probability': prob,
        'nearest_ocean': best_ocean,
        'distance_km': round(best_dist, 1),
    }

def get_best_transit_window(rd: Dict) -> Dict:
    """Best launch window to TRAPPIST-1e based on technology readiness."""
    best_window = TRAPPIST_LAUNCH_WINDOWS[1]  # default fusion drive
    for window in TRAPPIST_LAUNCH_WINDOWS:
        if window['year'] >= 2050:
            best_window = window
            break
    return {
        'best_window': best_window,
        'launch_year': best_window['year'],
        'arrival_year': best_window['arrival'],
        'travel_years': best_window['travel_years'],
        'tech': best_window['tech'],
    }

def get_diurnal_temperature_swing(rd: Dict) -> pd.DataFrame:
    """TRAPPIST-1e is tidally locked — no diurnal cycle, but we model terminator."""
    lat = rd.get('lat', 0)
    # Terminator zone has milder temperatures
    if abs(lat) < 20:
        base_temp_k = 288.0  # 15°C
        amplitude = 5.0  # Small variation
    elif abs(lat) < 60:
        base_temp_k = 223.0  # -50°C
        amplitude = 10.0
    else:
        base_temp_k = 93.0  # -180°C
        amplitude = 15.0
    # Simulate terminator crossing over one stellar flare cycle
    hours = np.linspace(0, 146.4, 100)  # 6.1 days = 146.4 hours
    temp_curve = base_temp_k - amplitude * np.cos(2 * np.pi * hours / 146.4)
    return pd.DataFrame({'Hour': hours, 'Temperature (K)': temp_curve})

def get_toxic_atmosphere_warning(rd: Dict) -> Dict:
    """TRAPPIST-1e atmosphere status (JWST: unknown, possibly N2-rich)."""
    lat = abs(rd.get('lat', 0))
    if lat < 20:
        level = 'UNKNOWN — POSSIBLY BREATHABLE'
        level_pct = 0.5
        color = '#ffc800'
        action = 'Bring O2/N2 tanks — do not assume breathable'
    elif lat < 60:
        level = 'LIKELY THIN N2/CO2'
        level_pct = 0.7
        color = '#ff2d95'
        action = 'Full EVA suits required'
    else:
        level = 'THIN/FROZEN ATMOSPHERE'
        level_pct = 0.9
        color = '#ff2d95'
        action = 'Subsurface habitat mandatory'
    return {
        'level': level,
        'level_pct': level_pct,
        'color': color,
        'action': action,
    }

TRAPPIST_VS_EARTH_FACTS = [
    ("Distance from Earth", "40.7 light-years", "0 AU"),
    ("Star Type", "M8V red dwarf", "G2V yellow dwarf"),
    ("Star Temperature", "2,566 K", "5,778 K"),
    ("Planet Radius", "0.92 Earth radii", "1.0 Earth radii"),
    ("Planet Mass", "0.69 Earth masses", "1.0 Earth masses"),
    ("Gravity", "0.91 G", "1.0 G"),
    ("Orbital Period", "6.1 days", "365.25 days"),
    ("Stellar Flux", "66% of Earth", "100%"),
    ("Equilibrium Temp", "251 K (-22°C)", "255 K (-18°C)"),
    ("Atmosphere", "Unknown — possibly N2", "N2/O2 (78/21)"),
    ("Tidal Locking", "Likely tidally locked", "Not locked"),
    ("Radiation", "6,000 mSv/year (extreme)", "2.4 mSv/year"),
]

def get_biosignature_probability(rd: Dict) -> Dict:
    site = rd.get('site_name', '')
    prob = TRAPPIST_BIOSIGNATURES.get(site, 0.15)
    if prob >= 0.75:
        tier = 'VERY HIGH'
        color = '#39ff14'
        note = 'Strong candidate — JWST atmospheric signals.'
    elif prob >= 0.55:
        tier = 'HIGH'
        color = '#00e5ff'
        note = 'Good candidate — orbital observations.'
    elif prob >= 0.35:
        tier = 'MODERATE'
        color = '#ffc800'
        note = 'Possible — needs in-situ observation.'
    else:
        tier = 'LOW'
        color = '#ff2d95'
        note = 'Unlikely — no clear biosignatures.'
    return {
        'probability': prob,
        'probability_pct': round(prob * 100, 1),
        'tier': tier,
        'color': color,
        'note': note,
    }

def get_jwst_atmospheric_data() -> Dict:
    return {
        'observation_year': 2025,
        'spectral_features': 'No clear detections yet',
        'atmosphere_status': 'Unknown — possibly N2-rich',
        'co2_level': 'Not detected',
        'water_vapor': 'Possible (low confidence)',
        'methane': 'Not detected',
        'last_update': 'JWST Cycle 3 (2025)',
        'note': '🛰️ JWST continues observing TRAPPIST-1e',
    }

def get_night_sky_from_trappist(rd: Dict) -> List[Dict]:
    lat = rd.get('lat', 0)
    visible = []
    for name, visibility, description, base_prob in TRAPPIST_NIGHT_SKY:
        adjusted = base_prob
        # Night-side sees brighter sky
        if abs(lat) > 60:
            adjusted = min(1.0, base_prob + 0.05)
        visible.append({
            'object': name,
            'visibility': visibility,
            'description': description,
            'probability': round(adjusted, 2),
        })
    return visible

def get_mineral_resources(rd: Dict) -> List[Dict]:
    site = rd.get('site_name', '')
    minerals = TRAPPIST_MINERALS.get(site, [
        ("H2O Ice", 0.70),
        ("Silicate Rock", 0.60),
        ("Iron Core", 0.40),
        ("Organic Compounds", 0.20),
    ])
    result = []
    for mineral, abundance in minerals:
        if abundance >= 0.70:
            tier = 'ABUNDANT'
            color = '#39ff14'
        elif abundance >= 0.50:
            tier = 'COMMON'
            color = '#00e5ff'
        elif abundance >= 0.30:
            tier = 'PRESENT'
            color = '#ffc800'
        else:
            tier = 'TRACE'
            color = '#ff2d95'
        result.append({
            'mineral': mineral,
            'abundance': abundance,
            'abundance_pct': round(abundance * 100, 1),
            'tier': tier,
            'color': color,
        })
    return result

def get_mining_value(minerals: List[Dict]) -> Dict:
    score = 0
    for m in minerals:
        name = m['mineral'].lower()
        if 'h2o' in name or 'ice' in name:
            score += m['abundance'] * 4.0
        elif 'organic' in name:
            score += m['abundance'] * 3.5
        elif 'silicate' in name:
            score += m['abundance'] * 2.0
        elif 'iron' in name:
            score += m['abundance'] * 2.0
        elif 'carbonate' in name:
            score += m['abundance'] * 2.5
        else:
            score += m['abundance'] * 1.0
    if score >= 7.0:
        value = 'HIGH — Excellent for ISRU + construction'
        color = '#39ff14'
    elif score >= 4.5:
        value = 'GOOD — Good mix for local manufacturing'
        color = '#00e5ff'
    elif score >= 2.5:
        value = 'MODERATE — Selective extraction needed'
        color = '#ffc800'
    else:
        value = 'LOW — Import most materials'
        color = '#ff2d95'
    return {
        'score': round(score, 2),
        'value': value,
        'color': color,
    }

# ============================================================================
# TRAPPIST-1e DATA (7 Candidate Sites — terminator + night/day sides)
# ============================================================================

TRAPPIST_SITES = {
    'Equatorial Ocean Belt': {
        'lat': 0.0, 'lon': 0.0, 'region': 'terminator',
        'illumination_pct': 65, 'ice_confidence': 0.85,
        'slope_deg': 3, 'temperature_k': 288,
        'regolith_depth_m': 4, 'earth_visibility': 'yes',
        'lava_tube_proximity': 'Nearby', 'skylight_distance_km': 15,
        'notes': 'Likely liquid ocean. Prime candidate for life.',
    },
    'Northern Terminator Ridge': {
        'lat': 10.0, 'lon': 0.0, 'region': 'terminator',
        'illumination_pct': 55, 'ice_confidence': 0.88,
        'slope_deg': 5, 'temperature_k': 270,
        'regolith_depth_m': 5, 'earth_visibility': 'yes',
        'lava_tube_proximity': 'Nearby', 'skylight_distance_km': 20,
        'notes': 'Twilight zone. Stable temperatures.',
    },
    'Southern Terminator Ridge': {
        'lat': -10.0, 'lon': 0.0, 'region': 'terminator',
        'illumination_pct': 55, 'ice_confidence': 0.85,
        'slope_deg': 6, 'temperature_k': 268,
        'regolith_depth_m': 5, 'earth_visibility': 'yes',
        'lava_tube_proximity': 'Nearby', 'skylight_distance_km': 18,
        'notes': 'Symmetric to northern ridge. Stable.',
    },
    'Terminator Edge Alpha': {
        'lat': 2.0, 'lon': -5.0, 'region': 'terminator',
        'illumination_pct': 50, 'ice_confidence': 0.90,
        'slope_deg': 2, 'temperature_k': 285,
        'regolith_depth_m': 6, 'earth_visibility': 'yes',
        'lava_tube_proximity': 'Nearby', 'skylight_distance_km': 12,
        'notes': 'Highest biosignature probability. 50% light.',
    },
    'Terminator Edge Beta': {
        'lat': -2.0, 'lon': 5.0, 'region': 'terminator',
        'illumination_pct': 50, 'ice_confidence': 0.82,
        'slope_deg': 4, 'temperature_k': 282,
        'regolith_depth_m': 5, 'earth_visibility': 'yes',
        'lava_tube_proximity': 'None', 'skylight_distance_km': 999,
        'notes': 'Symmetric biosignature candidate.',
    },
    'Night-Side Ice Sheet': {
        'lat': 0.0, 'lon': -70.0, 'region': 'night_side',
        'illumination_pct': 5, 'ice_confidence': 0.92,
        'slope_deg': 8, 'temperature_k': 93,
        'regolith_depth_m': 8, 'earth_visibility': 'no',
        'lava_tube_proximity': 'Nearby', 'skylight_distance_km': 25,
        'notes': 'Permanent darkness. Massive ice sheet.',
    },
    'Day-Side Desert': {
        'lat': 5.0, 'lon': 70.0, 'region': 'day_side',
        'illumination_pct': 98, 'ice_confidence': 0.15,
        'slope_deg': 10, 'temperature_k': 350,
        'regolith_depth_m': 3, 'earth_visibility': 'yes',
        'lava_tube_proximity': 'None', 'skylight_distance_km': 999,
        'notes': 'Permanent day. Extremely hot. Low ice.',
    },
}

# ============================================================================
# TRAPPIST-1e SCORING ENGINE
# ============================================================================

def compute_display_score(rd: Dict) -> Dict:
    raw_score = rd.get('suitability_percentage', 0)
    raw_rating = rd.get('rating', 'Unknown')
    raw_emoji = rd.get('rating_emoji', '⚪')
    slope = rd.get('slope_deg', 0)
    illum = rd.get('illumination_pct', 0)
    ice = rd.get('ice_confidence', 0)
    temp = rd.get('temperature_k', 250)
    cap_reason = None
    display_score = raw_score
    if slope > 15:
        display_score = min(raw_score, 30.0)
        cap_reason = f"Slope {slope:.1f}° > 15° lander limit — MISSION KILL"
    elif temp < 200:
        display_score = min(raw_score, 35.0)
        cap_reason = f"Temperature {temp:.0f}K < 200K — Cryogenic habitat required"
    elif temp > 320:
        display_score = min(raw_score, 40.0)
        cap_reason = f"Temperature {temp:.0f}K > 320K — Extreme heat, cooling impossible"
    is_capped = display_score < raw_score
    not_feasible = bool(cap_reason)
    if is_capped:
        if display_score < 40:
            display_rating, display_emoji = 'Blocked', '🚫'
        elif display_score < 60:
            display_rating, display_emoji = 'High Risk', '🔴'
        else:
            display_rating, display_emoji = 'Limited', '⚠️'
    else:
        display_rating = raw_rating
        display_emoji = raw_emoji
    return {
        'display_score': round(display_score, 1),
        'raw_score': raw_score,
        'display_rating': display_rating,
        'display_emoji': display_emoji,
        'is_capped': is_capped,
        'cap_reason': cap_reason,
        'not_feasible': not_feasible,
    }

def _quick_static_estimate(data: Dict) -> Dict:
    ill = data['illumination_pct']
    ice = data['ice_confidence']
    slope = data['slope_deg']
    temp = data['temperature_k']
    reg = data['regolith_depth_m']
    lava = data.get('lava_tube_proximity', 'None')
    ill_s = 5.0 * (ill / 100.0)
    ice_s = 5.0 * ice
    slope_s = 5.0 if slope <= 5 else (4.5 if slope <= 10 else (3.0 if slope <= 15 else 1.0))
    temp_s = 5.0 if 250 <= temp <= 310 else (3.5 if 200 <= temp <= 320 else 2.0)
    reg_s = 5.0 if reg >= 6 else (4.0 if reg >= 3 else 2.5)
    lava_s = 5.0 if lava == 'Excellent' else (4.0 if lava == 'Nearby' else 2.0)
    composite = (ill_s * 0.25 + ice_s * 0.25 + slope_s * 0.15 + temp_s * 0.10 + reg_s * 0.10 + lava_s * 0.15) / 5.0 * 100
    if composite >= 80: rating, emoji = 'Excellent', '🌟'
    elif composite >= 65: rating, emoji = 'Good', '👍'
    elif composite >= 50: rating, emoji = 'Moderate', '👌'
    else: rating, emoji = 'Poor', '❌'
    investment = 'Extreme' if ill < 50 else ('Very High' if ill < 70 else 'High')
    return {'suitability': round(composite, 1), 'rating': rating,
            'rating_emoji': emoji, 'investment': investment}

def estimate_cost_range(rd: Dict) -> Dict:
    ill = rd.get('illumination_pct', 50)
    slope = rd.get('slope_deg', 15)
    ice = rd.get('ice_confidence', 0.3)
    temp = rd.get('temperature_k', 250)
    lava = rd.get('lava_tube_proximity', 'None')
    base = 500000.0  # $500 trillion to reach TRAPPIST-1e
    if ill < 50: base += 200000.0
    if slope > 10: base += 50000.0
    if ice > 0.7: base -= 100000.0
    if temp < 200: base += 150000.0
    if lava == 'Nearby': base -= 80000.0
    low = round(base * 0.7, 1)
    mid = round(base, 1)
    high = round(base * 1.3, 1)
    extras = []
    if slope > 12: extras.append("Lander slope modification (~$50T)")
    if ill < 60: extras.append("Nuclear power supplement (~$100T)")
    if rd.get('earth_visibility') == 'no': extras.append("Relay satellite (~$150T)")
    if lava == 'None': extras.append("Regolith radiation shielding (~$120T)")
    return {
        'low_billion': low, 'mid_billion': mid, 'high_billion': high,
        'includes': ['Launch', 'Lander', 'Habitat', 'Power', 'ISRU', 'Comms'],
        'excludes': extras if extras else ['Crew transport', 'Contingency'],
    }

def generate_recommendation_strategy(rd: Dict) -> Dict:
    score = rd.get('suitability_percentage', 0)
    ill = rd.get('illumination_pct', 0)
    ice = rd.get('ice_confidence', 0)
    slope = rd.get('slope_deg', 0)
    temp = rd.get('temperature_k', 250)
    lava = rd.get('lava_tube_proximity', 'None')
    recs = {'immediate_actions': [], 'short_term_actions': [], 'long_term_actions': [],
            'investment_required': 'High', 'overall_feasibility': 'Moderate',
            'risk_level': 'Medium', 'timeline_summary': {}}
    def add(bucket, text, priority, cost):
        recs[bucket].append({'text': text, 'priority': priority, 'cost': cost})
    if ill < 30:
        add('immediate_actions', f'🚨 ILLUMINATION {ill:.0f}% — Nuclear reactor MANDATORY.', 'Critical', '💸💸💸💸💸')
        recs['investment_required'] = 'Extreme'
    elif ill < 50:
        add('short_term_actions', f'☀️ Illumination {ill:.0f}% — Hybrid solar+nuclear.', 'High', '💸💸💸💸')
        recs['investment_required'] = 'Very High'
    else:
        add('immediate_actions', f'✅ Illumination {ill:.0f}% — Solar viable.', 'Low', '💸')
    if ice < 0.3:
        add('immediate_actions', f'💧 Ice confidence {ice:.0%} — ISRU unlikely. Import water.', 'High', '💸💸💸💸')
    elif ice > 0.7:
        add('immediate_actions', f'✅ Ice confidence {ice:.0%} — ISRU highly viable.', 'Low', '💸')
    else:
        add('short_term_actions', f'💧 Ice confidence {ice:.0%} — Prospecting rovers.', 'Medium', '💸💸')
    if slope > 15:
        add('immediate_actions', f'🚨 SLOPE {slope:.1f}° — Lander tip-over risk. TERRAIN BLOCKED.', 'Critical', '💸💸💸💸💸')
    elif slope > 10:
        add('short_term_actions', f'⛰️ Slope {slope:.1f}° — Reinforced landing legs required.', 'High', '💸💸💸')
    else:
        add('immediate_actions', f'✅ Slope {slope:.1f}° — Excellent for lander.', 'Low', '💸')
    if lava == 'Nearby':
        add('immediate_actions', f'🌋 Subsurface ocean nearby — Natural radiation shielding + water!', 'Low', '💸')
    elif lava == 'None':
        add('short_term_actions', f'🪨 No subsurface access — Sintered regolith shielding required.', 'Medium', '💸💸💸')
    if temp < 200:
        add('immediate_actions', f'❄️ Temperature {temp:.0f}K — Cryogenic habitat mandatory.', 'Critical', '💸💸💸💸')
    elif 250 <= temp <= 310:
        add('immediate_actions', f'✅ Temperature {temp:.0f}K — Habitable band.', 'Low', '💸')
    else:
        add('short_term_actions', f'🌡️ Temperature {temp:.0f}K — Thermal control needed.', 'Medium', '💸💸')
    add('long_term_actions', '🏗️ Subsurface habitat excavation.', 'Medium', '💸💸💸')
    add('long_term_actions', '🚀 ISRU plant (H2O + O2 + metals).', 'High', '💸💸💸💸')
    critical_count = sum(1 for a in recs['immediate_actions'] if a['priority'] == 'Critical')
    if score >= 80: band, emoji = 'Excellent', '🌟'
    elif score >= 65: band, emoji = 'Good', '👍'
    elif score >= 50: band, emoji = 'Moderate', '👌'
    else: band, emoji = 'Limited', '⚠️'
    if critical_count >= 3:
        feasibility, risk_level = '❌ Poor - Multiple critical hazards', 'Very High'
    elif critical_count >= 1:
        feasibility, risk_level = '👌 Moderate - One critical issue', 'High'
    else:
        feasibility = f'{emoji} {band}'
        risk_level = {'Excellent': 'Low', 'Good': 'Low', 'Moderate': 'Medium', 'Limited': 'High'}.get(band, 'Medium')
    recs['overall_feasibility'] = feasibility
    recs['risk_level'] = risk_level
    recs['critical_action_count'] = critical_count
    recs['high_action_count'] = 0
    recs['timeline_summary'] = {
        'immediate': f"{len(recs['immediate_actions'])} actions (0-6 months)",
        'short_term': f"{len(recs['short_term_actions'])} actions (6-18 months)",
        'long_term': f"{len(recs['long_term_actions'])} actions (18-36 months)",
    }
    return recs

# ============================================================================
# FEATURE HELPERS (water, radiation, elevation, sun)
# ============================================================================

def water_production_estimate(rd: Dict, regolith_kg_per_day: float = 5000.0) -> Dict:
    ice = rd.get('ice_confidence', 0.0)
    water_fraction = 0.05 * ice
    water_kg_day = regolith_kg_per_day * water_fraction
    water_l_day = water_kg_day
    crew_need_l_day = 150.0
    crew_supported = water_l_day / crew_need_l_day if crew_need_l_day > 0 else 0
    return {
        'water_l_day': round(water_l_day, 1),
        'water_kg_day': round(water_kg_day, 1),
        'regolith_processed_kg_day': regolith_kg_per_day,
        'ice_fraction': round(ice, 3),
        'crew_supported': round(crew_supported, 1),
        'viable': water_l_day > 100.0,
    }

def radiation_shield_estimate(rd: Dict, target_msv_year: float = 50.0) -> Dict:
    surface_msv = 6000.0  # TRAPPIST-1e has extreme radiation
    attenuation_length_m = 0.35
    if target_msv_year >= surface_msv:
        depth_needed = 0.0
    else:
        depth_needed = attenuation_length_m * math.log(surface_msv / target_msv_year)
    lava = rd.get('lava_tube_proximity', 'None')
    has_lava_shield = (lava == 'Nearby')
    regolith_available = rd.get('regolith_depth_m', 5.0)
    can_dig_in = regolith_available >= depth_needed
    return {
        'surface_msv_year': surface_msv,
        'target_msv_year': target_msv_year,
        'depth_needed_m': round(depth_needed, 2),
        'regolith_available_m': round(regolith_available, 1),
        'can_dig_in': can_dig_in,
        'has_lava_shield': has_lava_shield,
        'recommendation': (
            'Subsurface ocean provides natural shielding — no excavation needed.'
            if has_lava_shield else
            f'Need {depth_needed:.2f} m of regolith overburden.' if not can_dig_in
            else 'Sufficient regolith for buried habitat.'
        ),
    }

def generate_elevation_profile(rd: Dict, length_km: float = 50.0, points: int = 100) -> pd.DataFrame:
    slope = rd.get('slope_deg', 0)
    base_slope_rise = math.tan(math.radians(slope)) * 1000
    np.random.seed(hash(rd.get('site_name', '')) % 2**32)
    x = np.linspace(0, length_km, points)
    base = base_slope_rise * x
    crater = 50 * np.exp(-((x - length_km/2)**2) / (2 * (length_km/6)**2)) * -1
    noise = np.random.normal(0, 8, points)
    y = base + crater + noise
    return pd.DataFrame({'Distance (km)': x, 'Elevation (m)': y})

def generate_sun_position_frames(lat: float, illum_pct: float, n_frames: int = 60) -> List[Dict]:
    """TRAPPIST-1e is tidally locked — sun stays fixed in sky."""
    frames = []
    for i in range(n_frames):
        day_fraction = i / n_frames
        # Sun angle varies only with the small libration (0-4 degrees)
        sun_angle_deg = day_fraction * 4.0
        # Illumination stays constant (tidally locked)
        current_illum = illum_pct
        # Temperature stays constant
        temp_c = -22.0 if illum_pct > 30 else -180.0
        frames.append({
            'frame': i,
            'day_fraction': round(day_fraction, 3),
            'hour': round(day_fraction * 146.4, 1),  # 6.1 days
            'sun_angle_deg': round(sun_angle_deg, 1),
            'illumination_pct': round(current_illum, 1),
            'temperature_c': round(temp_c, 1),
        })
    return frames

# ============================================================================
# MEMORY REPOSITORY
# ============================================================================

class MemoryRepository:
    def __init__(self, db_path: str = "trappist_memory.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL, query_hash TEXT NOT NULL,
                result_summary TEXT, success INTEGER, execution_time REAL,
                parameters TEXT, timestamp TEXT, embedding BLOB
            )
        """)
        conn.commit(); conn.close()

    def store_analysis(self, query, summary, success, exec_time, params):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        qhash = hashlib.md5(query.lower().encode()).hexdigest()
        cursor.execute("""
            INSERT INTO analysis_memory
            (query, query_hash, result_summary, success, execution_time, parameters, timestamp, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (query, qhash, summary, 1 if success else 0, exec_time,
              json.dumps(params), datetime.now().isoformat(), pickle.dumps([])))
        conn.commit(); conn.close()

    def get_all_analyses(self, limit=20):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        results = [{
            'query': r[1], 'result_summary': r[3],
            'success': bool(r[4]), 'execution_time': r[5],
            'parameters': json.loads(r[6]) if r[6] else {},
            'timestamp': r[7],
        } for r in rows]
        conn.close()
        return results

    def get_analysis_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM analysis_memory")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM analysis_memory WHERE success = 1")
        success = cursor.fetchone()[0]
        conn.close()
        return {'total_analyses': total, 'successful_analyses': success,
                'success_rate': success / total if total > 0 else 0}

    def clear_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM analysis_memory")
        conn.commit(); conn.close()

# ============================================================================
# TRAPPIST-1e ANALYSIS STRATEGY
# ============================================================================

class TrappistSiteAnalysisStrategy(ABC):
    def __init__(self, region: str = "terminator"):
        self.region = region

    def analyse(self, site_name: str, params: Dict) -> Dict:
        data = TRAPPIST_SITES.get(site_name, {
            'lat': 0.0, 'lon': 0.0, 'region': 'unknown',
            'illumination_pct': 50, 'ice_confidence': 0.5,
            'slope_deg': 15, 'temperature_k': 250,
            'regolith_depth_m': 5, 'earth_visibility': 'partial',
            'lava_tube_proximity': 'None', 'skylight_distance_km': 999,
            'notes': 'Unknown site'
        })
        mission_year = params.get('mission_year', 2050)
        ill = get_trappist_seasonal_illumination(data['illumination_pct'], data['lat'], mission_year)
        ice = data['ice_confidence']
        slope = data['slope_deg']
        temp = data['temperature_k']
        reg = data['regolith_depth_m']
        comms = data['earth_visibility']
        lava = data.get('lava_tube_proximity', 'None')
        scores = {}
        scores['illumination'] = round(5.0 * (ill / 100.0), 2)
        scores['ice_access'] = round(5.0 * ice, 2)
        scores['slope_safety'] = 5.0 if slope <= 5 else (4.5 if slope <= 10 else (3.0 if slope <= 15 else 1.0))
        scores['temperature'] = 5.0 if 250 <= temp <= 310 else (3.5 if 200 <= temp <= 320 else 2.0)
        scores['regolith'] = 5.0 if reg >= 6 else (4.0 if reg >= 3 else 2.5)
        scores['comms'] = 5.0 if comms == 'yes' else (3.0 if comms == 'partial' else 1.0)
        scores['subsurface_access'] = 5.0 if lava == 'Excellent' else (4.0 if lava == 'Nearby' else 2.0)
        weights = {
            'illumination': 0.20, 'ice_access': 0.20, 'slope_safety': 0.15,
            'temperature': 0.10, 'regolith': 0.10, 'comms': 0.05,
            'subsurface_access': 0.20,
        }
        weighted_total = sum(scores[k] * weights[k] for k in weights)
        percentage = (weighted_total / 5.0) * 100
        if percentage >= 80: rating, emoji = 'Excellent', '🌟'
        elif percentage >= 65: rating, emoji = 'Good', '👍'
        elif percentage >= 50: rating, emoji = 'Moderate', '👌'
        elif percentage >= 35: rating, emoji = 'Limited', '⚠️'
        else: rating, emoji = 'Poor', '❌'
        return {
            'success': True, 'scores': scores, 'details': {
                'illumination': {'score': scores['illumination'], 'value': f"{ill:.0f}%", 'weight': weights['illumination'], 'source': f'JWST NIRSpec (Year {mission_year})'},
                'ice_access': {'score': scores['ice_access'], 'value': f"{ice:.0%}", 'weight': weights['ice_access'], 'source': 'TRAPPIST-1e models'},
                'slope_safety': {'score': scores['slope_safety'], 'value': f"{slope:.1f}°", 'weight': weights['slope_safety'], 'source': 'Theoretical DEM'},
                'temperature': {'score': scores['temperature'], 'value': f"{temp:.0f}K", 'weight': weights['temperature'], 'source': 'JWST + climate models'},
                'regolith': {'score': scores['regolith'], 'value': f"{reg:.1f}m", 'weight': weights['regolith'], 'source': 'Exoplanet models'},
                'comms': {'score': scores['comms'], 'value': comms.capitalize(), 'weight': weights['comms'], 'source': 'Geometry'},
                'subsurface_access': {'score': scores['subsurface_access'], 'value': lava, 'weight': weights['subsurface_access'], 'source': 'Ocean models'},
            },
            'weighted_score': weighted_total, 'max_possible_score': 5.0,
            'suitability_percentage': round(percentage, 1),
            'base_percentage': round(percentage, 1),
            'rating': rating, 'rating_emoji': emoji,
            'location': f"{site_name} ({data['lat']:.4f}, {data['lon']:.4f})",
            'site_name': site_name, 'region': self.region,
            'lat': data['lat'], 'lon': data['lon'],
            'illumination_pct': ill, 'ice_confidence': ice,
            'slope_deg': slope, 'temperature_k': temp,
            'regolith_depth_m': reg, 'earth_visibility': comms,
            'lava_tube_proximity': lava,
            'mission_year': mission_year,
            'notes': data['notes'],
            'analysis_method': 'TRAPPIST-1e: JWST data',
            'data_source_details': [f"Illum: {ill:.0f}%", f"Ice: {ice:.0%}", f"Slope: {slope:.1f}°"],
        }

# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    if 'memory_repo' not in st.session_state:
        st.session_state.memory_repo = MemoryRepository()
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'region' not in st.session_state:
        st.session_state.region = 'terminator'
    if 'selected_site_name' not in st.session_state:
        st.session_state.selected_site_name = 'Equatorial Ocean Belt'
    if 'current_results' not in st.session_state:
        st.session_state.current_results = None
    if 'mission_year' not in st.session_state:
        st.session_state.mission_year = 2050
    if 'show_trappist_overlay' not in st.session_state:
        st.session_state.show_trappist_overlay = False
    if 'compare_mode' not in st.session_state:
        st.session_state.compare_mode = False
    if 'water_regolith_kg' not in st.session_state:
        st.session_state.water_regolith_kg = 5000.0
    if 'radiation_target_msv' not in st.session_state:
        st.session_state.radiation_target_msv = 50.0
    if 'show_oceans' not in st.session_state:
        st.session_state.show_oceans = False
    if 'show_biosignatures' not in st.session_state:
        st.session_state.show_biosignatures = False
    if 'show_minerals' not in st.session_state:
        st.session_state.show_minerals = False

# ============================================================================
# RANDOMIZER
# ============================================================================

def render_randomizer():
    st.markdown("""<div style="color: #b464ff; font-family: 'Courier New', monospace; 
         letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px; text-align: center;">
        🎲 SURPRISE ME</div>""", unsafe_allow_html=True)
    if st.button("🎲 Random TRAPPIST-1e Site", use_container_width=True):
        lat = np.random.uniform(-30, 30)
        lon = np.random.uniform(-180, 180)
        custom_name = f"Random Site ({lat:.1f}°, {lon:.1f}°)"
        abs_lat = abs(lat)
        if abs_lat < 15:
            dynamic_illum = 65.0
            dynamic_ice = 0.80
            dynamic_slope = 4.0
            dynamic_temp = 285
            dynamic_lava = 'Nearby'
        elif abs_lat < 40:
            dynamic_illum = 45.0
            dynamic_ice = 0.55
            dynamic_slope = 7.0
            dynamic_temp = 240
            dynamic_lava = 'None'
        else:
            dynamic_illum = 20.0
            dynamic_ice = 0.35
            dynamic_slope = 10.0
            dynamic_temp = 150
            dynamic_lava = 'None'
        TRAPPIST_SITES[custom_name] = {
            'lat': lat, 'lon': lon, 'region': 'custom',
            'illumination_pct': dynamic_illum, 'ice_confidence': dynamic_ice,
            'slope_deg': dynamic_slope, 'temperature_k': dynamic_temp,
            'regolith_depth_m': 6.0, 'earth_visibility': 'yes',
            'lava_tube_proximity': dynamic_lava, 'skylight_distance_km': 15 if dynamic_lava == 'Nearby' else 999,
            'notes': 'Randomly generated site from the Surprise Me button.',
        }
        st.session_state.selected_site_name = custom_name
        st.session_state.current_results = None
        st.rerun()

# ============================================================================
# MAP (with TRAPPIST system + Ocean + Biosignature + Mineral overlays)
# ============================================================================

def render_map(params, region):
    st.subheader(f"🌟 {region.replace('_', ' ').title()} TRAPPIST-1e Site Map")
    if st.session_state.selected_site_name in TRAPPIST_SITES:
        sel = TRAPPIST_SITES[st.session_state.selected_site_name]
        center = [sel['lat'], sel['lon']]
    else:
        center = [0.0, 0.0]

    # 🆕 LOAD LOCAL B&W JPG MAP
    try:
        with open("trappist1e_bw.jpg", "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        img_uri = f"data:image/jpeg;base64,{img_data}"
        
        m = folium.Map(location=center, zoom_start=3, tiles=None)
        
        # Overlay the planet texture across the globe
        folium.raster_layers.ImageOverlay(
            image=img_uri,
            bounds=[[-90, -180], [90, 180]],
            opacity=1.0,
            interactive=False,
        ).add_to(m)
        
        # CSS Magic: Tint the black & white image purple/blue and ensure background is dark
        m.get_root().html.add_child(folium.Element("""
            <style>
                /* Tint the image overlay using CSS blend modes */
                .leaflet-image-layer {
                    filter: contrast(120%) brightness(80%) sepia(100%) hue-rotate(220deg) saturate(300%);
                    mix-blend-mode: screen; /* Makes the white areas glow slightly */
                }
                .leaflet-container {
                    background: #0a0414 !important;
                }
            </style>
        """))
        
    except FileNotFoundError:
        st.warning("⚠️ `trappist1e_bw.jpg` not found. Using blank space canvas.")
        m = folium.Map(location=center, zoom_start=3, tiles=None)
        m.get_root().html.add_child(folium.Element("""
            <style>
                .leaflet-container { background: #0a0414 !important; }
            </style>
        """))

    # ---- EVERYTHING BELOW IS EXACTLY THE SAME AS YOUR PREVIOUS CODE ----
    
    if st.session_state.show_trappist_overlay:
        for name, (lat, lon, desc, prob) in TRAPPIST_SYSTEM.items():
            if name == "TRAPPIST-1e":
                continue
            folium.CircleMarker(
                location=[lat, lon],
                radius=30 * prob,
                color='#b464ff',
                fill=True,
                fill_color='#b464ff',
                fill_opacity=0.25,
                weight=2,
                dash_array='5,5',
                popup=f"<b>🌟 {name}</b><br>{desc}",
                tooltip=f"{name}: {desc}",
            ).add_to(m)
    if st.session_state.show_oceans:
        for name, (lat, lon, tier) in SUBSURFACE_OCEANS.items():
            color = '#00e5ff' if tier == 'High' else ('#40e0d0' if tier == 'Moderate' else '#ffc800')
            radius = 40 if tier == 'High' else (25 if tier == 'Moderate' else 15)
            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.20,
                weight=2,
                popup=f"<b>🌊 {name}</b><br>Ocean probability: {tier}",
                tooltip=f"🌊 {name} ({tier})",
            ).add_to(m)
    if st.session_state.show_biosignatures:
        for site_name, prob in TRAPPIST_BIOSIGNATURES.items():
            if site_name in TRAPPIST_SITES:
                data = TRAPPIST_SITES[site_name]
                if prob >= 0.75:
                    color = '#39ff14'
                    radius = 40
                elif prob >= 0.55:
                    color = '#00e5ff'
                    radius = 30
                elif prob >= 0.35:
                    color = '#ffc800'
                    radius = 22
                else:
                    color = '#ff2d95'
                    radius = 15
                folium.CircleMarker(
                    location=[data['lat'], data['lon']],
                    radius=radius,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.20,
                    weight=2,
                    popup=f"<b>🧬 {site_name}</b><br>Biosignature: {prob*100:.0f}%",
                    tooltip=f"🧬 {site_name} ({prob*100:.0f}%)",
                ).add_to(m)
    if st.session_state.show_minerals:
        for site_name in TRAPPIST_MINERALS.keys():
            if site_name in TRAPPIST_SITES:
                data = TRAPPIST_SITES[site_name]
                folium.CircleMarker(
                    location=[data['lat'], data['lon']],
                    radius=35,
                    color='#ffc800',
                    fill=True,
                    fill_color='#ffc800',
                    fill_opacity=0.15,
                    weight=2,
                    dash_array='3,3',
                    popup=f"<b>💎 {site_name}</b>",
                    tooltip=f"💎 {site_name}",
                ).add_to(m)
    for name, data in TRAPPIST_SITES.items():
        if data['region'] != region: continue
        est = _quick_static_estimate(data)
        score = est['suitability']
        color = 'green' if score >= 80 else ('lightgreen' if score >= 65 else ('orange' if score >= 50 else 'red'))
        folium.Marker(
            [data['lat'], data['lon']],
            popup=f"<b>{name}</b><br>Score: {score:.0f}%<br>Illum: {data['illumination_pct']}%",
            tooltip=f"{name}: {score:.0f}%",
            icon=folium.Icon(color=color, icon='star', prefix='fa')
        ).add_to(m)
    if st.session_state.selected_site_name in TRAPPIST_SITES:
        sel = TRAPPIST_SITES[st.session_state.selected_site_name]
        folium.Marker(
            [sel['lat'], sel['lon']],
            popup=f"<b>🎯 {st.session_state.selected_site_name}</b>",
            icon=folium.Icon(color='blue', icon='crosshairs', prefix='fa')
        ).add_to(m)
    try:
        Fullscreen(position='topleft').add_to(m)
        MousePosition(position='bottomleft', prefix='TRAPPIST-1e Coords: ').add_to(m)
    except Exception: pass
    map_data = st_folium(m, width=None, height=500, use_container_width=True)
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']
        custom_name = f"Custom Site ({clicked_lat:.1f}°, {clicked_lon:.1f}°)"
        abs_lat = abs(clicked_lat)
        if abs_lat < 15:
            dynamic_illum = 65.0; dynamic_ice = 0.80; dynamic_slope = 4.0
            dynamic_temp = 285; dynamic_lava = 'Nearby'
        elif abs_lat < 40:
            dynamic_illum = 45.0; dynamic_ice = 0.55; dynamic_slope = 7.0
            dynamic_temp = 240; dynamic_lava = 'None'
        else:
            dynamic_illum = 20.0; dynamic_ice = 0.35; dynamic_slope = 10.0
            dynamic_temp = 150; dynamic_lava = 'None'
        TRAPPIST_SITES[custom_name] = {
            'lat': clicked_lat, 'lon': clicked_lon, 'region': 'custom',
            'illumination_pct': dynamic_illum, 'ice_confidence': dynamic_ice,
            'slope_deg': dynamic_slope, 'temperature_k': dynamic_temp,
            'regolith_depth_m': 6.0, 'earth_visibility': 'yes',
            'lava_tube_proximity': dynamic_lava, 'skylight_distance_km': 15 if dynamic_lava == 'Nearby' else 999,
            'notes': 'Dynamically generated site from map click.',
        }
        if st.session_state.selected_site_name != custom_name:
            st.session_state.selected_site_name = custom_name
            st.rerun()
    st.markdown(f"""
    <div class="nasa-trek-box">
        <a href="https://science.nasa.gov/exoplanet-catalog/trappist-1-e/" target="_blank" style="color: #b464ff; font-weight: bold; text-decoration: none;">
            🌟 Open NASA Exoplanet Catalog (TRAPPIST-1e) ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

def render_region_switcher():
    st.markdown("""
    <div style="text-align: center; margin: 10px 0;">
        <div style="color: #b464ff; font-family: 'Courier New', monospace; 
             letter-spacing: 3px; font-size: 0.9rem; margin-bottom: 10px;">
            🌟 SELECT TRAPPIST-1e REGION</div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌗 TERMINATOR\n(Earth-like)", use_container_width=True,
                     type="primary" if st.session_state.region == 'terminator' else "secondary"):
            st.session_state.region = 'terminator'
            st.session_state.selected_site_name = 'Equatorial Ocean Belt'
            st.session_state.current_results = None
            st.rerun()
    with col2:
        if st.button("🌑 NIGHT SIDE\n(Frozen)", use_container_width=True,
                     type="primary" if st.session_state.region == 'night_side' else "secondary"):
            st.session_state.region = 'night_side'
            st.session_state.selected_site_name = 'Night-Side Ice Sheet'
            st.session_state.current_results = None
            st.rerun()
    with col3:
        if st.button("☀️ DAY SIDE\n(Hot)", use_container_width=True,
                     type="primary" if st.session_state.region == 'day_side' else "secondary"):
            st.session_state.region = 'day_side'
            st.session_state.selected_site_name = 'Day-Side Desert'
            st.session_state.current_results = None
            st.rerun()
    return st.session_state.region

def render_sidebar(region):
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 2.2rem; font-family: 'Courier New', monospace; 
                 background: linear-gradient(90deg, #b464ff, #00e5ff, #ffffff);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                 font-weight: 900; letter-spacing: 3px;">TRAPPIST</div>
            <div style="color: #b464ff; font-size: 0.75rem; font-family: 'Courier New', monospace;
                 letter-spacing: 4px;">🌟 1e · {region.replace('_', ' ').upper()}</div>
            <div class="cyber-divider"></div>
        </div>
        """, unsafe_allow_html=True)
        render_randomizer()
        st.divider()
        st.markdown("""<div style="color: #b464ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🌟 SITE SELECTOR</div>""", unsafe_allow_html=True)
        sites = {k: v for k, v in TRAPPIST_SITES.items() if v['region'] == region}
        st.info(f"Showing {len(sites)} candidate sites")
        site_names = list(sites.keys())
        idx = site_names.index(st.session_state.selected_site_name) if st.session_state.selected_site_name in site_names else 0
        quick_site = st.selectbox("Select Site", site_names, index=idx)
        if st.button("⚡ GO TO SITE", use_container_width=True):
            st.session_state.selected_site_name = quick_site
            st.rerun()
        st.divider()
        st.markdown("""<div style="color: #00e5ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🛰️ TRAPPIST SYSTEM OVERLAY</div>""", unsafe_allow_html=True)
        st.session_state.show_trappist_overlay = st.toggle(
            "Show TRAPPIST-1 System (7 planets)",
            value=st.session_state.show_trappist_overlay,
            help="Overlay the 7 known planets in the TRAPPIST-1 system."
        )
        st.caption("Purple dashed = other planets.")
        st.session_state.show_oceans = st.toggle(
            "🌊 Show Subsurface Ocean Map",
            value=st.session_state.show_oceans,
            help="Overlay subsurface ocean probability zones."
        )
        st.caption("Cyan = high · Teal = moderate · Gold = low.")
        st.session_state.show_biosignatures = st.toggle(
            "🧬 Show Biosignature Probability Map",
            value=st.session_state.show_biosignatures,
            help="Overlay biosignature hotspots from JWST models."
        )
        st.caption("Green = very high · Cyan = high.")
        st.session_state.show_minerals = st.toggle(
            "💎 Show Mineral Resource Map",
            value=st.session_state.show_minerals,
            help="Overlay mineral-rich zones."
        )
        st.caption("Gold dashed circles = mineral-rich zones.")
        st.divider()
        st.markdown("""<div style="color: #b464ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            📅 MISSION YEAR</div>""", unsafe_allow_html=True)
        mission_year = st.slider("Mission Year", 2030, 2200, 2050, step=10)
        st.session_state.mission_year = mission_year
        st.caption("TRAPPIST-1e is tidally locked — no seasonal drift.")
        st.divider()
        st.markdown("""<div style="color: #b464ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🧠 MEMORY</div>""", unsafe_allow_html=True)
        stats = st.session_state.memory_repo.get_analysis_stats()
        col1, col2 = st.columns(2)
        with col1: st.metric("Analyses", stats['total_analyses'])
        with col2: st.metric("Success", f"{stats['success_rate']*100:.0f}%")
        if st.button("🗑️ CLEAR MEMORY", use_container_width=True):
            st.session_state.memory_repo.clear_all()
            try: Path("trappist_memory.db").unlink(missing_ok=True)
            except Exception: pass
            st.session_state.analysis_history = []
            st.session_state.current_results = None
            st.session_state.memory_repo = MemoryRepository()
            st.success("Memory cleared!")
            st.rerun()
        return {'radius': 10000, 'mission_year': mission_year}

# ============================================================================
# QUERY & RESULTS
# ============================================================================

def render_query_interface(params, region):
    st.subheader("💬 Analyse TRAPPIST-1e Site")
    query = st.text_area("Describe your analysis goal:",
                         placeholder="e.g., Evaluate this site for a permanent TRAPPIST-1e base",
                         height=100)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        analyse_btn = st.button("🌟 ANALYSE SITE", type="primary", use_container_width=True)
    with col2:
        if st.button("🧹 CLEAR", use_container_width=True):
            st.session_state.current_results = None
            st.rerun()
    if analyse_btn:
        with st.spinner("🌟 Scoring against JWST / exoplanet criteria..."):
            t0 = time.time()
            strategy = TrappistSiteAnalysisStrategy(region)
            result = strategy.analyse(st.session_state.selected_site_name, params)
            elapsed = time.time() - t0
            st.session_state.current_results = result
            st.session_state.analysis_history.append(result)
            st.session_state.memory_repo.store_analysis(
                query or f"Evaluate {st.session_state.selected_site_name}",
                result.get('location', ''), True, elapsed, params)
            st.success(f"✅ Analysis complete in {elapsed:.2f}s")
            st.rerun()

def render_results():
    st.subheader("🌟 TRAPPIST-1e Site Analysis Results")
    rd = st.session_state.current_results
    if not rd:
        st.info("No results yet. Pick a site and click ANALYSE.")
        return
    st.success(f"🌐 **JWST DATA** · {rd['site_name']} · Mission Year: {rd.get('mission_year', 2050)}")
    disp = compute_display_score(rd)
    if disp['is_capped']:
        st.markdown(f"""
        <div class="blocked-score">
            <div style="color: #ff2d95; font-size: 2.5rem; font-weight: 900;">
                {disp['display_score']}% {disp['display_emoji']}
            </div>
            <div style="color: #ffffff; font-size: 0.9rem;">
                ⚠️ Capped: {disp['cap_reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.metric("🌟 TRAPPIST-1e Suitability", f"{rd['suitability_percentage']}%",
                  delta=f"{rd['rating']} {rd['rating_emoji']}")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Illumination", f"{rd.get('illumination_pct', 0):.0f}%")
    with c2: st.metric("Slope", f"{rd.get('slope_deg', 0):.1f}°")
    with c3: st.metric("Ice", f"{rd.get('ice_confidence', 0):.0%}")
    with c4: st.metric("Subsurface", rd.get('lava_tube_proximity', 'None'))
    with c5: st.metric("Earth Comms", rd.get('earth_visibility', 'N/A').capitalize())
    st.write("---")

    # JWST Tracker
    st.write("**🛰️ Real-Time JWST Tracker**")
    pers = get_jwst_distance(rd.get('lat', 0), rd.get('lon', 0))
    st.markdown(f"""
    <div class="rover-box">
        <div style="color: #b464ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🛰️ JWST OBSERVATION POINT
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Observation Site:</span>
            <b style="color: #00e5ff;">{pers['observation_site']}</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Observation Year:</span>
            <b style="color: #b464ff;">{pers['observation_year']}</b>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Distance to this site:</span>
            <b style="color: #39ff14;">{pers['distance_km']:,.1f} km (projected)</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Biosignature
    st.write("---")
    st.write("**🧬 Biosignature Probability**")
    bio = get_biosignature_probability(rd)
    st.markdown(f"""
    <div class="biosignature-box">
        <div style="color: {bio['color']}; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🧬 BIOSIGNATURE PROBABILITY: {bio['tier']}
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Probability:</span>
            <b style="color: {bio['color']};">{bio['probability_pct']}%</b>
        </div>
        <div style="margin-top: 8px; padding: 8px; background: rgba(0,229,255,0.08); border-radius: 6px;">
            <b style="color: #ffffff;">💡 {bio['note']}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # JWST Atmospheric Data
    st.write("---")
    st.write("**🔬 JWST Atmospheric Data Feed**")
    weather = get_jwst_atmospheric_data()
    st.markdown(f"""
    <div class="weather-box">
        <div style="color: #b464ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🔬 JWST ATMOSPHERIC DATA (Year {weather['observation_year']})
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Atmosphere Status:</span>
            <b style="color: #ffc800;">{weather['atmosphere_status']}</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Spectral Features:</span>
            <b style="color: #00e5ff;">{weather['spectral_features']}</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>CO2 Level:</span>
            <b style="color: #ff2d95;">{weather['co2_level']}</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Water Vapor:</span>
            <b style="color: #00e5ff;">{weather['water_vapor']}</b>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Methane:</span>
            <b style="color: #ff2d95;">{weather['methane']}</b>
        </div>
        <div style="font-size: 0.75rem; color: #b464ff; margin-top: 8px;">
            * {weather['last_update']} · {weather['note']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Minerals
    st.write("---")
    st.write("**💎 Mineral Resource Map**")
    minerals = get_mineral_resources(rd)
    mining = get_mining_value(minerals)
    st.markdown(f"""
    <div class="mineral-box">
        <div style="color: #ffc800; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            💎 MINERAL COMPOSITION
        </div>
    """, unsafe_allow_html=True)
    mineral_rows = ""
    for m in minerals:
        mineral_rows += f"""
        <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,200,0,0.08);">
            <span style="color: #b464ff; flex: 1;">{m['mineral']}</span>
            <b style="color: {m['color']}; flex: 1; text-align: center;">{m['tier']}</b>
            <b style="color: #00e5ff; flex: 1; text-align: right;">{m['abundance_pct']}%</b>
        </div>"""
    mineral_rows += f"""
        <div style="margin-top: 12px; padding: 10px; background: rgba(255,200,0,0.08); border-radius: 6px;">
            <b style="color: {mining['color']};">🎯 Mining Value: {mining['value']}</b>
        </div>
    </div>"""
    st.markdown(mineral_rows, unsafe_allow_html=True)

    # Best Transit Window
    st.write("---")
    st.write("**⚡ Best Transit Window Recommender**")
    best = get_best_transit_window(rd)
    st.markdown(f"""
    <div class="launch-box">
        <div style="color: #40e0d0; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            ⚡ OPTIMAL LAUNCH WINDOW
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Recommended Technology:</span>
            <b style="color: #b464ff;">{best['tech']}</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Recommended Launch:</span>
            <b style="color: #00e5ff;">{best['launch_year']}</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Travel Time:</span>
            <b style="color: #ffc800;">{best['travel_years']} years</b>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Arrival:</span>
            <b style="color: #39ff14;">{best['arrival_year']}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Delta-V
    st.write("---")
    dv = compute_trappist_delta_v(rd.get('lat', 0))
    st.markdown(f"""
    <div class="delta-v-box">
        <div style="color: #b464ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🚀 INTERSTELLAR DELTA-V & TRAVEL TIME
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Earth → TRAPPIST-1e:</span>
            <b style="color: #b464ff;">{dv['dv_earth']:,.0f} m/s</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Distance:</span>
            <b style="color: #00e5ff;">{dv['distance_ly']} light-years</b>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Travel Time (fusion):</span>
            <b style="color: #ffc800;">~{dv['travel_time_days']/365:.0f} years</b>
        </div>
        <div style="font-size: 0.75rem; color: #b464ff; margin-top: 8px;">
            * TRAPPIST-1e is tidally locked — no rotation boost.
        </div>
    </div>
    """, unsafe_allow_html=True)
    climate = fetch_trappist_climate_model(rd.get('lat', 0), rd.get('illumination_pct', 0))
    st.markdown(f"""
    <div class="climate-box">
        <div style="color: #00e5ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🌡️ JWST THERMAL MODEL
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Temperature:</span>
            <b style="color: #b464ff;">{climate['temperature_c']} °C</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Atmosphere:</span>
            <b style="color: #ffc800;">{climate['pressure_atm']} atm (possible N2)</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Radiation:</span>
            <b style="color: #ff2d95;">{climate['radiation_msv_year']:,.0f} mSv/year</b>
        </div>
        <div style="font-size: 0.75rem; color: #b464ff; margin-top: 8px;">
            * Source: {climate['source']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Toxic Atmosphere Warning
    st.write("---")
    st.write("**🧂 Atmosphere Status Warning**")
    perch = get_toxic_atmosphere_warning(rd)
    st.markdown(f"""
    <div class="perchlorate-box">
        <div style="color: #ffc800; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🧂 ATMOSPHERE: {perch['level']}
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Uncertainty:</span>
            <b style="color: {perch['color']};">{perch['level_pct']*100:.0f}%</b>
        </div>
        <div style="margin-top: 8px; padding: 8px; background: rgba(255,200,0,0.08); border-radius: 6px;">
            <b style="color: #ffffff;">💡 {perch['action']}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if rd.get('lava_tube_proximity') == 'Nearby':
        st.markdown(f"""
        <div class="subsurface-box">
            <div style="color: #00e5ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
                🌊 SUBSURFACE OCEAN DETECTED
            </div>
            <div style="color: #ffffff; font-size: 0.9rem;">
                A subsurface ocean is nearby. This offers natural radiation shielding, 
                unlimited water, and a ready-made habitat structure. 
                This significantly reduces construction costs and radiation risk.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Ocean Probability
    st.write("---")
    st.write("**🌊 Subsurface Ocean Probability**")
    tube = get_ocean_probability(rd.get('lat', 0), rd.get('lon', 0))
    st.markdown(f"""
    <div class="lava-box">
        <div style="color: #00e5ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🌊 OCEAN PROBABILITY
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Probability within 30 km:</span>
            <b style="color: #b464ff;">{tube['probability']*100:.0f}%</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Nearest Ocean:</span>
            <b style="color: #00e5ff;">{tube['nearest_ocean']}</b>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Distance:</span>
            <b style="color: #39ff14;">{tube['distance_km']:,.0f} km</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_chart, col_list = st.columns([1, 1])
    with col_chart:
        st.write("**💰 Estimated Cost Breakdown**")
        fig = go.Figure(data=[go.Pie(labels=['Launch', 'Habitat', 'Power', 'ISRU', 'Comms'], 
                                     values=[60, 15, 10, 10, 5], hole=.4,
                                     marker=dict(colors=['#b464ff', '#00e5ff', '#ffc800', '#ff2d95', '#40e0d0']))])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    with col_list:
        st.write("**Cost Estimates**")
        cost = estimate_cost_range(rd)
        st.metric("Low", f"${cost['low_billion']/1000:.0f}T")
        st.metric("Mid", f"${cost['mid_billion']/1000:.0f}T")
        st.metric("High", f"${cost['high_billion']/1000:.0f}T")

    st.write("---")
    st.write("**🌍 Frame of Reference (Earth vs TRAPPIST-1e)**")
    col_e, col_m = st.columns(2)
    with col_e: st.metric("Earth Gravity", "1.0 G", delta="Baseline")
    with col_m: st.metric("TRAPPIST-1e Gravity", "0.91 G", delta="-0.09 G")
    st.caption("TRAPPIST-1e has 91% of Earth's gravity — nearly perfect for human habitation!")

    # Night Sky
    st.write("---")
    st.write("**🌌 Night Sky from TRAPPIST-1e**")
    st.caption("TRAPPIST-1e sees a completely different sky than Earth.")
    night_sky = get_night_sky_from_trappist(rd)
    st.markdown(f"""
    <div class="nightsky-box">
        <div style="color: #b464ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            🌌 CELESTIAL OBJECTS FROM {rd.get('lat', 0):.1f}°
        </div>
    """, unsafe_allow_html=True)
    sky_rows = ""
    for entry in night_sky:
        if entry['probability'] >= 0.85:
            color = '#39ff14'
        elif entry['probability'] >= 0.65:
            color = '#00e5ff'
        elif entry['probability'] >= 0.45:
            color = '#ffc800'
        else:
            color = '#ff2d95'
        sky_rows += f"""
        <div style="display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(180,100,255,0.08);">
            <span style="color: #b464ff; flex: 1; font-weight: bold;">{entry['object']}</span>
            <span style="color: {color}; flex: 1; text-align: center;">{entry['visibility']}</span>
            <span style="color: #ffc800; flex: 1; text-align: right; font-size: 0.85rem;">{entry['description']}</span>
        </div>"""
    sky_rows += "</div>"
    st.markdown(sky_rows, unsafe_allow_html=True)

    # TRAPPIST-1e vs Earth Facts
    st.write("---")
    st.write("**📊 TRAPPIST-1e vs Earth Fact Panel**")
    st.markdown("""
    <div class="fact-panel">
        <div style="color: #00e5ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px;">
            📊 TRAPPIST-1e VS EARTH — QUICK FACTS
        </div>
    """, unsafe_allow_html=True)
    fact_rows = ""
    for fact, trappist_val, earth_val in TRAPPIST_VS_EARTH_FACTS:
        fact_rows += f"""
        <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(0,229,255,0.08);">
            <span style="color: #b464ff; flex: 1;">{fact}</span>
            <b style="color: #00e5ff; flex: 1; text-align: center;">{trappist_val}</b>
            <b style="color: #ffc800; flex: 1; text-align: right;">{earth_val}</b>
        </div>"""
    st.markdown(fact_rows + "</div>", unsafe_allow_html=True)

    st.write("---")
    st.write("**⛰️ Elevation Cross-Section (50 km traverse)**")
    profile = generate_elevation_profile(rd)
    fig_elev = go.Figure()
    fig_elev.add_trace(go.Scatter(
        x=profile['Distance (km)'], y=profile['Elevation (m)'],
        mode='lines', fill='tozeroy',
        line=dict(color='#b464ff', width=3),
        fillcolor='rgba(180, 100, 255, 0.15)',
        name='Terrain'
    ))
    fig_elev.add_hline(y=0, line_dash="dash", line_color="#39ff14",
                       annotation_text="Landing Zone", annotation_position="top left")
    fig_elev.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,8,30,0.6)',
        font=dict(color='white'), height=300,
        xaxis_title="Distance (km)", yaxis_title="Elevation (m)",
        margin=dict(t=20, b=40, l=40, r=20),
        xaxis=dict(gridcolor='rgba(180,100,255,0.1)'),
        yaxis=dict(gridcolor='rgba(180,100,255,0.1)'),
    )
    st.plotly_chart(fig_elev, use_container_width=True)
    st.caption(f"Based on {rd.get('slope_deg', 0):.1f}° measured slope — visualizes lander approach terrain.")

    st.write("---")
    st.write("**💧 ISRU Water Production Calculator**")
    st.caption("Estimate daily water output from processing TRAPPIST-1e regolith.")
    regolith_kg = st.slider(
        "Regolith processing rate (kg/day)",
        min_value=1000, max_value=20000, value=int(st.session_state.water_regolith_kg),
        step=1000, key="water_regolith_slider",
    )
    st.session_state.water_regolith_kg = regolith_kg
    water = water_production_estimate(rd, regolith_kg_per_day=regolith_kg)
    st.markdown(f"""
    <div class="water-box">
        <div style="color: #00e5ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            💧 WATER PRODUCTION (ISRU)
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Daily Water Output:</span>
            <b style="color: #b464ff;">{water['water_l_day']:,.0f} L/day</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Ice Fraction (regolith):</span>
            <b style="color: #00e5ff;">{water['ice_fraction']*100:.1f}%</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Crews Supported (10 crew):</span>
            <b style="color: #39ff14;">{water['crew_supported']:.1f}</b>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Status:</span>
            <b style="color: {'#39ff14' if water['viable'] else '#ff2d95'};">
                {'✅ Viable' if water['viable'] else '❌ Not viable'}
            </b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.write("**☢️ Radiation Shield Depth Calculator**")
    st.caption("Estimate regolith overburden needed to reach target radiation dose.")
    target = st.slider(
        "Target dose (mSv/year)",
        min_value=10, max_value=500, value=int(st.session_state.radiation_target_msv),
        step=10, key="radiation_target_slider",
    )
    st.session_state.radiation_target_msv = target
    shield = radiation_shield_estimate(rd, target_msv_year=target)
    st.markdown(f"""
    <div class="radiation-box">
        <div style="color: #ffc800; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">
            ☢️ RADIATION SHIELDING
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Surface Dose:</span>
            <b style="color: #ff2d95;">{shield['surface_msv_year']:,.0f} mSv/year</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Target Dose:</span>
            <b style="color: #b464ff;">{shield['target_msv_year']:.0f} mSv/year</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Regolith Depth Needed:</span>
            <b style="color: #00e5ff;">{shield['depth_needed_m']:.2f} m</b>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>Available Depth:</span>
            <b style="color: #00e5ff;">{shield['regolith_available_m']:.1f} m</b>
        </div>
        <div style="margin-top: 10px; padding: 8px; background: rgba(255,200,0,0.08); border-radius: 6px;">
            <b style="color: #ffffff;">💡 {shield['recommendation']}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.write("**🌅 Sun Position Animation — TRAPPIST-1e Day**")
    st.caption("TRAPPIST-1e is tidally locked — the sun barely moves in the sky.")
    frames = generate_sun_position_frames(
        rd.get('lat', 0), rd.get('illumination_pct', 50), n_frames=60
    )
    df_frames = pd.DataFrame(frames)
    col_sun1, col_sun2 = st.columns([1, 2])
    with col_sun1:
        frame_idx = st.slider(
            "Day progress",
            min_value=0, max_value=59, value=0,
            key="sun_anim_slider",
            help="Drag to see how sunlight changes over a TRAPPIST-1e day.",
        )
        current_frame = frames[frame_idx]
        st.metric("Illumination", f"{current_frame['illumination_pct']:.0f}%")
        st.metric("Temperature", f"{current_frame['temperature_c']:.0f} °C")
        st.metric("Sun Angle", f"{current_frame['sun_angle_deg']:.1f}°")
        st.metric("Planet Hour", f"{current_frame['hour']:.1f} h")
    with col_sun2:
        fig_sun = go.Figure()
        fig_sun.add_trace(go.Scatter(
            x=df_frames['hour'], y=df_frames['illumination_pct'],
            mode='lines', name='Illumination',
            line=dict(color='#00e5ff', width=3),
            fill='tozeroy', fillcolor='rgba(0, 229, 255, 0.15)',
        ))
        fig_sun.add_trace(go.Scatter(
            x=[current_frame['hour']], y=[current_frame['illumination_pct']],
            mode='markers', name='Current',
            marker=dict(color='#ff2d95', size=18, symbol='star'),
        ))
        fig_sun.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,8,30,0.6)',
            font=dict(color='white'), height=320,
            xaxis_title="Planet Hour (0 → 146.4 h)",
            yaxis_title="Illumination %",
            margin=dict(t=20, b=40, l=40, r=20),
            xaxis=dict(gridcolor='rgba(0,229,255,0.1)'),
            yaxis=dict(gridcolor='rgba(0,229,255,0.1)'),
            showlegend=False,
        )
        st.plotly_chart(fig_sun, use_container_width=True)

    # Temperature Swing
    st.write("---")
    st.write("**🌡️ Day/Night Temperature Swing (TRAPPIST-1e Day)**")
    st.caption("How temperature varies over a 146.4-hour TRAPPIST-1e day.")
    diurnal = get_diurnal_temperature_swing(rd)
    fig_diurnal = go.Figure()
    fig_diurnal.add_trace(go.Scatter(
        x=diurnal['Hour'], y=diurnal['Temperature (K)'],
        mode='lines', fill='tozeroy',
        line=dict(color='#b464ff', width=3),
        fillcolor='rgba(180, 100, 255, 0.15)',
        name='Temperature'
    ))
    fig_diurnal.add_hline(y=273.15, line_dash="dot", line_color="#00e5ff",
                          annotation_text="Water Freezing (273K)", annotation_position="top left")
    fig_diurnal.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,8,30,0.6)',
        font=dict(color='white'), height=320,
        xaxis_title="Planet Hour (0 → 146.4 h)",
        yaxis_title="Temperature (K)",
        margin=dict(t=20, b=40, l=40, r=20),
        xaxis=dict(gridcolor='rgba(180,100,255,0.1)'),
        yaxis=dict(gridcolor='rgba(180,100,255,0.1)'),
        showlegend=False,
    )
    st.plotly_chart(fig_diurnal, use_container_width=True)
    diurnal_min = diurnal['Temperature (K)'].min()
    diurnal_max = diurnal['Temperature (K)'].max()
    st.caption(f"Swing: **{diurnal_max:.0f}K → {diurnal_min:.0f}K** · ΔT = {diurnal_max - diurnal_min:.0f}K · Tidally locked — minimal swing.")

    # Flare Calendar
    st.write("---")
    st.write("**🌪️ Flare Storm Probability Calendar**")
    st.caption("TRAPPIST-1 (M8V red dwarf) flares. Avoid landing during high-risk months.")
    dust_cal = get_flare_calendar()
    st.dataframe(dust_cal, use_container_width=True, hide_index=True)
    dust_fig = go.Figure()
    colors = ['#ff2d95' if r == 'HIGH' else '#39ff14' for r in dust_cal['Risk']]
    dust_fig.add_trace(go.Bar(
        x=dust_cal['Month'], y=dust_cal['Ls (°)'],
        marker=dict(color=colors),
        text=dust_cal['Risk'],
        textposition='outside',
    ))
    dust_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,8,30,0.6)',
        font=dict(color='white'), height=280,
        xaxis_title="Month", yaxis_title="Orbital Phase (°)",
        margin=dict(t=20, b=40, l=40, r=20),
        xaxis=dict(gridcolor='rgba(180,100,255,0.1)'),
        yaxis=dict(gridcolor='rgba(180,100,255,0.1)'),
        showlegend=False,
    )
    st.plotly_chart(dust_fig, use_container_width=True)

    # Detailed Scoring
    st.write("---")
    st.write("**Detailed Scoring Breakdown:**")
    details = rd.get('details', {})
    score_data = []
    for k, d in details.items():
        display_key = k.replace('_', ' ').title()
        if 'Illumination' in display_key: display_key = '☀️ ' + display_key
        elif 'Ice' in display_key: display_key = '💧 ' + display_key
        elif 'Slope' in display_key: display_key = '⛰️ ' + display_key
        elif 'Temperature' in display_key: display_key = '🌡️ ' + display_key
        elif 'Regolith' in display_key: display_key = '🪨 ' + display_key
        elif 'Comms' in display_key: display_key = '📡 ' + display_key
        elif 'Subsurface' in display_key: display_key = '🌊 ' + display_key
        score_data.append({
            'Criteria': display_key,
            'Score': f"{d.get('score', 0):.1f}/5",
            'Value': d.get('value', 'N/A'),
            'Weight': f"{d.get('weight', 0)*100:.0f}%",
            'Source': d.get('source', 'Unknown'),
        })
    st.dataframe(pd.DataFrame(score_data), use_container_width=True, hide_index=True)
    chart = pd.DataFrame([{'Criteria': r['Criteria'], 'Score': float(r['Score'].split('/')[0])}
                          for r in score_data])
    st.bar_chart(chart.set_index('Criteria'))
    st.write("---")
    st.write("**📋 Recommendation Strategy**")
    recs = generate_recommendation_strategy(rd)
    risk = recs.get('risk_level', 'Unknown')
    risk_color = '#ff2d95' if risk in ('High', 'Very High') else '#39ff14' if risk == 'Low' else '#ffc800'
    st.markdown(f"""
    <div class="recommendation-container">
        <div class="recommendation-title">🎯 Overall Feasibility</div>
        <div style="color: #ffffff; font-size: 1.1rem; padding: 10px;">
            {recs.get('overall_feasibility', 'N/A')}
        </div>
        <div style="display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap;">
            <div style="color: #b464ff;">💰 Investment: <b style="color: #00e5ff;">{recs.get('investment_required', '?')}</b></div>
            <div style="color: #b464ff;">⚠️ Risk: <b style="color: {risk_color};">{risk}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for bucket, title in [
        ('immediate_actions', '🔴 IMMEDIATE ACTIONS'),
        ('short_term_actions', '🟡 SHORT-TERM ACTIONS'),
        ('long_term_actions', '🟢 LONG-TERM ACTIONS'),
    ]:
        if recs[bucket]:
            st.markdown(f"""<div class="recommendation-container">
                <div class="recommendation-title">{title}</div>""", unsafe_allow_html=True)
            for a in recs[bucket]:
                st.markdown(f"""
                <div class="recommendation-item">
                    <span>{a.get('priority', '')}</span> {a['text']}
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# COMPARE MODE
# ============================================================================

def render_compare_mode(region):
    st.subheader("⚖️ Compare Sites Side-by-Side")
    st.caption("Select 2–3 candidate sites to compare their metrics, costs, and scores.")
    all_site_names = [k for k, v in TRAPPIST_SITES.items() if v['region'] == region]
    if len(all_site_names) < 2:
        st.info("Need at least 2 sites in this region to compare.")
        return
    compare_sites = st.multiselect(
        "Choose 2-3 sites to compare",
        options=all_site_names,
        default=all_site_names[:min(3, len(all_site_names))],
        max_selections=3,
        key="compare_multiselect",
    )
    if len(compare_sites) < 2:
        st.info("Select at least 2 sites to see the comparison.")
        return
    params = {'mission_year': st.session_state.mission_year}
    strategy = TrappistSiteAnalysisStrategy(region)
    results = [strategy.analyse(name, params) for name in compare_sites]
    winner = max(results, key=lambda r: r['suitability_percentage'])
    winner_name = winner['site_name']
    st.write("### 📊 Side-by-Side Metrics")
    metric_rows = []
    for r in results:
        is_winner = (r['site_name'] == winner_name)
        metric_rows.append({
            '🏆': '🏆' if is_winner else '',
            'Site': r['site_name'],
            'Score': f"{r['suitability_percentage']}% {r['rating_emoji']}",
            'Illum %': f"{r['illumination_pct']:.0f}",
            'Slope °': f"{r['slope_deg']:.1f}",
            'Ice %': f"{r['ice_confidence']*100:.0f}",
            'Temp K': f"{r['temperature_k']:.0f}",
            'Subsurface': r['lava_tube_proximity'],
            'Comms': r['earth_visibility'].capitalize(),
            'Rating': r['rating'],
        })
    df_compare = pd.DataFrame(metric_rows)
    st.dataframe(df_compare, use_container_width=True, hide_index=True)
    st.write("### 🕸️ Radar Comparison")
    categories = ['Illumination', 'Ice', 'Slope', 'Temperature', 'Regolith', 'Comms', 'Subsurface']
    fig_radar = go.Figure()
    palette = ['#b464ff', '#00e5ff', '#40e0d0', '#ff2d95']
    for i, r in enumerate(results):
        d = r['details']
        values = [
            d['illumination']['score'],
            d['ice_access']['score'],
            d['slope_safety']['score'],
            d['temperature']['score'],
            d['regolith']['score'],
            d['comms']['score'],
            d['subsurface_access']['score'],
        ]
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=r['site_name'][:25],
            line=dict(color=palette[i % len(palette)], width=2),
            opacity=0.6,
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor='rgba(15,8,30,0.6)',
            radialaxis=dict(visible=True, range=[0, 5], gridcolor='rgba(180,100,255,0.2)'),
            angularaxis=dict(gridcolor='rgba(180,100,255,0.15)'),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=450,
        legend=dict(bgcolor='rgba(0,0,0,0)'),
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.write("### 🏆 Recommended Site")
    st.markdown(f"""
    <div class="recommendation-container" style="border-color: #39ff14;">
        <div class="recommendation-title" style="color: #39ff14;">🏆 {winner_name}</div>
        <div style="color: #ffffff; font-size: 1rem; padding: 6px;">
            Highest suitability score: <b style="color: #00e5ff;">{winner['suitability_percentage']}%</b>
            ({winner['rating']} {winner['rating_emoji']})
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_simulation_lab():
    st.subheader("🧪 Simulation Lab (What-If)")
    st.markdown("Adjust parameters to see how the mission scales.")
    col1, col2, col3 = st.columns(3)
    with col1:
        crew_size = st.slider("Crew Size", 4, 100, 10)
    with col2:
        habitat_mass = st.slider("Habitat Mass (Tons)", 50, 500, 150)
    with col3:
        power_source = st.selectbox("Power Source", ["Hybrid (Solar+Nuclear)", "Solar Only", "Nuclear Only"])
    base_cost = 500000.0
    new_cost = base_cost + (crew_size * 5000.0) + (habitat_mass * 1000.0)
    if power_source == "Nuclear Only": new_cost += 50000.0
    if power_source == "Solar Only": new_cost -= 30000.0
    air_needed = crew_size * 200
    water_needed = crew_size * 150
    regolith_shielding = crew_size * 20
    st.markdown("---")
    st.write("### 📊 Updated Mission Output")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("New Cost", f"${new_cost/1000:.0f}T")
    with c2: st.metric("Air Needed", f"{air_needed:,} L/day")
    with c3: st.metric("Water Needed", f"{water_needed:,} L/day")
    with c4: st.metric("Regolith Shield", f"{regolith_shielding:,} tons")

def render_memory_explorer():
    st.subheader("💾 Memory Explorer")
    analyses = st.session_state.memory_repo.get_all_analyses(limit=20)
    if analyses:
        st.write(f"**{len(analyses)} past analyses**")
        for entry in analyses:
            qprev = entry['query'][:50] + "..." if len(entry['query']) > 50 else entry['query']
            with st.expander(f"{'✅' if entry['success'] else '❌'} {qprev}"):
                st.write(f"**Query:** {entry['query']}")
                st.write(f"**Time:** {entry['execution_time']:.2f}s")
                st.write(f"**Timestamp:** {entry['timestamp']}")
    else:
        st.info("No past analyses yet.")

# ============================================================================
# MAIN
# ============================================================================

def main():
    st.set_page_config(page_title="TRAPPIST-1e Base", page_icon="🌟", layout="wide")
    st.markdown(TRAPPIST_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div class="main-title">🌟 TRAPPIST-1e</div>
        <div class="subtitle">🌟 EXOPLANET BASE SELECTION · v1.0.0</div>
        <div style="display: flex; justify-content: center; gap: 10px; margin: 10px 0;">
            <span class="phase-badge phase-badge-2">☀️ ILLUMINATION</span>
            <span class="phase-badge phase-badge-3">💧 ICE</span>
            <span class="phase-badge phase-badge-4">🌊 OCEAN</span>
            <span class="phase-badge phase-badge-5">🧬 BIOSIGNATURE</span>
        </div>
        <div class="cyber-divider"></div>
        <div class="trappist-banner">
            🛰️ JWST DATA · ☀️ ILLUMINATION · 💧 ICE · 🌊 OCEAN · 🧬 BIOSIGNATURE · 🪨 REGOLITH
        </div>
    </div>
    """, unsafe_allow_html=True)
    init_session_state()
    region = render_region_switcher()
    region_sites = [k for k, v in TRAPPIST_SITES.items() if v['region'] == region]
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 8px 15px;
         border: 1px solid rgba(180,100,255,0.15); border-radius: 8px;
         background: rgba(180,100,255,0.03); margin-bottom: 15px;">
        <span style="color: #00e5ff; font-family: 'Courier New'; font-size: 0.7rem;">📍 SITES LOADED</span>
        <span style="color: #b464ff; font-family: 'Courier New'; font-size: 0.8rem; font-weight: bold;">{len(region_sites)} candidate sites</span>
        <span style="color: #00e5ff; font-family: 'Courier New'; font-size: 0.6rem;">{region.replace('_', ' ').upper()}</span>
    </div>
    """, unsafe_allow_html=True)
    params = render_sidebar(region)
    col1, col2 = st.columns([1.5, 1])
    with col1:
        render_map(params, region)
        render_query_interface(params, region)
    with col2:
        if st.session_state.selected_site_name:
            st.markdown(f"""
            <div style="padding: 10px 15px; border: 1px solid rgba(180,100,255,0.2);
                 border-radius: 8px; background: rgba(180,100,255,0.03); margin-bottom: 15px;">
                <div style="color: #00e5ff; font-family: 'Courier New'; font-size: 0.6rem; letter-spacing: 1px;">SELECTED SITE</div>
                <div style="color: #b464ff; font-family: 'Courier New'; font-size: 0.9rem;">{st.session_state.selected_site_name}</div>
            </div>
            """, unsafe_allow_html=True)
    st.divider()
    col_cmp1, col_cmp2 = st.columns([1, 3])
    with col_cmp1:
        st.session_state.compare_mode = st.toggle(
            "⚖️ Compare Mode",
            value=st.session_state.compare_mode,
            help="Enable side-by-side comparison of up to 3 sites."
        )
    if st.session_state.compare_mode:
        render_compare_mode(region)
        st.divider()
    if st.session_state.current_results:
        tab1, tab2 = st.tabs(["📊 Analysis Results", "🛰️ NASA Eyes on Exoplanets"])
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                render_results()
            with col2:
                render_memory_explorer()
            with st.expander("🧪 Simulation Lab (What-If)"):
                render_simulation_lab()
        with tab2:
            st.markdown("### 🛰️ NASA Eyes on Exoplanets — TRAPPIST-1")
            st.markdown("Powered by **NASA's Eyes on Exoplanets**.")
            components.iframe(
                src="https://eyes.nasa.gov/apps/exo/#/planet/TRAPPIST-1_e",
                height=600, scrolling=True
            )
    else:
        render_memory_explorer()
    st.markdown("""
    <div class="cyber-divider"></div>
    <div style="text-align: center; padding: 15px 0; color: #333; font-family: 'Courier New'; 
         font-size: 0.6rem; letter-spacing: 2px;">
        <span style="color: #b464ff;">[</span> 
        TRAPPIST-1e BASE v1.0.0 · JWST DATA · EXOPLANET-ALIGNED
        <span style="color: #b464ff;">]</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 40px 0;">
        <a href="https://buymeacoffee.com/stargazex" target="_blank"> 
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                 alt="Buy Me A Coffee" 
                 style="height: 60px !important;width: 217px !important;" > 
        </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()