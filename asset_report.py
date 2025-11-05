"""Asset Report page for Streamlit"""
import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime

def show(db, role):
    """Display asset report page"""
    st.markdown('<h1 class="main-header">Asset Report</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Detailed report of all assets</p>', unsafe_allow_html=True)
    
    # Filters
    with st.expander("🔍 Filters", expanded=False):
        categories = db.get_all('Categories')
        locations = db.get_all('Locations')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Category", [""] + [c.get('Category Name', '') for c in categories])
        with col2:
            location_filter = st.selectbox("Location", [""] + [l.get('Location Name', '') for l in locations])
        with col3:
            status_filter = st.selectbox("Status", ["", "Active", "Inactive", "Under Maintenance", "Disposed"])
        
        search = st.text_input("Search", placeholder="Search by Asset Code or Item Name...")
    
    # Get and filter assets
    assets = db.get_all('Assets')
    
    if category_filter:
        assets = [a for a in assets if a.get('Asset Category') == category_filter]
    if location_filter:
        assets = [a for a in assets if a.get('Location') == location_filter]
    if status_filter:
        assets = [a for a in assets if a.get('Asset Status') == status_filter]
    if search:
        search_lower = search.lower()
        assets = [a for a in assets if search_lower in a.get('Asset Code', '').lower() or 
                 search_lower in a.get('Item Name', '').lower()]
    
    # Summary
    st.metric("Total Assets", len(assets))
    
    # Display table
    if assets:
        df = pd.DataFrame(assets)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📥 Export to Excel"):
            excel_buffer = create_excel_export(assets)
            st.download_button(
                label="Download Excel File",
                data=excel_buffer,
                file_name=f"asset_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No assets found matching the filters.")

def create_excel_export(assets):
    """Create Excel export"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Asset Report"
    
    if assets:
        headers = list(assets[0].keys())
        ws.append(headers)
        
        for asset in assets:
            row = [asset.get(header, '') for header in headers]
            ws.append(row)
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

