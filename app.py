import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import numpy as np
from streamlit_gsheets import GSheetsConnection

# --- Configuration ---
st.set_page_config(page_title="Workout Companion", page_icon="💪", layout="centered")

# --- Database Connection ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # ttl=0 ensures we don't use old cached data if you just updated the sheet
    df = conn.read(ttl=0)
    
    # --- Data Cleaning ---
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    # Force string to keep "10-12" or "30 sec"
    df['Target Reps'] = df['Target Reps'].astype(str).replace('nan', '')
    
    cols_to_numeric = ['Actual Weight (kg)', 'Actual Reps', 'Sets', 'Difficulty (1-10)']
    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not connect to Google Sheet. Error: {e}")
    st.stop()

# ==========================================
# SIDEBAR (Global Navigation & Notes)
# ==========================================
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["🏋️ Tracker", "📈 Analytics", "⚙️ Plan Generator"])

st.sidebar.divider()

# --- FEATURE: POP-UP NOTES ---
# Using an expander makes this accessible on every page without taking up space
with st.sidebar.expander("ℹ️ Warm-up & Guidelines", expanded=False):
    st.markdown("""
    ### 🏃‍♂️ Start Here
    - **Cardio:** 5 min (Elliptical)
    - **First Exercise:** Always do warm-up sets with light weight!
    
    ### 🧘‍♂️ Upper Body Warm-up
    - Arm circles
    - Cat-cow
    - No-money drill
    - Torso twist
    
    ### 🦵 Lower Body Warm-up
    - Leg swings
    - Bodyweight deep squat
    - World's greatest stretch
    """)

# ==========================================
# PAGE 1: TRACKER
# ==========================================
if page == "🏋️ Tracker":
    st.title("Today's Workout")
    
    selected_date = st.date_input("Select Date", datetime.now())
    
    mask = df['Date'].dt.date == selected_date
    day_data = df[mask]

    if day_data.empty:
        st.info("No workout scheduled! Rest day? 🛌")
    else:
        muscles = ", ".join(day_data['Muscle Group'].unique())
        st.caption(f"Focus: {muscles}")
        
        with st.form("log_workout"):
            updates = {}
            for index, row in day_data.iterrows():
                st.markdown(f"**{row['Exercise']}**")
                
                # Layout: Goal | Kg | Reps | RPE
                c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
                
                c1.caption(f"Goal:\n{row['Sets']} x {row['Target Reps']}")
                
                val_w = row['Actual Weight (kg)'] if pd.notna(row['Actual Weight (kg)']) else 0.0
                val_r = row['Actual Reps'] if pd.notna(row['Actual Reps']) else 0.0
                val_d = row['Difficulty (1-10)'] if pd.notna(row['Difficulty (1-10)']) else 0.0
                
                new_w = c2.number_input("Kg", value=float(val_w), key=f"w_{index}")
                new_r = c3.number_input("Reps", value=float(val_r), key=f"r_{index}")
                new_d = c4.number_input("RPE", min_value=0.0, max_value=10.0, value=float(val_d), key=f"d_{index}")
                c4.caption("1=Easy 10=Fail")
                
                updates[index] = {'w': new_w, 'r': new_r, 'd': new_d}
                st.divider()
            
            if st.form_submit_button("✅ Save to Google Sheet"):
                for idx, data in updates.items():
                    df.at[idx, 'Actual Weight (kg)'] = data['w']
                    df.at[idx, 'Actual Reps'] = data['r']
                    df.at[idx, 'Difficulty (1-10)'] = data['d']
                
                conn.update(data=df)
                st.success("Success! Google Sheet updated.")
                st.cache_data.clear()

# ==========================================
# PAGE 2: ANALYTICS
# ==========================================
elif page == "📈 Analytics":
    st.title("Progress Dashboard")
    
    history = df.dropna(subset=['Actual Weight (kg)'])
    
    if history.empty:
        st.warning("No data logged yet.")
    else:
        vol = (history['Sets'] * history['Actual Reps'] * history['Actual Weight (kg)']).sum()
        st.metric("Lifetime Volume", f"{int(vol):,} kg")
        
        st.subheader("Strength Trends")
        ex_list = history['Exercise'].unique()
        selected_ex = st.selectbox("Choose Exercise", ex_list)
        
        chart_data = history[history['Exercise'] == selected_ex]
        
        if not chart_data.empty:
            c = alt.Chart(chart_data).mark_line(point=True).encode(
                x='Date', 
                y='Actual Weight (kg)', 
                tooltip=['Date', 'Actual Weight (kg)', 'Actual Reps', 'Difficulty (1-10)']
            )
            st.altair_chart(c, use_container_width=True)

# ==========================================
# PAGE 3: PLAN GENERATOR
# ==========================================
elif page == "⚙️ Plan Generator":
    st.title("Plan Creator")
    st.info("Use this to generate CSV data for next month.")
    
    with st.form("generator_form"):
        min_date = df['Date'].min()
        source_date = st.date_input("Template Week Start", min_date)
        weeks_to_generate = st.slider("Weeks to add", 1, 12, 4)
        start_new_date = st.date_input("Start New Plan On", datetime.now() + timedelta(days=1))
        
        if st.form_submit_button("Generate CSV"):
            source_start = pd.Timestamp(source_date)
            source_end = source_start + timedelta(days=6)
            template_df = df[(df['Date'] >= source_start) & (df['Date'] <= source_end)].copy()
            
            if not template_df.empty:
                new_rows = []
                for w in range(weeks_to_generate):
                    week_offset = w * 7
                    week_df = template_df.copy()
                    base_shift = pd.Timestamp(start_new_date) - source_start
                    
                    week_df['Date'] = week_df['Date'] + base_shift + timedelta(days=week_offset)
                    week_df['Day'] = week_df['Date'].dt.day_name().str[:3]
                    
                    # Reset logs
                    week_df['Actual Weight (kg)'] = np.nan
                    week_df['Actual Reps'] = np.nan
                    week_df['Difficulty (1-10)'] = np.nan
                    
                    new_rows.append(week_df)
                
                generated_df = pd.concat(new_rows)
                csv = generated_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download New Plan CSV", csv, "new_plan.csv", "text/csv")
            else:
                st.error("No data found in source week.")
