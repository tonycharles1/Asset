"""Depreciation page for Streamlit"""
import streamlit as st
import pandas as pd
from datetime import datetime

def show(db, role):
    """Display depreciation page"""
    st.markdown('<h1 class="main-header">Depreciation Report</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">View asset depreciation calculations and current values</p>', unsafe_allow_html=True)
    
    # Get data
    assets = db.get_all('Assets')
    asset_types = db.get_all('AssetTypes')
    
    # Create lookup for depreciation
    dep_lookup = {}
    for at in asset_types:
        dep_lookup[at.get('Asset Type', '')] = float(at.get('Depreciation Value (%)', 0) or 0)
    
    # Calculate depreciation
    today = datetime.now().date()
    processed_assets = []
    
    for asset in assets:
        # Get purchase amount
        try:
            purchase_amount = float(asset.get('Amount', 0) or 0)
        except:
            purchase_amount = 0
        
        # Get purchase date
        purchase_date_str = asset.get('Date of Purchase', '')
        age_years = 0
        if purchase_date_str:
            try:
                purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()
                delta = today - purchase_date
                age_years = delta.days / 365.25
                if age_years < 0:
                    age_years = 0
            except:
                pass
        
        # Get depreciation %
        asset_category = asset.get('Asset Category', '')
        depreciation_percent = dep_lookup.get(asset_category, 0)
        
        # Calculate
        annual_dep = 0
        total_dep = 0
        current_value = purchase_amount
        
        if purchase_amount > 0 and depreciation_percent > 0 and age_years > 0:
            annual_dep = purchase_amount * (depreciation_percent / 100)
            total_dep = annual_dep * age_years
            current_value = max(0, purchase_amount - total_dep)
        
        asset['Purchase Amount'] = purchase_amount
        asset['Age (Years)'] = round(age_years, 2)
        asset['Depreciation %'] = depreciation_percent
        asset['Annual Depreciation'] = round(annual_dep, 2)
        asset['Total Depreciation'] = round(total_dep, 2)
        asset['Current Value'] = round(current_value, 2)
        
        processed_assets.append(asset)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Assets", len(processed_assets))
    with col2:
        total_purchase = sum(a.get('Purchase Amount', 0) for a in processed_assets)
        st.metric("Total Purchase Value", f"${total_purchase:,.2f}")
    with col3:
        total_dep = sum(a.get('Total Depreciation', 0) for a in processed_assets)
        st.metric("Total Depreciation", f"${total_dep:,.2f}")
    with col4:
        total_current = sum(a.get('Current Value', 0) for a in processed_assets)
        st.metric("Current Book Value", f"${total_current:,.2f}")
    
    # Display table
    if processed_assets:
        display_cols = ['Asset Code', 'Item Name', 'Asset Category', 'Location', 
                       'Purchase Amount', 'Age (Years)', 'Depreciation %', 
                       'Annual Depreciation', 'Total Depreciation', 'Current Value']
        df = pd.DataFrame(processed_assets)
        available_cols = [col for col in display_cols if col in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📥 Export to Excel"):
            excel_buffer = create_excel_export(processed_assets)
            st.download_button(
                label="Download Excel File",
                data=excel_buffer,
                file_name=f"depreciation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No assets found for depreciation calculation.")

def create_excel_export(assets):
    """Create Excel export"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Depreciation Report"
    
    headers = ['Asset Code', 'Item Name', 'Category', 'Location', 'Purchase Date',
               'Age (Years)', 'Purchase Amount', 'Depreciation %', 'Annual Depreciation',
               'Total Depreciation', 'Current Book Value', 'Status']
    ws.append(headers)
    
    for asset in assets:
        row = [
            asset.get('Asset Code', ''),
            asset.get('Item Name', ''),
            asset.get('Asset Category', ''),
            asset.get('Location', ''),
            asset.get('Date of Purchase', ''),
            asset.get('Age (Years)', ''),
            asset.get('Purchase Amount', ''),
            asset.get('Depreciation %', ''),
            asset.get('Annual Depreciation', ''),
            asset.get('Total Depreciation', ''),
            asset.get('Current Value', ''),
            asset.get('Asset Status', '')
        ]
        ws.append(row)
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

