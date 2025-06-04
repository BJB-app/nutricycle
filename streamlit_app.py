
import streamlit as st
from datetime import datetime
from nutricycle_app import User, UserPreferences, NutriCycleApp

# Page configuration
st.set_page_config(page_title="NutriCycle", layout="centered")

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #2d0727, #0c0822);
        color: #ffffff;
        font-family: 'sans-serif';
    }
    .stButton > button {
        background-color: #ff4d7e;
        color: white;
        border-radius: 10px;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff10;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and intro
st.title("🌿 NutriCycle")
st.subheader("Live like a woman, feel like a woman — How you feel outside starts with what you feed inside.")

st.markdown(
    "Most women were never taught how their hormones shape their energy, cravings, moods, and needs. "
    "Yet, this wisdom is rarely shared—leaving us guessing why some days we feel unstoppable… and others, completely drained.\n\n"

    "What if you could work with your cycle, not against it? What if the right foods at the right phase could help you feel balanced, energized, and in sync with your body’s natural rhythm?\n\n"

    "That’s where **NutriCycle** comes in. It delivers personalized food recommendations tailored to your current menstrual phase, so that you can:\n"
    "- Fuel energy when estrogen peaks,\n"
    "- Soothe cravings when progesterone rises,\n"
    "- Rebuild strength as your body resets.\n\n"

    "**No more guesswork. Just simple science-backed nourishment, perfectly timed.**"
)

# Input form
with st.form("user_form"):
    name = st.text_input("Your Name:")
    cycle_start = st.date_input("📅 When did your last period start?", value=datetime.today())
    cycle_length = st.number_input("Cycle Length (in days)", min_value=21, max_value=35, value=28)
    period_length = st.number_input("Period Duration (in days)", min_value=3, max_value=10, value=5)
    allergies_input = st.text_input("Any Food Allergies? (comma-separated)", placeholder="e.g. dairy, gluten")

    submitted = st.form_submit_button("Sync My Cycle")

# Logic after submission
if submitted:
    allergies = [a.strip().lower() for a in allergies_input.split(',')] if allergies_input else []
    cycle_start_str = cycle_start.strftime("%d-%m-%Y")

    user = User(name, cycle_start_str, cycle_length, period_length, UserPreferences(allergies))
    app = NutriCycleApp(user)

    st.subheader(f"👤 Profile: {user.get_name()}")

    current_phase = app._NutriCycleApp__tracker.get_current_phase()

    # Show cycle wheel
    st.image("nutricycle_cycle_wheel_final.png", caption="Your Cycle Wheel", use_column_width=True)

    if current_phase:
        st.markdown(f"### 🔄 You are currently in: **{current_phase.get_name()}**")

        if hasattr(current_phase, "get_info"):
            st.info(current_phase.get_info())

        grouped = current_phase.get_grouped_recommendations(user.get_allergies())
        st.markdown("### 🥦 What to Eat This Phase")
        for category, foods in grouped.items():
            st.markdown(f"**{category}**: {', '.join(foods) if foods else 'No safe foods'}")

        st.markdown("### ⚠️ Best to Avoid Right Now")
        st.error(", ".join(current_phase.get_avoid_list()))
    else:
        st.warning("Could not determine your current phase. Please check your inputs.")
