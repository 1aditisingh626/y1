import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Ultimate House Price Predictor 🏠", page_icon="🏠")
st.title("🏠 Ultimate House Price Predictor")
st.caption("ML that thinks like a buyer 🧠 | Beginner Friendly | Fun Insights")

# ---------------------------------
# LOAD DATA
# ---------------------------------
data = pd.read_csv("house_data.csv")

# ---------------------------------
# ENCODING
# ---------------------------------
data_encoded = pd.get_dummies(
    data,
    columns=["location", "property_type", "furnishing"],
    drop_first=True
)

X = data_encoded.drop("price", axis=1)
y = data_encoded["price"]

# ---------------------------------
# TRAIN TEST SPLIT
# ---------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------
# MODEL
# ---------------------------------
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=5,
    random_state=42
)
model.fit(X_train, y_train)

# ---------------------------------
# MODEL PERFORMANCE
# ---------------------------------
r2 = r2_score(y_test, model.predict(X_test))
cv_score = cross_val_score(model, X, y, cv=5).mean()

# ---------------------------------
# INPUT FUNCTION
# ---------------------------------
def get_inputs(tag):
    st.subheader(tag)

    area = st.slider("📐 Area (sqft)", 500, 3000, 1200, key=f"a_{tag}")
    bedrooms = st.selectbox("🛏 Bedrooms", [1,2,3,4,5], key=f"b_{tag}")
    bathrooms = st.selectbox("🚿 Bathrooms", [1,2,3], key=f"ba_{tag}")
    age = st.slider("🏚 House Age (years)", 0, 30, 5, key=f"ag_{tag}")

    location = st.selectbox("📍 Location", data["location"].unique(), key=f"l_{tag}")
    property_type = st.selectbox("🏢 Property Type", data["property_type"].unique(), key=f"p_{tag}")
    furnishing = st.selectbox("🛋 Furnishing", data["furnishing"].unique(), key=f"f_{tag}")

    row = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age": age
    }

    for col in X.columns:
        if col.startswith("location_"):
            row[col] = 1 if col == f"location_{location}" else 0
        elif col.startswith("property_type_"):
            row[col] = 1 if col == f"property_type_{property_type}" else 0
        elif col.startswith("furnishing_"):
            row[col] = 1 if col == f"furnishing_{furnishing}" else 0

    return pd.DataFrame([row])

# ---------------------------------
# MODE
# ---------------------------------
mode = st.radio("🎮 Choose Mode", ["Single House Prediction", "Compare Two Houses"])

# ---------------------------------
# SINGLE MODE
# ---------------------------------
if mode == "Single House Prediction":

    inp = get_inputs("🏠 Enter House Details")

    if st.button("🔮 Predict Price"):
        price = int(model.predict(inp)[0])

        tree_preds = np.array([t.predict(inp)[0] for t in model.estimators_])
        low, high = int(tree_preds.min()), int(tree_preds.max())

        # PRICE REACTION
        if price < 3000000:
            emoji = "😃 Affordable Deal!"
        elif price < 7000000:
            emoji = "🙂 Balanced Choice"
        else:
            emoji = "😲 Luxury Zone!"

        st.success(f"💰 Estimated Price: ₹ {price:,}")
        st.info(f"📊 Confidence Range: ₹ {low:,} – ₹ {high:,}")
        st.write(f"**Market Reaction:** {emoji}")

        st.write(
            "🧠 **ML Insight:** This price is influenced mainly by area, location, "
            "number of bedrooms and house age. Random Forest compares hundreds of similar houses before deciding."
        )

# ---------------------------------
# COMPARISON MODE
# ---------------------------------
else:
    col1, col2 = st.columns(2)

    with col1:
        A = get_inputs("🏠 House A")
    with col2:
        B = get_inputs("🏠 House B")

    if st.button("⚔ Compare Houses"):
        pA = model.predict(A)[0]
        pB = model.predict(B)[0]

        st.metric("House A Price", f"₹ {int(pA):,}")
        st.metric("House B Price", f"₹ {int(pB):,}")

        if pA < pB:
            st.success("🏆 House A is a better value for money")
        else:
            st.success("🏆 House B is a better value for money")

# ---------------------------------
# FEATURE IMPORTANCE (ONLY USEFUL)
# ---------------------------------
st.write("### 🔍 What Affects Price the Most?")
importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

fig, ax = plt.subplots()
importance.head(6).plot(kind="barh", ax=ax)
ax.invert_yaxis()
st.pyplot(fig)

# ---------------------------------
# MODEL TRUST
# ---------------------------------
st.write("### 📈 Model Trust Score")
st.metric("R² Accuracy", f"{round(r2*100,2)} %")
st.metric("Cross Validation Score", f"{round(cv_score*100,2)} %")

st.caption("⚠️ Educational ML project | Predictions are illustrative")
