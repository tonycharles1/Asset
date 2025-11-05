"""Subcategories page for Streamlit"""
import streamlit as st
import pandas as pd

def show(db, role):
    """Display subcategories page"""
    st.markdown('<h1 class="main-header">Subcategories</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage asset subcategories</p>', unsafe_allow_html=True)
    
    # Add subcategory form
    with st.expander("➕ Add New Subcategory", expanded=False):
        with st.form("add_subcategory_form"):
            categories = db.get_all('Categories')
            category_options = {c.get('Category Name', ''): c.get('ID', '') for c in categories}
            
            subcategory_name = st.text_input("Subcategory Name *", required=True)
            category_name = st.selectbox("Category *", [""] + list(category_options.keys()), required=True)
            
            submitted = st.form_submit_button("💾 Add Subcategory", use_container_width=True)
            
            if submitted:
                if subcategory_name and category_name:
                    subcategory_id = db.get_next_id('Subcategories')
                    category_id = category_options.get(category_name, '')
                    if db.insert('Subcategories', {
                        'ID': subcategory_id,
                        'Subcategory Name': subcategory_name,
                        'Category ID': category_id
                    }):
                        st.success("Subcategory added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add subcategory")
                else:
                    st.error("Please fill in all required fields")
    
    # Display subcategories
    subcategories = db.get_all('Subcategories')
    
    if subcategories:
        df = pd.DataFrame(subcategories)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Delete option for admin
        if role == 'admin':
            st.markdown("### Delete Subcategories")
            for subcat in subcategories:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{subcat.get('Subcategory Name', '')}**")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_subcat_{subcat.get('ID')}"):
                        if db.delete('Subcategories', 'ID', subcat.get('ID')):
                            st.success(f"Subcategory '{subcat.get('Subcategory Name')}' deleted")
                            st.rerun()
    else:
        st.info("No subcategories found. Add your first subcategory above.")

