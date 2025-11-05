# 📋 Forms Available in Asset Management System

All forms are ready and accessible! Here's a complete guide to all available forms:

## 🔐 Authentication Forms

### 1. Register Form
- **URL**: http://localhost:5000/register
- **Purpose**: Create a new user account
- **Fields**: Username, Email, Password, Role
- **Note**: First user automatically becomes admin

### 2. Login Form
- **URL**: http://localhost:5000/login
- **Purpose**: User authentication
- **Fields**: Username, Password

---

## 📍 Master Data Forms

### 3. Locations Form
- **URL**: http://localhost:5000/locations
- **Purpose**: Manage asset locations
- **Fields**: 
  - Location Name (text input)
- **Features**: 
  - Add new locations
  - View all locations
  - Delete (Admin only)

### 4. Categories Form
- **URL**: http://localhost:5000/categories
- **Purpose**: Manage asset categories
- **Fields**: 
  - Category Name (text input)
- **Features**: 
  - Add new categories
  - View all categories
  - Delete (Admin only)

### 5. Subcategories Form
- **URL**: http://localhost:5000/subcategories
- **Purpose**: Manage asset subcategories
- **Fields**: 
  - Category (dropdown - select from existing categories)
  - Subcategory Name (text input)
- **Features**: 
  - Add new subcategories linked to categories
  - View all subcategories with category names
  - Delete (Admin only)

### 6. Asset Types Form
- **URL**: http://localhost:5000/asset_types
- **Purpose**: Manage asset types with depreciation
- **Fields**: 
  - Asset Code (text input)
  - Asset Type (text input)
  - Depreciation Value (%) (number input)
- **Features**: 
  - Add new asset types
  - View all asset types
  - Delete (Admin only)

### 7. Brands Form
- **URL**: http://localhost:5000/brands
- **Purpose**: Manage asset brands
- **Fields**: 
  - Brand Name (text input)
- **Features**: 
  - Add new brands
  - View all brands
  - Delete (Admin only)

---

## 🏢 Asset Management Forms

### 8. Assets List & Add Form
- **URL**: http://localhost:5000/assets
- **Purpose**: View and manage all assets
- **Add Asset URL**: http://localhost:5000/assets/add
- **Fields**:
  - Item Name * (required)
  - Asset Category * (dropdown)
  - Asset Subcategory (dropdown)
  - Brand (dropdown)
  - Asset Description (textarea)
  - Amount (number)
  - Location (dropdown)
  - Date of Purchase (date picker)
  - Warranty (text)
  - Department (text)
  - Ownership (text)
- **Features**:
  - Auto-generated Asset Code (primary key)
  - Edit existing assets
  - Delete assets (Admin only)
  - Bulk select for barcode printing
  - Responsive table view

### 9. Edit Asset Form
- **URL**: http://localhost:5000/assets/edit/<asset_code>
- **Purpose**: Modify existing asset details
- **Fields**: Same as Add Asset form
- **Features**: Pre-filled with existing data

---

## 🔄 Asset Movement Forms

### 10. Asset Movements List
- **URL**: http://localhost:5000/asset_movements
- **Purpose**: View asset movement history
- **Features**: 
  - View all movements
  - Track location changes
  - See who moved assets and when

### 11. Add Asset Movement Form
- **URL**: http://localhost:5000/asset_movements/add
- **Purpose**: Record asset movement between locations
- **Fields**:
  - Asset Code * (dropdown - select asset)
  - From Location * (dropdown)
  - To Location * (dropdown)
  - Notes (textarea)
- **Features**:
  - Automatically updates asset location
  - Records movement date and user
  - Maintains complete history

---

## 🏷️ Barcode Printing

### 12. Barcode Print Feature
- **Location**: Assets page → Select assets → Print Barcodes button
- **Purpose**: Generate PDF with barcodes for selected assets
- **Features**:
  - Select multiple assets via checkboxes
  - Generate PDF with barcodes
  - Includes asset information

---

## 📱 Responsive Design

All forms are fully responsive and work on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Mobile phones

---

## 🎯 Recommended Setup Order

To set up your system properly, create master data in this order:

1. **Locations** - Add all locations where assets can be stored
2. **Categories** - Add main asset categories
3. **Subcategories** - Add subcategories linked to categories
4. **Asset Types** - Add asset types with depreciation values
5. **Brands** - Add all asset brands
6. **Assets** - Start adding your assets!

---

## 🚀 Quick Start

1. Make sure the application is running: `python app.py`
2. Open: http://localhost:5000
3. Register/Login
4. Navigate to each form using the sidebar menu
5. Start adding your data!

---

## 💡 Tips

- Use the sidebar navigation to quickly access all forms
- All forms have validation and error messages
- Admin users can delete records, regular users can only edit
- Asset Codes are auto-generated when you add assets
- The dashboard shows a summary of your assets

---

**All forms are ready to use! Just start the application and begin creating your data!** 🎉


