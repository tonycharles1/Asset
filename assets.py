"""Assets page for Streamlit"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os

def show(db, role):
    """Display assets page"""
    st.markdown('<h1 class="main-header">Assets</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage and track all your assets</p>', unsafe_allow_html=True)
    
    # Add Asset button
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search by Asset Code or Item Name", placeholder="Type to search...")
    with col2:
        if st.button("➕ Add Asset", use_container_width=True):
            st.session_state.show_add_asset = True
    
    # Get assets
    assets = db.get_all('Assets')
    
    # Filter assets
    if search_term:
        assets = [a for a in assets if search_term.lower() in a.get('Asset Code', '').lower() or 
                 search_term.lower() in a.get('Item Name', '').lower()]
    
    # Show add asset form
    if st.session_state.get('show_add_asset', False):
        with st.expander("➕ Add New Asset", expanded=True):
            add_asset_form(db)
    
    # Display assets table
    if assets:
        df = pd.DataFrame(assets)
        # Select relevant columns for display
        display_cols = ['Asset Code', 'Item Name', 'Asset Category', 'Location', 'Amount', 'Asset Status']
        available_cols = [col for col in display_cols if col in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
        
        # Action buttons for each asset
        st.markdown("### Asset Actions")
        for asset in assets:
            with st.expander(f"🔧 {asset.get('Asset Code', '')} - {asset.get('Item Name', '')}"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{asset.get('Asset Code')}"):
                        st.session_state[f"edit_{asset.get('Asset Code')}"] = True
                with col2:
                    if role == 'admin':
                        if st.button(f"🗑️ Delete", key=f"delete_{asset.get('Asset Code')}"):
                            if db.delete('Assets', 'Asset Code', asset.get('Asset Code')):
                                st.success("Asset deleted successfully")
                                st.rerun()
    else:
        st.info("No assets found. Click 'Add Asset' to create your first asset.")

def add_asset_form(db):
    """Add asset form"""
    with st.form("add_asset_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            item_name = st.text_input("Item Name *", required=True)
            categories = db.get_all('Categories')
            category_names = [c.get('Category Name', '') for c in categories]
            asset_category = st.selectbox("Asset Category *", [""] + category_names, required=True)
            subcategories = db.get_all('Subcategories')
            subcategory_names = [s.get('Subcategory Name', '') for s in subcategories]
            asset_subcategory = st.selectbox("Asset Subcategory", [""] + subcategory_names)
            brands = db.get_all('Brands')
            brand_names = [b.get('Brand Name', '') for b in brands]
            brand = st.selectbox("Brand", [""] + brand_names)
            asset_description = st.text_area("Asset Description")
        
        with col2:
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            locations = db.get_all('Locations')
            location_names = [l.get('Location Name', '') for l in locations]
            location = st.selectbox("Location", [""] + location_names)
            date_of_purchase = st.date_input("Date of Purchase")
            warranty = st.text_input("Warranty")
            department = st.text_input("Department")
            ownership = st.text_input("Ownership")
            status_options = ["", "Active", "Inactive", "Under Maintenance", "Disposed", "Sold", "Lost"]
            asset_status = st.selectbox("Asset Status", status_options)
        
        col1, col2 = st.columns(2)
        with col1:
            image_file = st.file_uploader("Image Attachment", type=['png', 'jpg', 'jpeg', 'gif', 'webp'])
        with col2:
            document_file = st.file_uploader("Document Attachment", type=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'])
        
        submitted = st.form_submit_button("💾 Save Asset", use_container_width=True)
        
        if submitted:
            if item_name and asset_category:
                # Generate asset code
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                asset_code = f"AST-{timestamp}"
                
                # Handle file uploads (note: Streamlit file uploads need special handling)
                # For now, we'll store file metadata - actual file storage would need cloud storage
                image_filename = ''
                if image_file:
                    image_filename = f"{asset_code}_{image_file.name}"
                
                document_filename = ''
                if document_file:
                    document_filename = f"{asset_code}_{document_file.name}"
                
                asset_data = {
                    'Asset Code': asset_code,
                    'Item Name': item_name,
                    'Asset Category': asset_category,
                    'Asset SubCategory': asset_subcategory or '',
                    'Brand': brand or '',
                    'Asset Description': asset_description or '',
                    'Amount': str(amount) if amount else '',
                    'Location': location or '',
                    'Date of Purchase': date_of_purchase.strftime('%Y-%m-%d') if date_of_purchase else '',
                    'Warranty': warranty or '',
                    'Department': department or '',
                    'Ownership': ownership or '',
                    'Asset Status': asset_status or '',
                    'Image Attachment': image_filename,
                    'Document Attachment': document_filename
                }
                
                if db.insert('Assets', asset_data):
                    st.success("Asset added successfully!")
                    st.session_state.show_add_asset = False
                    st.rerun()
                else:
                    st.error("Failed to add asset")
            else:
                st.error("Please fill in required fields (Item Name and Category)")

