import streamlit as st
from pymongo import MongoClient
import streamlit.components.v1 as components



# Establish a MongoClient Connection
client = MongoClient('mongodb+srv://jaybo2:pmp1jmb@cluster0.dosdp0e.mongodb.net/')
collection = client['Genesis-enriched']['**COMPANY']
search_collection = client['Genesis-enriched']['**G-TYPE Search']  # Collection for search

# Fetch the first document
document = collection.find_one()
logo = "gen_small.png"

# Create a sidebar
sidebar = st.sidebar
sidebar.image(logo, use_column_width=True)

# Create text input boxes pre-filled with the company data
company_name = sidebar.text_input('Company Name', document['Company Name'])
annual_revenue = sidebar.text_input('Annual Revenue ($M)', document['Annual Revenue ($M)'])
annual_ebit = sidebar.text_input('Annual EBIT ($M)', document['Annual EBIT ($M)'])
ticker = sidebar.text_input('Ticker', document['Ticker'])
total_employees = sidebar.text_input('Total Employees', document['Total Employees'])
g_type = sidebar.text_input('G-TYPE', document['G-TYPE'])

# Create a button for updating the record
if sidebar.button('Update Record'):
    # Convert G-TYPE to integer
    g_type = int(g_type)

    # Update the document with new data
    collection.update_one({'_id': document['_id']}, {"$set": {
        'Company Name': company_name,
        'Annual Revenue ($M)': annual_revenue,
        'Annual EBIT ($M)': annual_ebit,
        'Ticker': ticker,
        'Total Employees': total_employees,
        'G-TYPE': g_type
    }})
    sidebar.success('Record updated successfully.')

# Create a text input box for the search term
search_term = sidebar.text_input('Search for G-TYPE: ')

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
    results_placeholder = sidebar.empty()

    # Check if results is empty
    if not results:
        results_placeholder.write("No match found, please try a different search")
    else:
        # Print the parsed results
        for result in results:
            gen_code = result.get('GEN_CODE', 'N/A')
            description = result.get('GEN_CODE_description', 'N/A')
            results_placeholder.write(f"GEN_CODE: {gen_code} \n  Description: {description}")


# Add a title to the top of the frame with the graphs
st.image(logo, width=400)
st.title(company_name)

# Add the first iframe
components.html("""
<iframe style="background: #000000;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-genesis-zvkbj/embed/charts?id=6568ccc3-c315-4791-8556-10b62075ecf3&maxDataAge=60&theme=dark&autoRefresh=true"></iframe>
""", height=480)

# Add the second iframe
components.html("""
<iframe style="background: #000000;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="580" src="https://charts.mongodb.com/charts-genesis-zvkbj/embed/charts?id=1b7a64ad-07ab-4fcc-8b13-a5e5034fe08c&maxDataAge=60&theme=dark&autoRefresh=true"></iframe>
""", height=580)