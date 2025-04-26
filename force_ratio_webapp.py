import streamlit as st
import random

# --- Unit Library ---
unit_library = {
    'Infantry Company': {'strength': 100, 'oli': 1.0},
    'Tank Squadron': {'strength': 60, 'oli': 1.5},
    'Artillery Battery': {'strength': 50, 'oli': 1.2},
    'Engineer Platoon': {'strength': 40, 'oli': 0.8}
}

# --- Terrain Effects ---
terrain_modifiers = {
    'Open Terrain': (1.0, 1.0),
    'Forested': (1.0, 1.1),         # defender +10%
    'Urban': (0.8, 1.3),            # attacker -20%, defender +30%
    'Mountainous': (0.85, 1.2)      # attacker -15%, defender +20%
}

# --- Core Functions ---
def apply_modifiers(base_value, modifiers):
    result = base_value
    for mod in modifiers:
        result *= mod
    return result

def calculate_force(units_selected):
    total_strength = 0
    total_power = 0
    for unit, quantity in units_selected.items():
        if quantity > 0:
            unit_data = unit_library[unit]
            total_strength += unit_data['strength'] * quantity
            total_power += (unit_data['strength'] * unit_data['oli']) * quantity
    return total_strength, total_power

def force_ratio_simulation(
    blue_units, blue_modifiers,
    red_units, red_modifiers,
    terrain
):
    blue_strength, blue_power = calculate_force(blue_units)
    red_strength, red_power = calculate_force(red_units)

    terrain_attacker_mod, terrain_defender_mod = terrain_modifiers[terrain]

    blue_power = apply_modifiers(blue_power, blue_modifiers + [terrain_attacker_mod])
    red_power = apply_modifiers(red_power, red_modifiers + [terrain_defender_mod])

    force_ratio = blue_power / red_power if red_power != 0 else 99  # Avoid division by zero

    if force_ratio >= 3.0:
        outcome = random.choices(['Decisive Win', 'Win', 'Draw'], weights=[70, 25, 5])[0]
    elif force_ratio >= 2.0:
        outcome = random.choices(['Win', 'Draw', 'Loss'], weights=[60, 30, 10])[0]
    elif force_ratio >= 1.0:
        outcome = random.choices(['Draw', 'Loss', 'Decisive Loss'], weights=[40, 50, 10])[0]
    else:
        outcome = random.choices(['Loss', 'Decisive Loss'], weights=[30, 70])[0]

    if outcome in ['Decisive Win', 'Win']:
        blue_casualties = random.randint(5, 20)
        red_casualties = random.randint(30, 70)
    elif outcome == 'Draw':
        blue_casualties = random.randint(20, 50)
        red_casualties = random.randint(20, 50)
    else:
        blue_casualties = random.randint(30, 70)
        red_casualties = random.randint(5, 20)

    if force_ratio >= 3.0:
        time_to_achieve = random.randint(1, 2)
    elif force_ratio >= 2.0:
        time_to_achieve = random.randint(2, 4)
    elif force_ratio >= 1.0:
        time_to_achieve = random.randint(4, 7)
    else:
        time_to_achieve = random.randint(7, 14)

    return {
        'Blue Strength': int(blue_strength),
        'Red Strength': int(red_strength),
        'Blue Combat Power': round(blue_power, 1),
        'Red Combat Power': round(red_power, 1),
        'Force Ratio': round(force_ratio, 2),
        'Predicted Outcome': outcome,
        'Blue Casualties (%)': blue_casualties,
        'Red Casualties (%)': red_casualties,
        'Estimated Time (days)': time_to_achieve
    }

# --- Streamlit App Layout ---
st.set_page_config(page_title="Force Ratio Battle Simulator", layout="wide")
st.title("Force Ratio Battle Simulator")

# Battle History Memory
if 'battle_history' not in st.session_state:
    st.session_state.battle_history = []

# Input Area
st.header("Force Selection")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Blue Force")
    blue_units = {}
    for unit in unit_library:
        qty = st.number_input(f"{unit} (Blue)", min_value=0, value=0, step=1)
        blue_units[unit] = qty
    blue_modifiers = st.multiselect(
        "Blue Modifiers",
        options=[
            ("Good Leadership (+10%)", 1.1),
            ("Bad Weather (-10%)", 0.9),
            ("Excellent Morale (+15%)", 1.15),
            ("Poor Supply (-15%)", 0.85)
        ]
    )
    blue_modifier_values = [mod[1] for mod in blue_modifiers]

with col2:
    st.subheader("Red Force")
    red_units = {}
    for unit in unit_library:
        qty = st.number_input(f"{unit} (Red)", min_value=0, value=0, step=1)
        red_units[unit] = qty
    red_modifiers = st.multiselect(
        "Red Modifiers",
        options=[
            ("Good Leadership (+10%)", 1.1),
            ("Bad Weather (-10%)", 0.9),
            ("Excellent Morale (+15%)", 1.15),
            ("Poor Supply (-15%)", 0.85)
        ]
    )
    red_modifier_values = [mod[1] for mod in red_modifiers]

# Terrain Selection
st.header("Terrain")
terrain = st.selectbox(
    "Select Terrain",
    options=list(terrain_modifiers.keys())
)

# Battle Button
if st.button("Simulate Battle"):
    result = force_ratio_simulation(
        blue_units, blue_modifier_values,
        red_units, red_modifier_values,
        terrain
    )
    st.subheader("Battle Outcome")
    for key, value in result.items():
        st.write(f"**{key}:** {value}")

    # Save to Battle History
    st.session_state.battle_history.append(result)

# Display Battle History
if st.session_state.battle_history:
    st.header("Battle History")
    st.table(st.session_state.battle_history)
