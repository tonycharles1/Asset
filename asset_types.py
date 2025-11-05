"""Asset Types page for Streamlit"""
import streamlit as st
import pandas as pd

def show(db, role):
    """Display asset types page"""
    st.markdown('<h1 class="main-header">Asset Types</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage asset types and depreciation values</p>', unsafe_allow_html=True)
    
    # Add asset type form
    with st.expander("➕ Add New Asset Type", expanded=False):
        with st.form("add_asset_type_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                asset_code = st.text_input("Asset Code *", required=True)
            with col2:
                asset_type = st.text_input("Asset Type *", required=True)
            with col3:
                depreciation_value = st.number_input("Depreciation Value (%) *", min_value=0.0, max_value=100.0, step=0.01, required=True)
            
            submitted = st.form_submit_button("💾 Add Asset Type", use_container_width=True)
            
            if submitted:
                if asset_code and asset_type and depreciation_value:
                    if db.insert('AssetTypes', {
                        'Asset Code': asset_code,
                        'Asset Type': asset_type,
                        'Depreciation Value (%)': str(depreciation_value)
                    }):
                        st.success("Asset Type added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add asset type")
                else:
                    st.error("Please fill in all required fields")
    
    # Display asset types
    asset_types = db.get_all('AssetTypes')
    
    if asset_types:
        df = pd.DataFrame(asset_types)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Delete option for admin
        if role == 'admin':
            st.markdown("### Delete Asset Types")
            for at in asset_types:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{at.get('Asset Code', '')}** - {at.get('Asset Type', '')} ({at.get('Depreciation Value (%)', '')}%)")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_at_{at.get('Asset Code')}"):
                        if db.delete('AssetTypes', 'Asset Code', at.get('Asset Code')):
                            st.success(f"Asset Type '{at.get('Asset Code')}' deleted")
                            st.rerun()
    else:
        st.info("No asset types found. Add your first asset type above.")

