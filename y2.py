import streamlit as st
import datetime
import hashlib

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Luck Meter Today",
    page_icon="🍀",
    layout="centered"
)

st.title("🍀 Luck Meter Today")
st.caption("Same number + same day = same luck | Tomorrow = new luck ✨")

# --------------------------------
# INPUTS
# --------------------------------
name = st.text_input("🧑 Enter Your Name")
number = st.selectbox("🔢 Select a Number", list(range(1, 10)))

# --------------------------------
# DATE INFO
# --------------------------------
today = datetime.date.today()
day_name = today.strftime("%A")

# --------------------------------
# BUTTON
# --------------------------------
if st.button("Check My Luck 🍀"):

    if name.strip() == "":
        st.warning("Name likhna compulsory hai 😅")

    else:
        # --------------------------------
        # CREATE UNIQUE DAILY STRING
        # --------------------------------
        unique_text = f"{name.lower()}-{number}-{today}"

        hash_value = hashlib.md5(unique_text.encode()).hexdigest()

        # --------------------------------
        # LUCK SCORE (0–100)
        # --------------------------------
        luck_score = int(hash_value[:2], 16) % 101

        # --------------------------------
        # LUCK COLOR
        # --------------------------------
        colors = ["Red ❤️", "Blue 💙", "Green 💚", "Yellow 💛", "Purple 💜"]
        lucky_color = colors[int(hash_value[2:4], 16) % len(colors)]

        # --------------------------------
        # LUCKY TIME
        # --------------------------------
        times = [
            "🌅 Morning (6–10 AM)",
            "☀️ Afternoon (12–4 PM)",
            "🌆 Evening (6–9 PM)",
            "🌙 Night (10 PM)"
        ]
        lucky_time = times[int(hash_value[4:6], 16) % len(times)]

        # --------------------------------
        # LUCK ADVICE
        # --------------------------------
        advices = [
            "💰 Paiso ka risk aaj avoid karo",
            "📚 Aaj learning ke liye best day",
            "❤️ Communication pe dhyaan do",
            "🚀 Aaj action lene ka sahi time hai",
            "😌 Calm raho, sab theek hoga"
        ]
        lucky_advice = advices[int(hash_value[6:8], 16) % len(advices)]

        # --------------------------------
        # DISPLAY RESULTS
        # --------------------------------
        st.write("----")
        st.write(f"📅 **Date:** {today}")
        st.write(f"📆 **Day:** {day_name}")

        st.progress(luck_score)
        st.subheader(f"🍀 Your Luck Today: **{luck_score}%**")

        # --------------------------------
        # LUCK LEVELS
        # --------------------------------
        if luck_score <= 25:
            st.error("😭 Very Bad Luck")
        elif luck_score <= 50:
            st.warning("😐 Average Luck")
        elif luck_score <= 75:
            st.success("🙂 Good Luck")
        else:
            st.success("😎 Very Lucky Day")
            st.balloons()

        # --------------------------------
        # EXTRA DETAILS
        # --------------------------------
        st.info(f"🎨 **Lucky Color:** {lucky_color}")
        st.info(f"⏰ **Lucky Time:** {lucky_time}")
        st.info(f"🔮 **Lucky Advice:** {lucky_advice}")

        st.caption("🔁 Come back tomorrow for a new luck result 😉")
