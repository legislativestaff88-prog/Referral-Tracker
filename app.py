import streamlit as st
import pandas as pd

# -------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(page_title="SP Oroquieta - Committee Referrals Tracker", layout="wide")

# Simple Password Protection System
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "Oroquieta2026": # <-- CHANGE PASSWORD HERE
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Enter Password to Access System:", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "Enter Password to Access System:", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect. Please try again.")
        return False
    else:
        # Password correct.
        return True

# -------------------------------------------------------------
# 2. PASSWORD CHECK
# -------------------------------------------------------------
if check_password():
    
    # -------------------------------------------------------------
    # 3. INITIALIZE DATA SYSTEM (MOCKING INITIAL FILE DATA)
    # -------------------------------------------------------------
    if 'referrals_df' not in st.session_state:
        # Pre-loading data provided from your logs
        initial_data = [
            # 2025 Data
            {"CY": "2025", "No.": 1, "Date & Time": "July 30, 2025 1:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "1st INDORSEMENT FROM CITY MAYOR RE: ESTATE OF PEDRO ARCE AND CARMEN BARRICA ARCE REALTY TAX REDEMPTION", "Status": "DATE REPORTED: CR No. xx-xx-xxx PR No. xxx-2026 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 2, "Date & Time": "TBS", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "1ST INDORSEMENT RE: DILG ADVISORY ON HOMEOWNERS ASSOCIATION (HOA) ELECTIONS", "Status": "DATE REPORTED: Pending updates", "Is Acted": False},
            {"CY": "2025", "No.": 8, "Date & Time": "Sept 9, 2025 9:00 AM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "LIGA NG MGA BARANGAY PRESIDENT RE: LAND BOUNDARY DISPUTES", "Status": "DATE REPORTED: July 28, 2025 CR No. 25-09-154 PR No. 190-2025 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 11, "Date & Time": "Sept 9, 2025 2:30 PM", "Committee/s": "Committee on Civil Service, Personnel Welfare and Development", "Subject": "PROPOSED CITY RESOLUTION NO. 166-2025 FOR CREATION OF LEDIPO POSITION", "Status": "DATE REPORTED: September 15, 2025 CR No. 2025-09-188 PR No. 189-2025 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 13, "Date & Time": "Oct 8, 2025", "Committee/s": "Committee on Ethics and Good Governance", "Subject": "COMPLAINT AGAINST DIANE JANE ADLAON CORONEL FOR ADMINISTRATIVE ADJUDICATION", "Status": "DATE REPORTED: February 23, 2026 CR No. 26-02-045 Amicable Agreement signed", "Is Acted": True},
            {"CY": "2025", "No.": 15, "Date & Time": "Oct 22, 2025 2:30 PM", "Committee/s": "Committee on Civil Service, Personnel Welfare and Development", "Subject": "REITERATING NEED TO CREATE CITY COOPERATIVES DEVELOPMENT OFFICER (SG 25)", "Status": "DATE REPORTED: February 9, 2026 CR No. 26-02-021 (WITH MINUTES)", "Is Acted": True},
            
            # 2026 Data
            {"CY": "2026", "No.": 1, "Date & Time": "Jan 28, 2026 2:30 PM", "Committee/s": "Committee on Civil Service, Personnel Welfare and Development", "Subject": "CITY VETERINARIAN REQUEST FOR INCLUSION OF POSITION TITLES AND SALARY RATES FOR JOB ORDER WORKERS", "Status": "DATE REPORTED: CR No. 26-xx-xxx PO No. xxx-2026 (Sent to HRMO)", "Is Acted": True},
            {"CY": "2026", "No.": 2, "Date & Time": "Feb 18, 2026 1:00 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "PSDP APPLICATION OF LORENZO TAN MULTI-PURPOSE COOPERATIVE (LTMPC)", "Status": "DATE REPORTED: February 23, 2026 CR No. 26-02-041 PR No. 064-2026 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2026", "No.": 6, "Date & Time": "Apr 10, 2026 9:00 AM", "Committee/s": "Committee on Ethics and Good Governance", "Subject": "COMPLAINT FILED AGAINST PUNONG BARANGAY NILA M. MADERSE OF TALAIRON", "Status": "DATE REPORTED: Pending Investigation", "Is Acted": False},
            {"CY": "2026", "No.": 16, "Date & Time": "May 7, 2026 1:00 PM", "Committee/s": "Committee of the Whole", "Subject": "COASTAL MASTER PLAN AND WATERFRONT DEVELOPMENT PLAN PRESENTATION BY ER&B ASSOCIATES", "Status": "DATE REPORTED: Review ongoing", "Is Acted": False}
        ]
        st.session_state.referrals_df = pd.DataFrame(initial_data)

    df = st.session_state.referrals_df

    # -------------------------------------------------------------
    # 4. DASHBOARD HEADER & LIVE STATISTICS SUMMARY
    # -------------------------------------------------------------
    st.title("🏛️ Sangguniang Panlungsod Referral & Action Tracking System")
    st.subheader("Oroquieta City Legislative Ledger Management")
    
    st.markdown("---")
    
    # Dynamic Summary Table Calculations (Calculated directly from live entry logs)
    st.markdown("### 📊 Automated Calendar Year Summary Accounts")
    selected_summary_cy = st.selectbox("Select Calendar Year Summary View:", ["2026", "2025"])
    
    # Filter for active statistics window
    stat_df = df[df['CY'] == selected_summary_cy]
    
    # Generate statistics grouped by structured committees
    committees_list = [
        "Committee on Housing, Land Use and Zoning",
        "Committee on Civil Service, Personnel Welfare and Development",
        "Committee on Ethics and Good Governance",
        "Committee of the Whole"
    ]
    
    summary_rows = []
    for comp in committees_list:
        comp_data = stat_df[stat_df['Committee/s'] == comp]
        total_refs = len(comp_data)
        acted = len(comp_data[comp_data['Is Acted'] == True])
        pending = len(comp_data[comp_data['Is Acted'] == False])
        summary_rows.append({"COMMITTEE": comp, "REFERRAL": total_refs, "ACTED": acted, "PENDING": pending})
        
    st.table(pd.DataFrame(summary_rows))
    
    st.markdown("---")

    # -------------------------------------------------------------
    # 5. INPUT DATA PORTAL (ADD NEW ENTRIES)
    # -------------------------------------------------------------
    with st.expander("➕ Input Portal: Log New Committee Referral / Action Taken"):
        with st.form("referral_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                cy_input = st.selectbox("Calendar Year (CY):", ["2026", "2025", "2027"])
                no_input = st.number_input("Tracking Number (No.):", min_value=1, step=1)
            with col2:
                date_input = st.text_input("Date & Time Logged:", placeholder="e.g., October 23, 2026 3:30 PM")
                committee_input = st.selectbox("Assign Committee/s:", committees_list)
            with col3:
                action_status = st.checkbox("Mark as Acted / Completed Immediately?")
                
            subject_input = st.text_area("Official Legislative Subject / Document Details:")
            status_input = st.text_area("Action Taken / Committee Report (CR) Status Details:")
            
            submit_btn = st.form_submit_button("Save Log Entry to Secure Database")
            
            if submit_btn:
                new_row = {
                    "CY": cy_input,
                    "No.": int(no_input),
                    "Date & Time": date_input,
                    "Committee/s": committee_input,
                    "Subject": subject_input,
                    "Status": status_input,
                    "Is Acted": action_status
                }
                st.session_state.referrals_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ Successfully registered Tracking Entry No. {no_input} to CY {cy_input} Repository!")
                st.rerun()

    # -------------------------------------------------------------
    # 6. MASTER DATABASE VIEW & DATA MANIPULATION
    # -------------------------------------------------------------
    st.markdown("### 🔍 Search & Data Repository Workspace")
    
    # Structural filters
    search_col1, search_col2 = st.columns([1, 3])
    with search_col1:
        filter_cy = st.radio("Filter Database Year:", ["All", "2026", "2025"])
    with search_col2:
        search_query = st.text_input("Live Query Filter (Search by Subject, Committee, or Document References):")

    # Apply structural system database filters
    display_df = df.copy()
    if filter_cy != "All":
        display_df = display_df[display_df['CY'] == filter_cy]
    if search_query:
        display_df = display_df[
            display_df['Subject'].str.contains(search_query, case=False, na=False) |
            display_df['Committee/s'].str.contains(search_query, case=False, na=False) |
            display_df['Status'].str.contains(search_query, case=False, na=False)
        ]

    # Clean rendering frame configuration
    display_df = display_df.rename(columns={"Is Acted": "Acted Status Indicator"})
    st.dataframe(display_df, use_container_width
