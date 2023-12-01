import streamlit as st
from pymongo import MongoClient

# Establish a MongoClient Connection
client = client = MongoClient(st.secrets["mongo"]["url"])
collection = client['Genesis-enriched']['**COMPANY']
search_collection = client['Genesis-enriched']['**G-TYPE Search']  # Collection for search

# Fetch the first document
document = collection.find_one()
logo = "/Users/polaris/Genasis/gen_small.png"
st.image(logo, use_column_width=True)


# Create text input boxes pre-filled with the company data
company_name = st.text_input('Company Name', document['Company Name'])
annual_revenue = st.text_input('Annual Revenue ($M)', document['Annual Revenue ($M)'])
annual_ebit = st.text_input('Annual EBIT ($M)', document['Annual EBIT ($M)'])
ticker = st.text_input('Ticker', document['Ticker'])
total_employees = st.text_input('Total Employees', document['Total Employees'])
g_type = st.text_input('G-TYPE', document['G-TYPE'])


# Create a button for updating the record
if st.button('Update Record'):
    # Update the document with new data
    collection.update_one({'_id': document['_id']}, {"$set": {
        'Company Name': company_name,
        'Annual Revenue ($M)': annual_revenue,
        'Annual EBIT ($M)': annual_ebit,
        'Ticker': ticker,
        'Total Employees': total_employees,
        'G-TYPE': g_type
    }})
    st.success('Record updated successfully.')

# Create a text input box for the search term
search_term = st.text_input('Search for G-TYPE: ')

# If the search term is not empty, perform the search
if search_term:
    # Define the search pipeline
    pipeline = [
        {
            "$search": {
                "index": "default",
                "text": {
                    "query": search_term,
                    "path": "GEN_CODE_description"  # Searching in the **G-TYPE Search field
                }
            }
        }
    ]

    # Run the search
    results = list(search_collection.aggregate(pipeline))

    # Create a placeholder for the results
    results_placeholder = st.empty()

    # Check if results is empty
    if not results:
        results_placeholder.write("No match found, please try a different search")
    else:
        # Print the parsed results
        for result in results:
            gen_code = result.get('GEN_CODE', 'N/A')
            description = result.get('GEN_CODE_description', 'N/A')
            results_placeholder.write(f"GEN_CODE: {gen_code} \n  Description: {description}")