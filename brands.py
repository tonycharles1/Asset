"""Brands page for Streamlit"""
import streamlit as st
import pandas as pd

def show(db, role):
    """Display brands page"""
    st.markdown('<h1 class="main-header">Brands</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage asset brands</p>', unsafe_allow_html=True)
    
    # Add brand form
    with st.expander("➕ Add New Brand", expanded=False):
        with st.form("add_brand_form"):
            brand_name = st.text_input("Brand Name *", required=True)
            submitted = st.form_submit_button("💾 Add Brand", use_container_width=True)
            
            if submitted:
                if brand_name:
                    brand_id = db.get_next_id('Brands')
                    if db.insert('Brands', {'ID': brand_id, 'Brand Name': brand_name}):
                        st.success("Brand added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add brand")
                else:
                    st.error("Please enter a brand name")
    
    # Display brands
    brands = db.get_all('Brands')
    
    if brands:
        df = pd.DataFrame(brands)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Delete option for admin
        if role == 'admin':
            st.markdown("### Delete Brands")
            for brand in brands:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{brand.get('Brand Name', '')}**")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_brand_{brand.get('ID')}"):
                        if db.delete('Brands', 'ID', brand.get('ID')):
                            st.success(f"Brand '{brand.get('Brand Name')}' deleted")
                            st.rerun()
    else:
        st.info("No brands found. Add your first brand above.")

