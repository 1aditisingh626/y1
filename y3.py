import streamlit as st
import datetime
import hashlib

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Cricket Performance Predictor", page_icon="🏏")
st.title("🔮 Next Match Performance Predictor")
st.caption("⚠️ Fun + logic based | Not real prediction")

# -------------------------------
# PLAYER DATA
# -------------------------------
players = {
    "Virat Kohli": {"role": "Top Order", "position": "Opener", "base": (35, 85)},
    "Rohit Sharma": {"role": "Opener", "position": "Opener", "base": (30, 80)},
    "Shubman Gill": {"role": "Opener", "position": "Opener", "base": (28, 78)},
    "KL Rahul": {"role": "Anchor", "position": "Middle", "base": (25, 70)},
    "Hardik Pandya": {"role": "Finisher", "position": "Lower", "base": (18, 55)},
    "Jasprit Bumrah": {"role": "Bowler", "position": "Lower", "base": (5, 25)}
}

match_types = ["T20", "ODI", "Test"]
venues = ["Home", "Away"]
modes = ["International", "IPL"]
match_importance = ["League Match", "Knockout Match"]

pitch_types = ["Flat Pitch 🏏", "Green Pitch 🌿", "Spin Pitch 🌀"]

# -------------------------------
# OPPOSITION TEAMS (HIDDEN LOGIC)
# -------------------------------
opposition_teams = {
    "Australia 🇦🇺": "Strong",
    "England 🏴": "Strong",
    "Pakistan 🇵🇰": "Average",
    "South Africa 🇿🇦": "Strong",
    "Sri Lanka 🇱🇰": "Average",
    "Bangladesh 🇧🇩": "Weak",
    "Afghanistan 🇦🇫": "Weak",
    "Nepal 🇳🇵": "Weak"
}

ipl_teams = ["CSK 🦁", "MI 🔵", "RCB 🔴", "KKR 🟣", "GT ⚡"]

# -------------------------------
# INPUTS
# -------------------------------
player = st.selectbox("🏏 Select Player", list(players.keys()))
match_type = st.selectbox("📋 Match Type", match_types)
mode = st.selectbox("🌍 Match Mode", modes)

if mode == "IPL":
    team = st.selectbox("🆚 Opposition Team", ipl_teams)
    strength = "Average"
else:
    team = st.selectbox("🆚 Opposition Team", list(opposition_teams.keys()))
    strength = opposition_teams[team]

venue = st.selectbox("🏟️ Match Venue", venues)
importance = st.selectbox("🏆 Match Importance", match_importance)
pitch = st.selectbox("🌱 Pitch Type", pitch_types)

today = datetime.date.today()

# -------------------------------
# BUTTON
# -------------------------------
if st.button("Predict Performance 🔮"):

    unique = f"{player}-{match_type}-{team}-{venue}-{importance}-{pitch}-{mode}-{today}"
    h = hashlib.md5(unique.encode()).hexdigest()

    # -------------------------------
    # BASE RUNS
    # -------------------------------
    min_r, max_r = players[player]["base"]
    runs = min_r + (int(h[:2], 16) % (max_r - min_r))

    # -------------------------------
    # POSITION EFFECT
    # -------------------------------
    if players[player]["position"] == "Opener":
        runs += 10
    elif players[player]["position"] == "Lower":
        runs -= 5

    # -------------------------------
    # OPPOSITION EFFECT
    # -------------------------------
    if strength == "Weak":
        runs += 15
    elif strength == "Strong":
        runs -= 12

    # -------------------------------
    # VENUE EFFECT
    # -------------------------------
    runs += 8 if venue == "Home" else -5

    # -------------------------------
    # MATCH IMPORTANCE EFFECT
    # -------------------------------
    if importance == "Knockout Match":
        runs -= 5  # pressure

    # -------------------------------
    # PITCH EFFECT
    # -------------------------------
    if "Green" in pitch:
        runs -= 8
    elif "Spin" in pitch:
        runs -= 5
    else:
        runs += 5

    # -------------------------------
    # MATCH TYPE & MODE
    # -------------------------------
    if match_type == "T20":
        strike_rate = int(h[2:4], 16) % 80 + (145 if mode == "IPL" else 120)
    elif match_type == "ODI":
        runs += 10
        strike_rate = int(h[2:4], 16) % 50 + 85
    else:  # Test
        runs += 25
        strike_rate = int(h[2:4], 16) % 25 + 45

    runs = max(0, runs)

    # -------------------------------
    # VERDICT
    # -------------------------------
    if runs < 20:
        verdict = "💀 Net practice vibes"
    elif runs < 50:
        verdict = "🙂 Decent contribution"
    elif runs < 80:
        verdict = "🔥 Match defining knock"
    else:
        verdict = "🐐 All-time classic"

    # -------------------------------
    # DISPLAY
    # -------------------------------
    st.write("---")
    st.subheader(f"{player} vs {team}")

    st.metric("🏏 Predicted Runs", runs)
    st.metric("⚡ Strike Rate", strike_rate)

    st.progress(min(runs, 100))

    st.success(f"🏆 Verdict: {verdict}")
    st.caption("🔁 Same selections + same day = same result | Try tomorrow 😉")
