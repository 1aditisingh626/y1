import streamlit as st

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="How Broke Are You?",
    page_icon="💸",
    layout="centered"
)

st.title("💸 How Broke Are You?")
st.caption("A brutal finance reality check 😬")

# --------------------------------
# INPUTS
# --------------------------------
income = st.number_input("💰 Monthly Income (₹)", min_value=0, step=1000)
expense = st.number_input("💸 Monthly Expenses (₹)", min_value=0, step=1000)
savings = st.number_input("🏦 Monthly Savings (₹)", min_value=0, step=500)

city = st.selectbox(
    "🏙️ Select Your City Type",
    ["Metro", "Tier-2", "Village"]
)

age = st.slider("🎂 Your Age", 16, 50, 22)

# --------------------------------
# BUTTON
# --------------------------------
if st.button("Check My Broke Status 💀"):

    if income == 0:
        st.error("Income 0 hai… system hi crash ho gaya 😭")

    else:
        # City cost factor
        if city == "Metro":
            city_factor = 0.15
        elif city == "Tier-2":
            city_factor = 0.08
        else:
            city_factor = 0

        adjusted_expense = expense + (expense * city_factor)
        ratio = adjusted_expense / income

        st.write("---")

        # --------------------------------
        # BROKE LEVELS
        # --------------------------------
        if ratio >= 1:
            st.error("💀 ULTRA BROKE 💀")
            st.write("🫠 UPI balance dekh ke phone silent ho jata hai")
            verdict = "Paisa aata hi nahi, jaata hi jaata hai"

        elif ratio >= 0.7:
            st.warning("😬 SURVIVAL MODE 😬")
            st.write("💳 Salary aati hai, EMI le jaati hai")
            verdict = "Zindagi chal rahi hai, savings nahi"

        elif ratio >= 0.4:
            st.info("😐 MIDDLE CLASS PRO MAX 😐")
            st.write("📈 Dreams high, bank balance low")
            verdict = "Stable ho, par secure nahi"

        else:
            st.success("😎 RICH (FOR NOW) 😎")
            st.write("💸 Aaj party, kal ka kal dekhenge")
            verdict = "Filhaal toh paisa tumhare control mein hai"
            st.balloons()

        # --------------------------------
        # SAVINGS ROAST
        # --------------------------------
        if savings == 0:
            st.error("🏦 Savings = 0 😭  Bhavishya bhi broke hai")

        # --------------------------------
        # AGE REALITY CHECK
        # --------------------------------
        if age >= 30 and ratio >= 0.7:
            st.error("⚠️ Age + Broke = Serious Combo 💀")
        elif age < 25 and ratio >= 0.7:
            st.info("🧒 Young ho, sudharne ka time hai")

        # --------------------------------
        # BROKE METER
        # --------------------------------
        broke_score = min(int(ratio * 100), 100)
        st.progress(broke_score)

        st.write(f"📊 **Broke Meter:** `{broke_score}%`")
        st.write(f"🧾 **Final Verdict:** {verdict}")
