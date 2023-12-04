import streamlit as st
from pymongo import MongoClient
import streamlit.components.v1 as components



# Inject the CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)

# Establish a MongoClient Connection
client = MongoClient('mongodb+srv://jaybo2:pmp1jmb@cluster0.dosdp0e.mongodb.net/')
collection = client['Genesis-enriched']['**COMPANY']
search_collection = client['Genesis-enriched']['**G-TYPE Search']  # Collection for search

# Fetch the first document
document = collection.find_one()
logo = "/Users/polaris/Genasis/gen_small.png"

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

import random

# Generate a random number
rand_num = random.randint(0, 1000000)

# Add a title to the top of the frame with the graphs
st.image(logo, width=400)
st.title(company_name)

# Embed the iframe
iframe_html = f"""
<iframe style="background: #21313C;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);width: 100vw;height: 100vh;"  src="https://charts.mongodb.com/charts-genesis-zvkbj/embed/dashboards?id=6561218b-9d63-42d3-9f7d-7b7f3c2c052d&theme=dark&autoRefresh=true&maxDataAge=3600&showTitleAndDesc=false&scalingWidth=scale&scalingHeight=scale"></iframe>
"""
components.html(iframe_html, height=1500, width=1000)

