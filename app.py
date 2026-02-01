import streamlit as st

# --- SIDEBAR MENU ---
st.sidebar.title("🏗️ RMC GROUP ERP")
choice = st.sidebar.radio("Module Select Karein", ["💰 Salary Slip", "🎓 Certificate/Degree"])

if choice == "💰 Salary Slip":
    st.header("Salary Management Module")
    # Yahan Salary wala pura code paste karein
    
elif choice == "🎓 Certificate/Degree":
    st.header("Academic Certificate Module")
    # Yahan Certificate wala pura code paste karein
