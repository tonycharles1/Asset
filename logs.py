"""Activity Logs page for Streamlit"""
import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime

def show(db, role):
    """Display activity logs page"""
    st.markdown('<h1 class="main-header">Activity Logs</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">System activity and audit trail</p>', unsafe_allow_html=True)
    
    # Get logs
    logs = []
    
    # Get activity logs
    try:
        activity_logs = db.get_all('ActivityLogs')
        for log_entry in activity_logs:
            logs.append({
                'Date & Time': log_entry.get('Date & Time', ''),
                'Type': log_entry.get('Type', 'Activity'),
                'User': log_entry.get('User', ''),
                'Action': log_entry.get('Action', ''),
                'Description': log_entry.get('Description', ''),
                'Details': log_entry.get('Details', '')
            })
    except:
        pass
    
    # Get movements as logs
    movements = db.get_all('AssetMovements')
    for movement in movements:
        logs.append({
            'Date & Time': movement.get('Movement Date', ''),
            'Type': 'Movement',
            'User': movement.get('Moved By', ''),
            'Action': 'Move',
            'Description': f"Asset {movement.get('Asset Code', '')} moved from {movement.get('From Location', '')} to {movement.get('To Location', '')}",
            'Details': movement.get('Notes', '')
        })
    
    # Sort by date
    logs.sort(key=lambda x: x.get('Date & Time', ''), reverse=True)
    
    # Filters
    with st.expander("🔍 Filters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            log_types = list(set([log.get('Type', '') for log in logs]))
            type_filter = st.selectbox("Type", [""] + log_types)
        with col2:
            users = list(set([log.get('User', '') for log in logs if log.get('User')]))
            user_filter = st.selectbox("User", [""] + users)
        
        date_from = st.date_input("Date From")
        date_to = st.date_input("Date To")
    
    # Apply filters
    filtered_logs = logs.copy()
    if type_filter:
        filtered_logs = [l for l in filtered_logs if l.get('Type') == type_filter]
    if user_filter:
        filtered_logs = [l for l in filtered_logs if l.get('User') == user_filter]
    if date_from:
        filtered_logs = [l for l in filtered_logs if l.get('Date & Time', '') >= date_from.strftime('%Y-%m-%d')]
    if date_to:
        filtered_logs = [l for l in filtered_logs if l.get('Date & Time', '') <= date_to.strftime('%Y-%m-%d')]
    
    # Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Logs", len(filtered_logs))
    with col2:
        unique_users = len(set([l.get('User', '') for l in filtered_logs if l.get('User')]))
        st.metric("Active Users", unique_users)
    with col3:
        movements_count = len([l for l in filtered_logs if l.get('Type') == 'Movement'])
        st.metric("Movements", movements_count)
    
    # Display table
    if filtered_logs:
        df = pd.DataFrame(filtered_logs)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📥 Export to Excel"):
            excel_buffer = create_excel_export(filtered_logs)
            st.download_button(
                label="Download Excel File",
                data=excel_buffer,
                file_name=f"activity_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No log entries found.")

def create_excel_export(logs):
    """Create Excel export"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Activity Logs"
    
    if logs:
        headers = list(logs[0].keys())
        ws.append(headers)
        
        for log in logs:
            row = [log.get(header, '') for header in headers]
            ws.append(row)
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

