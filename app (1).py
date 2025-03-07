
import streamlit as st
import pandas as pd

# Load data
SPARES_FILE = 'spares_inventory.csv'

@st.cache_data
def load_data():
    try:
        return pd.read_csv(SPARES_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Part Number', 'Part Name', 'Brand', 'Quantity', 'Price', 'Supplier', 'Date Added'])

def save_data(df):
    df.to_csv(SPARES_FILE, index=False)

def main():
    st.title('Motorbike Spares Inventory Management App')

    menu = ['View Inventory', 'Add Spare Part', 'Update Quantity', 'Remove Spare Part', 'Search Spare Part']
    choice = st.sidebar.selectbox('Menu', menu)

    df = load_data()

    if choice == 'View Inventory':
        st.subheader('Spare Parts Inventory')
        st.write(df)

    elif choice == 'Add Spare Part':
        st.subheader('Add New Spare Part')
        with st.form('add_spare_form'):
            part_number = st.text_input('Part Number')
            part_name = st.text_input('Part Name')
            brand = st.text_input('Brand')
            quantity = st.number_input('Quantity', min_value=0)
            price = st.number_input('Price', min_value=0.0, format="%.2f")
            supplier = st.text_input('Supplier')
            date_added = st.date_input('Date Added')
            submitted = st.form_submit_button('Add Spare Part')

            if submitted:
                new_part = {
                    'Part Number': part_number,
                    'Part Name': part_name,
                    'Brand': brand,
                    'Quantity': quantity,
                    'Price': price,
                    'Supplier': supplier,
                    'Date Added': date_added.strftime('%Y-%m-%d')
                }
                df = df.append(new_part, ignore_index=True)
                save_data(df)
                st.success(f'Added {part_name} to inventory!')

    elif choice == 'Update Quantity':
        st.subheader('Update Spare Part Quantity')
        part_number = st.text_input('Enter Part Number to Update')
        if st.button('Search'):
            part = df[df['Part Number'] == part_number]
            if not part.empty:
                st.write(part)
                new_quantity = st.number_input('New Quantity', min_value=0)
                if st.button('Update Quantity'):
                    df.loc[df['Part Number'] == part_number, 'Quantity'] = new_quantity
                    save_data(df)
                    st.success(f'Updated quantity for {part_number}')
            else:
                st.error('Part not found')

    elif choice == 'Remove Spare Part':
        st.subheader('Remove Spare Part')
        part_number = st.text_input('Enter Part Number to Remove')
        if st.button('Remove'):
            if part_number in df['Part Number'].values:
                df = df[df['Part Number'] != part_number]
                save_data(df)
                st.success(f'Removed {part_number} from inventory')
            else:
                st.error('Part not found')

    elif choice == 'Search Spare Part':
        st.subheader('Search Spare Part')
        search_term = st.text_input('Enter Part Number or Name to Search')
        if st.button('Search'):
            results = df[(df['Part Number'].str.contains(search_term, case=False)) |
                         (df['Part Name'].str.contains(search_term, case=False))]
            st.write(results)

if __name__ == '__main__':
    main()
