"""Movement Report page for Streamlit"""
import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime

def show(db, role):
    """Display movement report page"""
    st.markdown('<h1 class="main-header">Movement Report</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Report of all asset movements</p>', unsafe_allow_html=True)
    
    # Filters
    with st.expander("🔍 Filters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            date_from = st.date_input("Date From")
        with col2:
            date_to = st.date_input("Date To")
        
        user_filter = st.text_input("User", placeholder="Filter by user...")
    
    # Get movements
    movements = db.get_all('AssetMovements')
    
    # Filter
    if date_from:
        movements = [m for m in movements if m.get('Movement Date', '') >= date_from.strftime('%Y-%m-%d')]
    if date_to:
        movements = [m for m in movements if m.get('Movement Date', '') <= date_to.strftime('%Y-%m-%d')]
    if user_filter:
        movements = [m for m in movements if user_filter.lower() in m.get('Moved By', '').lower()]
    
    # Summary
    st.metric("Total Movements", len(movements))
    
    # Display table
    if movements:
        df = pd.DataFrame(movements)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📥 Export to Excel"):
            excel_buffer = create_excel_export(movements)
            st.download_button(
                label="Download Excel File",
                data=excel_buffer,
                file_name=f"movement_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No movements found matching the filters.")

def create_excel_export(movements):
    """Create Excel export"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Movement Report"
    
    if movements:
        headers = list(movements[0].keys())
        ws.append(headers)
        
        for movement in movements:
            row = [movement.get(header, '') for header in headers]
            ws.append(row)
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

