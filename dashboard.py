"""Dashboard page for Streamlit"""
import streamlit as st
import pandas as pd
from datetime import datetime

def show(db, role):
    """Display dashboard page"""
    st.markdown('<h1 class="main-header">Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Overview of your asset management system</p>', unsafe_allow_html=True)
    
    # Get assets
    assets = db.get_all('Assets')
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Assets", len(assets))
    
    with col2:
        total_value = sum(float(a.get('Amount', 0) or 0) for a in assets)
        st.metric("Total Asset Value", f"${total_value:,.2f}")
    
    with col3:
        st.metric("Categories", len(db.get_all('Categories')))
    
    with col4:
        st.metric("Locations", len(db.get_all('Locations')))
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Assets by Category")
        category_data = {}
        for asset in assets:
            category = asset.get('Asset Category', 'Uncategorized')
            category_data[category] = category_data.get(category, 0) + 1
        
        if category_data:
            df_cat = pd.DataFrame(list(category_data.items()), columns=['Category', 'Count'])
            st.bar_chart(df_cat.set_index('Category'))
    
    with col2:
        st.subheader("Assets by Location")
        location_data = {}
        for asset in assets:
            location = asset.get('Location', 'No Location')
            location_data[location] = location_data.get(location, 0) + 1
        
        if location_data:
            df_loc = pd.DataFrame(list(location_data.items()), columns=['Location', 'Count'])
            st.bar_chart(df_loc.set_index('Location'))
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Assets by Status")
        status_data = {}
        for asset in assets:
            status = asset.get('Asset Status', 'No Status')
            status_data[status] = status_data.get(status, 0) + 1
        
        if status_data:
            df_status = pd.DataFrame(list(status_data.items()), columns=['Status', 'Count'])
            st.bar_chart(df_status.set_index('Status'))
    
    with col2:
        st.subheader("Top Brands")
        brand_data = {}
        for asset in assets:
            brand = asset.get('Brand', 'No Brand')
            brand_data[brand] = brand_data.get(brand, 0) + 1
        
        top_brands = sorted(brand_data.items(), key=lambda x: x[1], reverse=True)[:10]
        if top_brands:
            df_brand = pd.DataFrame(top_brands, columns=['Brand', 'Count'])
            st.bar_chart(df_brand.set_index('Brand'))

