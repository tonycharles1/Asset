"""Categories page for Streamlit"""
import streamlit as st
import pandas as pd

def show(db, role):
    """Display categories page"""
    st.markdown('<h1 class="main-header">Categories</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage asset categories</p>', unsafe_allow_html=True)
    
    # Add category form
    with st.expander("➕ Add New Category", expanded=False):
        with st.form("add_category_form"):
            category_name = st.text_input("Category Name *", required=True)
            submitted = st.form_submit_button("💾 Add Category", use_container_width=True)
            
            if submitted:
                if category_name:
                    category_id = db.get_next_id('Categories')
                    if db.insert('Categories', {'ID': category_id, 'Category Name': category_name}):
                        st.success("Category added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add category")
                else:
                    st.error("Please enter a category name")
    
    # Display categories
    categories = db.get_all('Categories')
    
    if categories:
        df = pd.DataFrame(categories)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Delete option for admin
        if role == 'admin':
            st.markdown("### Delete Categories")
            for category in categories:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{category.get('Category Name', '')}**")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_cat_{category.get('ID')}"):
                        if db.delete('Categories', 'ID', category.get('ID')):
                            st.success(f"Category '{category.get('Category Name')}' deleted")
                            st.rerun()
    else:
        st.info("No categories found. Add your first category above.")

