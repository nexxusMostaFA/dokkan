import streamlit as st
import pandas as pd
from collections import defaultdict
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Product Inventory Management",
    layout="wide"
)

# Custom CSS to ensure buttons are visible in dark mode and enlarge product name and price
st.markdown("""
<style>
    /* Make buttons more visible in dark mode */
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 15px !important;
        font-size: 16px !important;
    }
    .stButton>button:hover {
        background-color: #45a049 !important;
    }
    
    /* Delete button styling */
    .delete-button>button {
        background-color: #ff4d4d !important;
        color: white !important;
    }
    .delete-button>button:hover {
        background-color: #cc0000 !important;
    }
    
    /* Larger font for product name and price */
    .product-name {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    .product-price {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #ff9900 !important;
    }
    
    /* Styling for quantity display */
    .quantity-display {
        font-size: 20px !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    /* Styling for barcode display */
    .barcode {
        font-family: monospace !important;
        font-size: 14px !important;
        color: #555 !important;
        background-color: #f0f0f0 !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        display: inline-block !important;
    }

    /* Styling for tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f0f0;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    
    /* Confirmation dialog styling */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
    }
    .dialog {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        z-index: 1001;
        width: 400px;
    }
</style>
""", unsafe_allow_html=True)

# File paths for data persistence
DATA_PATH = "inventory_data.json"
CART_PATH = "cart_data.json"

# Function to load data from file
def load_data():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return create_default_data()
    else:
        return create_default_data()

# Function to create default data
def create_default_data():
    # Define the original product data
    original_products_data = [
        {"Part Number": "06008A7E01", "Product Name": "Easy Aquatak 100 Long Lance", "Description": "ماكينة غسيل ضغط عالي 100 بار - 1200 وات - طول الخرطوم 3 متر", "Country": "China", "Price (EGP)": 3662.22, "Barcode": 4059952539447},
        {"Part Number": "06008A7F00", "Product Name": "Easy Aquatak 110", "Description": "ماكينة غسيل ضغط عالي 110 بار - 1300 وات - طول الخرطوم 3 متر", "Country": "China", "Price (EGP)": 4185.00, "Barcode": 3165140935685},
        {"Part Number": "06008A7A00", "Product Name": "Universal Aquatak 125", "Description": "ماكينة غسيل ضغط عالي 125 بار - 1500 وات - طول الخرطوم 5 متر", "Country": "China", "Price (EGP)": 5607.00, "Barcode": 3165140883610},
        {"Part Number": "06008A7C00", "Product Name": "Universal Aquatak 135", "Description": "ماكينة غسيل ضغط عالي 135 بار - 1900 وات - طول الخرطوم 7 متر", "Country": "China", "Price (EGP)": 7277.49, "Barcode": 3165140883795},
        {"Part Number": "06008A7D00", "Product Name": "Advanced Aquatak 140", "Description": "ماكينة غسيل ضغط عالي 140 بار - 2100 وات - طول الخرطوم 8 متر", "Country": "China", "Price (EGP)": 11513.82, "Barcode": 3165140906470},
        {"Part Number": "0600910600", "Product Name": "GHP 5-65X PROFESSIONAL", "Description": "Rated input power 2400 W - Max. pressure 160 bar - Hose length 10m", "Country": "China", "Price (EGP)": 33723.65, "Barcode": 3165140810173},
        {"Part Number": "0600910800", "Product Name": "GHP 5-75X PROFESSIONAL", "Description": "Rated input power 2600 W - Max. pressure 185 bar - Hose length 10m", "Country": "China", "Price (EGP)": 39674.88, "Barcode": 3165140810272},
        {"Part Number": "0600910300", "Product Name": "GHP 8-15 XD PROFESSIONAL", "Description": "Rated input power 4000 W - Max. pressure 150 bar - Hose length 15m", "Country": "China", "Price (EGP)": 63479.81, "Barcode": 3165140716826},
        {"Part Number": "F016800572", "Product Name": "Car Cleaning Kit", "Description": "طقم تنظيف السيارات لتنظيف السيارة من جميع الأتربة وتوافق مع الموديلات الآتية", "Country": "China", "Price (EGP)": 1253.49, "Barcode": 3165140941785},
        # Add more products as needed
        {"Part Number": "00007200", "Product Name": "Bosch GlassVAC Cordless Window Vacuum", "Description": "هذه النافذة اللاسلكية تقوم بتنظيف النوافذ بكفاءة عالية بفضل خبرة بوش في هذا المجال.", "Country": "China", "Price (EGP)": 2775, "Barcode": 3165140976374},
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(original_products_data)
    
    # Save the default data to file
    save_data(df)
    
    return df

# Function to save data to file
def save_data(df):
    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(df.to_dict('records'), f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Function to load cart data
def load_cart():
    if os.path.exists(CART_PATH):
        try:
            with open(CART_PATH, 'r') as f:
                cart_data = json.load(f)
                # Convert keys back to the format used by the app
                quantities = defaultdict(int)
                for key, value in cart_data.items():
                    quantities[key] = value
                return quantities
        except Exception as e:
            st.error(f"Error loading cart: {e}")
            return defaultdict(int)
    else:
        return defaultdict(int)

# Function to save cart data
def save_cart(quantities):
    try:
        with open(CART_PATH, 'w') as f:
            json.dump(dict(quantities), f)
        return True
    except Exception as e:
        st.error(f"Error saving cart: {e}")
        return False

# Function to calculate cart total
def calculate_cart_total():
    total = 0.0
    for key, qty in st.session_state.quantities.items():
        if qty > 0:
            # Split the key back into part_number and product_name
            part_number, product_name = key.split('_', 1)
            
            # Find the product in the DataFrame that matches both part number and product name
            product_mask = (st.session_state.products_df['Part Number'] == part_number) & \
                          (st.session_state.products_df['Product Name'] == product_name)
            
            if not product_mask.empty and any(product_mask):
                product_price = st.session_state.products_df.loc[product_mask, 'Price (EGP)'].values[0]
                total += product_price * qty
    
    st.session_state.cart_total = total

# Initialize session state for the product database if not already set
if 'products_df' not in st.session_state:
    st.session_state.products_df = load_data()

# Initialize session state for quantities if not already set
if 'quantities' not in st.session_state:
    st.session_state.quantities = load_cart()
    
if 'cart_total' not in st.session_state:
    st.session_state.cart_total = 0.0
    calculate_cart_total()

# Initialize form input variables with proper types
if 'new_part_number' not in st.session_state:
    st.session_state.new_part_number = ""
if 'new_product_name' not in st.session_state:
    st.session_state.new_product_name = ""
if 'new_description' not in st.session_state:
    st.session_state.new_description = ""
if 'new_country' not in st.session_state:
    st.session_state.new_country = ""
if 'new_price' not in st.session_state:
    st.session_state.new_price = 0.0
if 'new_barcode' not in st.session_state:
    st.session_state.new_barcode = ""
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'show_delete_confirm' not in st.session_state:
    st.session_state.show_delete_confirm = False
if 'delete_product_key' not in st.session_state:
    st.session_state.delete_product_key = None
if 'delete_success' not in st.session_state:
    st.session_state.delete_success = False

# Function to update quantity
def update_quantity(part_number, product_name, change):
    key = f"{part_number}_{product_name}"  # Use combined key for products with duplicate part numbers
    current_qty = st.session_state.quantities[key]
    new_qty = max(0, current_qty + change)  # Ensure quantity doesn't go below 0
    st.session_state.quantities[key] = new_qty
    
    # Recalculate cart total
    calculate_cart_total()
    
    # Save cart data to file
    save_cart(st.session_state.quantities)

# Function to add a new product
def add_new_product():
    # Get values from form
    new_part_number = st.session_state.new_part_number
    new_product_name = st.session_state.new_product_name
    new_description = st.session_state.new_description
    new_country = st.session_state.new_country
    new_price = st.session_state.new_price
    new_barcode = st.session_state.new_barcode
    
    # Validate input
    if not new_product_name:
        st.error("Product Name is required")
        return
    
    if new_price <= 0:
        st.error("Price must be greater than 0")
        return
    
    # Create new product dictionary
    new_product = {
        "Part Number": new_part_number,
        "Product Name": new_product_name,
        "Description": new_description,
        "Country": new_country,
        "Price (EGP)": float(new_price),
        "Barcode": new_barcode
    }
    
    # Add the new product to the DataFrame
    st.session_state.products_df = pd.concat([st.session_state.products_df, pd.DataFrame([new_product])], ignore_index=True)
    
    # Save data to file
    save_data(st.session_state.products_df)
    
    # Clear the form inputs
    st.session_state.new_part_number = ""
    st.session_state.new_product_name = ""
    st.session_state.new_description = ""
    st.session_state.new_country = ""
    st.session_state.new_price = 0.0
    st.session_state.new_barcode = ""
    
    # Show success message
    st.session_state.show_success = True

# Function to show delete confirmation
def show_delete_confirmation(key):
    st.session_state.show_delete_confirm = True
    st.session_state.delete_product_key = key

# Function to cancel deletion
def cancel_delete():
    st.session_state.show_delete_confirm = False
    st.session_state.delete_product_key = None

# Function to delete product
def delete_product():
    key = st.session_state.delete_product_key
    if key:
        part_number, product_name = key.split('_', 1)
        
        # Find the product index
        product_mask = (st.session_state.products_df['Part Number'] == part_number) & \
                      (st.session_state.products_df['Product Name'] == product_name)
        
        if any(product_mask):
            # Drop the product from the DataFrame
            st.session_state.products_df = st.session_state.products_df[~product_mask].reset_index(drop=True)
            
            # Save data to file
            save_data(st.session_state.products_df)
            
            # Remove from cart if present
            if key in st.session_state.quantities:
                del st.session_state.quantities[key]
                save_cart(st.session_state.quantities)
                calculate_cart_total()
            
            # Set success flag
            st.session_state.delete_success = True
    
    # Reset confirmation state
    st.session_state.show_delete_confirm = False
    st.session_state.delete_product_key = None

# App header with styled title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Product Inventory Management</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>Total Products: {len(st.session_state.products_df)}</h3>", unsafe_allow_html=True)

# Display cart total with styling
st.markdown(f"<h2 style='text-align: center; color: #ff9900;'>Cart Total: {st.session_state.cart_total:.2f} EGP</h2>", unsafe_allow_html=True)

# Create tabs for different sections
tabs = st.tabs(["Product Catalog", "Add New Product", "Manage Inventory"])

# Product Catalog Tab
with tabs[0]:
    # Search functionality
    st.subheader("Search Products")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search term", "", key="search_input")
    with col2:
        search_type = st.radio("Search by:", ["Name/Description", "Barcode", "Part Number"], horizontal=True)

    # Filter products based on search
    if search_query:
        if search_type == "Barcode":
            filtered_df = st.session_state.products_df[st.session_state.products_df['Barcode'].astype(str).str.contains(search_query)]
        elif search_type == "Part Number":
            filtered_df = st.session_state.products_df[st.session_state.products_df['Part Number'].astype(str).str.contains(search_query, case=False)]
        else:
            filtered_df = st.session_state.products_df[
                st.session_state.products_df['Product Name'].str.contains(search_query, case=False) | 
                st.session_state.products_df['Description'].str.contains(search_query, case=False)
            ]
    else:
        filtered_df = st.session_state.products_df

    # Display products
    st.markdown("<h2 style='text-align: center;'>Product Catalog</h2>", unsafe_allow_html=True)

    # Create columns for the product listing with styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("<h3>Part Number & Info</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3>Product Details</h3>", unsafe_allow_html=True)
    with col3:
        st.markdown("<h3>Quantity</h3>", unsafe_allow_html=True)

    # Display each product with quantity controls and improved styling
    for _, row in filtered_df.iterrows():
        part_number = row['Part Number'] if not pd.isna(row['Part Number']) else ""
        product_name = row['Product Name']
        key = f"{part_number}_{product_name}"  # Create a unique key combining part number and product name
        
        barcode = row['Barcode']
        current_qty = st.session_state.quantities[key]
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"<div><strong>{part_number}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='product-price'>Price: {row['Price (EGP)']:.2f} EGP</div>", unsafe_allow_html=True)
            st.markdown(f"<div>Country: {row['Country']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='barcode'>Barcode: {barcode}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div class='product-name'>{product_name}</div>", unsafe_allow_html=True)
            st.write(row['Description'])
        
        with col3:
            col3_1, col3_2, col3_3 = st.columns(3)
            with col3_1:
                st.button("➖", key=f"dec_{key}", on_click=update_quantity, args=(part_number, product_name, -1))
            with col3_2:
                st.markdown(f"<div class='quantity-display'>{current_qty}</div>", unsafe_allow_html=True)
            with col3_3:
                st.button("➕", key=f"inc_{key}", on_click=update_quantity, args=(part_number, product_name, 1))
        
        # Add a subtotal for this product if quantity > 0
        if current_qty > 0:
            st.markdown(f"<div style='text-align: right; font-weight: bold;'>Subtotal: {current_qty * row['Price (EGP)']:.2f} EGP</div>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)

    # Display order summary with improved styling
    if sum(st.session_state.quantities.values()) > 0:
        st.markdown("<h2 style='text-align: center; margin-top: 30px;'>Order Summary</h2>", unsafe_allow_html=True)
        
        # Create columns for the order summary with headers
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns([3, 1, 1, 1])
        with summary_col1:
            st.markdown("<strong>Product</strong>", unsafe_allow_html=True)
        with summary_col2:
            st.markdown("<strong>Barcode</strong>", unsafe_allow_html=True)
        with summary_col3:
            st.markdown("<strong>Quantity</strong>", unsafe_allow_html=True)
        with summary_col4:
            st.markdown("<strong>Subtotal</strong>", unsafe_allow_html=True)
        
        # Display each order item
        for key, qty in st.session_state.quantities.items():
            if qty > 0:
                # Split the key back into part_number and product_name
                part_number, product_name = key.split('_', 1)
                
                # Find the product in the DataFrame that matches both part number and product name
                product_mask = (st.session_state.products_df['Part Number'] == part_number) & \
                               (st.session_state.products_df['Product Name'] == product_name)
                
                if not product_mask.empty and any(product_mask):
                    product = st.session_state.products_df[product_mask].iloc[0]
                    subtotal = qty * product['Price (EGP)']
                    
                    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns([3, 1, 1, 1])
                    with summary_col1:
                        st.write(f"{product['Product Name']}")
                    with summary_col2:
                        st.write(f"{product['Barcode']}")
                    with summary_col3:
                        st.write(f"{qty}")
                    with summary_col4:
                        st.write(f"{subtotal:.2f} EGP")
        
        st.markdown(
            f"<div style='display: flex; justify-content: space-between; margin-top: 20px; font-size: 22px;'>"
            f"<span style='font-weight: bold;'>TOTAL:</span>"
            f"<span style='font-weight: bold; color: #ff9900;'>{st.session_state.cart_total:.2f} EGP</span>"
            f"</div>", 
            unsafe_allow_html=True
        )
        
        # Order actions
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("💾 Save Order", key="save_order"):
                # Save cart data to file
                if save_cart(st.session_state.quantities):
                    st.success("Order saved successfully!")
        with col2:
            if st.button("🧾 Print Invoice", key="print_invoice"):
                st.info("Printing functionality would be implemented here")
        with col3:
            if st.button("🗑️ Clear Cart", key="clear_cart"):
                st.session_state.quantities = defaultdict(int)
                st.session_state.cart_total = 0.0
                save_cart(st.session_state.quantities)
                st.rerun()  # Updated from experimental_rerun()

# Add New Product Tab
with tabs[1]:
    st.markdown("<h2 style='text-align: center;'>Add New Product</h2>", unsafe_allow_html=True)
    
    # Display success message if product was added
    if 'show_success' in st.session_state and st.session_state.show_success:
        st.success("Product added successfully!")
        st.session_state.show_success = False  # Reset after showing
    
    # Create form for adding a new product
    with st.form(key='add_product_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Part Number", key="new_part_number", placeholder="E.g., A12345")
            st.text_input("Product Name", key="new_product_name", placeholder="E.g., Bosch Power Drill")
            st.text_area("Description", key="new_description", placeholder="Enter product description here...")
        
        with col2:
            st.text_input("Country of Origin", key="new_country", placeholder="E.g., China")
            st.number_input("Price (EGP)", key="new_price", min_value=0.0, step=0.01, format="%.2f")
            st.text_input("Barcode", key="new_barcode", placeholder="E.g., 1234567890123")
        
        # Submit button
        submit_button = st.form_submit_button(label="Add Product", on_click=add_new_product)

# Manage Inventory Tab
with tabs[2]:
    st.markdown("<h2 style='text-align: center;'>Manage Inventory</h2>", unsafe_allow_html=True)
    
    # Display success message if product was deleted
    if st.session_state.delete_success:
        st.success("Product deleted successfully!")
        st.session_state.delete_success = False  # Reset after showing
    
    # Display all products with delete buttons
    for index, row in st.session_state.products_df.iterrows():
        part_number = row['Part Number'] if not pd.isna(row['Part Number']) else ""
        product_name = row['Product Name']
        key = f"{part_number}_{product_name}"
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"<div class='product-name'>{product_name}</div>", unsafe_allow_html=True)
            st.write(f"Part Number: {part_number}")
            st.write(f"Price: {row['Price (EGP)']:.2f} EGP")
        
        with col2:
            st.markdown(f"<div class='barcode'>Barcode: {row['Barcode']}</div>", unsafe_allow_html=True)
            st.write(f"Country: {row['Country']}")
        
        with col3:
            st.markdown("<div class='delete-button'>", unsafe_allow_html=True)
            st.button("🗑️ Delete", key=f"del_{key}", on_click=show_delete_confirmation, args=(key,))
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
    
    # Data backup and restore options
    st.markdown("<h3 style='text-align: center; margin-top: 30px;'>Data Management</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Backup Data", key="backup_data"):
            try:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"inventory_backup_{timestamp}.json"
                
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.products_df.to_dict('records'), f, ensure_ascii=False, indent=4)
                
                st.success(f"Data backed up to {backup_file}")
            except Exception as e:
                st.error(f"Error creating backup: {e}")
    
    with col2:
        # This is a placeholder. In a real application, you would need a way to select and upload files
        if st.button("Restore Default Data", key="restore_defaults"):
            if st.session_state.products_df is not None:
                st.session_state.products_df = create_default_data()
                st.success("Default data restored!")
                st.rerun()  # Updated from experimental_rerun()

# Delete confirmation dialog - Using Streamlit containers for better display
if st.session_state.show_delete_confirm:
    # Create a container for the confirmation dialog
    confirmation_container = st.container()
    
    with confirmation_container:
        st.markdown("<div style='background-color: #f8d7da; padding: 20px; border-radius: 5px; border: 1px solid #f5c6cb;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #721c24;'>Confirm Deletion</h3>", unsafe_allow_html=True)
        st.markdown("<p>Are you sure you want to delete this product?</p>", unsafe_allow_html=True)
        st.markdown("<p>This action cannot be undone.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add buttons for confirmation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cancel", key="cancel_delete"):
                cancel_delete()
                st.rerun()  # Updated from experimental_rerun()
        with col2:
            if st.button("Delete", key="confirm_delete"):
                delete_product()
                st.rerun()  # Updated from experimental_rerun()
