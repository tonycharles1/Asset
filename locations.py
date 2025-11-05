"""Locations page for Streamlit"""
import streamlit as st
import pandas as pd

def show(db, role):
    """Display locations page"""
    st.markdown('<h1 class="main-header">Locations</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage asset locations</p>', unsafe_allow_html=True)
    
    # Add location form
    with st.expander("➕ Add New Location", expanded=False):
        with st.form("add_location_form"):
            location_name = st.text_input("Location Name *", required=True)
            submitted = st.form_submit_button("💾 Add Location", use_container_width=True)
            
            if submitted:
                if location_name:
                    location_id = db.get_next_id('Locations')
                    if db.insert('Locations', {'ID': location_id, 'Location Name': location_name}):
                        st.success("Location added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add location")
                else:
                    st.error("Please enter a location name")
    
    # Display locations
    locations = db.get_all('Locations')
    
    if locations:
        df = pd.DataFrame(locations)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Delete option for admin
        if role == 'admin':
            st.markdown("### Delete Locations")
            for location in locations:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{location.get('Location Name', '')}**")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_loc_{location.get('ID')}"):
                        if db.delete('Locations', 'ID', location.get('ID')):
                            st.success(f"Location '{location.get('Location Name')}' deleted")
                            st.rerun()
    else:
        st.info("No locations found. Add your first location above.")

