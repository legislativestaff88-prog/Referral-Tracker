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
        st.text_input("Enter Password to Access System:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Password to Access System:", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect. Please try again.")
        return False
    else:
        return True

# -------------------------------------------------------------
# 2. PASSWORD CHECK
# -------------------------------------------------------------
if check_password():
    
    # -------------------------------------------------------------
    # 3. INITIALIZE SECURE DATABASE WORKSPACE (ALL DATA RECOVERY)
    # -------------------------------------------------------------
    if 'referrals_df' not in st.session_state:
        initial_data = [
            # --- 2025 FULL MASTER LOG ENTRIES ---
            {"CY": "2025", "No.": 1, "Date & Time": "July 30, 2025 1:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "1st INDORSEMENT FROM CITY MAYOR RE: ESTATE OF PEDRO ARCE AND CARMEN BARRICA ARCE REALTY TAX REDEMPTION", "Status": "DATE REPORTED: (Committee Order sent to CTO) CR No. xx-xx-xxx PR No. xxx-2026 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 2, "Date & Time": "TBS", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "1ST INDORSEMENT RE: DILG ADVISORY ON HOMEOWNERS ASSOCIATION (HOA) ELECTIONS", "Status": "DATE REPORTED: CR No.  PR No.", "Is Acted": False},
            {"CY": "2025", "No.": 3, "Date & Time": "July 23, 2026 1:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "SANGGUNIANG BARANGAY OF CIRIACO PASTRANO RES NO. 18 S. 2021 RE: BARANGAY CEMETERY", "Status": "DATE REPORTED: July 27, 2026 CR No. 26-07-174 PR No. 240-2026 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 4, "Date & Time": "July 23, 2026 1:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "3RD INDORSEMENT RE: OCPDC VERIFICATION AND INSPECTION ON BSSP LOT FOR CEMETERY PURPOSE", "Status": "DATE REPORTED: July 27, 2026 CR No. 26-07-174 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 5, "Date & Time": "July 23, 2026 1:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "3RD INDORSEMENT RE: CITY ASSESSOR COMMENT ON PROPOSED CEMETERY IN CIRIACO PASTRANO", "Status": "DATE REPORTED: July 27, 2026 CR No. 26-07-174 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 6, "Date & Time": "July 23, 2026 1:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "BARANGAY OF TUYABANG PROPER RESOLUTION NO. 028-2021 RE: BSSP LAND FOR BARANGAY CEMETERY", "Status": "DATE REPORTED: July 27, 2026 CR No. 26-07-174 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 7, "Date & Time": "July 23, 2026 1:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "RESOLUTION NO. 10-2022 OF BARANGAY BOLIBOL FOR APPROVAL OF CEMETERY IN PUROK-2", "Status": "DATE REPORTED: July 27, 2026 CR No. 26-07-174 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 8, "Date & Time": "Sept 9, 2025 9:00 AM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "LIGA NG MGA BARANGAY PRESIDENT RE: ONGOING LAND BOUNDARY DISPUTES AMONG BARANGAYS", "Status": "DATE REPORTED: July 28, 2025 CR No. 25-09-154 PR No. 190-2025 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 9, "Date & Time": "Oct 23, 2025 3:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "USTP CAMPUS DIRECTOR REQUEST FOR COPY OF CONFIRMATION OF SALE / DEED OF ABSOLUTE SALE", "Status": "DATE REPORTED: October 27, 2025 CR No. 2025-10-192 PR No. 229-2025 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 10, "Date & Time": "Oct 1, 2025 3:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "REQUEST FOR CONFIRMATION LETTER RE: DEED OF CONVEYANCE - LGU AND HEIRS OF JORGE FABRIGA", "Status": "DATE REPORTED: (RESURVEY) awaiting CLO response CR No. 2026-xx-xxx", "Is Acted": False},
            {"CY": "2025", "No.": 11, "Date & Time": "Sept 9, 2025 2:30 PM", "Committee/s": "Committee on Civil Service, Personnel Welfare and Development", "Subject": "PROPOSED CITY RESOLUTION NO. 166-2025 FOR CREATION/DESIGNATION OF LEDIPO FOR INVESTMENT PROMOTION", "Status": "DATE REPORTED: September 15, 2025 CR No. 2025-09-188 PR No. 189-2025 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 12, "Date & Time": "Oct 1, 2025", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "ORDINANCE TO ENSURE HARMONY BETWEEN ROAD ALIGNMENT AND TECHNICAL LOT DESCRIPTIONS ALONG PRES. E. QUIRINO ST", "Status": "DATE REPORTED: (RESURVEY) CR No.  PR No.", "Is Acted": False},
            {"CY": "2025", "No.": 13, "Date & Time": "Oct 8, 2025", "Committee/s": "Committee on Ethics and Good Governance", "Subject": "DEPUTY OMBUDSMAN COMPLAINT FOR ADMINISTRATIVE ADJUDICATION AGAINST DIANE JANE ADLAON CORONEL", "Status": "DATE REPORTED: February 23, 2026 CR No. 26-02-045 PR No. 070-2026 (Nov.7 Amicable Agreement signed)", "Is Acted": True},
            {"CY": "2025", "No.": 14, "Date & Time": "Sept 30, 2025 10:30 AM", "Committee/s": "Committee on Civil Service, Personnel Welfare and Development", "Subject": "SCHOLARSHIP SERVICE CONTRACT APPROVAL FOR CITY AGRICULTURIST MR. MAYNARD C. BONGCAYAO AT DAP", "Status": "DATE REPORTED: September 24, 2025 CR No. 25-10-168 PR No. 205-2025 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 15, "Date & Time": "Oct 22, 2025 2:30 PM", "Committee/s": "Committee on Civil Service, Personnel Welfare and Development", "Subject": "CREATION OF CITY COOPERATIVES DEVELOPMENT OFFICER POSITION (SG 25) COMPLIANCE WITH RA 11535", "Status": "DATE REPORTED: February 9, 2026 CR No. 26-02-021 PR No. 002-2026 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 16, "Date & Time": "Nov 18, 2025 3:00 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "APPROVING AND ADOPTING CITY'S FOREST LAND USE PLAN (FLUP) CY 2025-2029 AND DENR-10 MOA", "Status": "DATE REPORTED: - CR No. 26-xx-xxx (REVIEW THE FLUP)", "Is Acted": False},
            {"CY": "2025", "No.": 17, "Date & Time": "Oct 22, 2025 3:00 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "PRELIMINARY SUBDIVISION DEVELOPMENT PLAN OF ZENAIDA T. TIZON (3,250 SQM) AT VILLAFLOR", "Status": "DATE REPORTED: October 27, 2025 CR No. 25-10-193 PR No. 230-2025 (PSDP)", "Is Acted": True},
            {"CY": "2025", "No.": 18, "Date & Time": "Oct 22, 2025 3:00 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "PRELIMINARY SUBDIVISION DEVELOPMENT PLAN OF SERGIO ADLAON AND JOAN VILLANUEVA (8,174 SQM) AT VILLAFLOR", "Status": "DATE REPORTED: October 27, 2025 CR No. 25-10-193 PR No. 232-2025 (PSDP)", "Is Acted": True},
            {"CY": "2025", "No.": 19, "Date & Time": "Oct 22, 2025 3:00 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "PRELIMINARY SUBDIVISION DEVELOPMENT PLAN OF KENT RICKX S. PEDE (11,436 SQM) AT TALAIRON", "Status": "DATE REPORTED: October 27, 2025 CR No. 25-10-193 PR No. 233-2025 (PSDP)", "Is Acted": True},
            {"CY": "2025", "No.": 20, "Date & Time": "TBS", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "PROPOSED CITY ORDINANCE NO. 029-2025 AN ORDINANCE CREATING THE LOCAL HOUSING BOARD", "Status": "DATE REPORTED: - (For update) CR No. 26-xx-xxx PR No. xx-2026", "Is Acted": False},
            {"CY": "2025", "No.": 21, "Date & Time": "Nov 18, 2025", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "PRELIMINARY SUBDIVISION DEVELOPMENT PLAN OF MR. GERRY I. LAMPARAS (4,600 SQM) AT LOWER LAMAC", "Status": "DATE REPORTED: June 22, 2026 CR No. 26-06-151 PR No. 198-2026 (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 22, "Date & Time": "Jan 21, 2026 2:30 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "PRELIMINARY SUBDIVISION DEVELOPMENT PLAN OF MR. JACINTO AGUHOB (2,178 SQM) AT UPPER RIZAL", "Status": "DATE REPORTED: FEBRUARY 2, 2026 CR No. 26-02-031 Item #2 (Moot & Academic) (WITH MINUTES)", "Is Acted": True},
            {"CY": "2025", "No.": 23, "Date & Time": "TBS", "Committee/s": "Committee on Civil Service, Personnel Welfare and Development", "Subject": "PROJECT SELF-HELP: SUSTAINABLE ECONOMIC LINKAGES FOR FISHERFOLKS BY MARK ANTHONY D. ARTIGAS", "Status": "DATE REPORTED: Pending review", "Is Acted": False},
            {"CY": "2025", "No.": 24, "Date & Time": "Dec 10, 2025 3:00 PM", "Committee/s": "Committee on Housing, Land Use and Zoning", "Subject": "AUTHORIZING DEED OF ABSOLUTE SALE IN FAVOR OF THE HEIRS OF JOSE FLORES", "Status": "DATE REPORTED: December 15, 2025 CR No. 25-12-232 PR No. 278-2025 (WITH MINUTES)", "Is Acted": True}
