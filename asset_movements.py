"""Asset Movements page for Streamlit"""
import streamlit as st
import pandas as pd
from datetime import datetime

def show(db, role):
    """Display asset movements page"""
    st.markdown('<h1 class="main-header">Asset Movements</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Track asset movements between locations</p>', unsafe_allow_html=True)
    
    # Add movement form
    with st.expander("➕ Record Asset Movement", expanded=False):
        with st.form("add_movement_form"):
            assets = db.get_all('Assets')
            asset_options = {a.get('Asset Code', ''): a.get('Item Name', '') for a in assets}
            locations = db.get_all('Locations')
            location_names = [l.get('Location Name', '') for l in locations]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                asset_code = st.selectbox("Asset Code *", [""] + list(asset_options.keys()), required=True)
            with col2:
                from_location = st.selectbox("From Location *", [""] + location_names, required=True)
            with col3:
                to_location = st.selectbox("To Location *", [""] + location_names, required=True)
            
            notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("💾 Record Movement", use_container_width=True)
            
            if submitted:
                if asset_code and from_location and to_location:
                    movement_id = db.get_next_id('AssetMovements')
                    movement_data = {
                        'ID': movement_id,
                        'Asset Code': asset_code,
                        'From Location': from_location,
                        'To Location': to_location,
                        'Movement Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Moved By': st.session_state.user_id,
                        'Notes': notes or ''
                    }
                    
                    if db.insert('AssetMovements', movement_data):
                        # Update asset location
                        db.update('Assets', 'Asset Code', asset_code, {'Location': to_location})
                        st.success("Asset movement recorded successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to record movement")
                else:
                    st.error("Please fill in all required fields")
    
    # Display movements
    movements = db.get_all('AssetMovements')
    
    if movements:
        df = pd.DataFrame(movements)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No asset movements recorded yet.")

