import streamlit as st
from pymongo import MongoClient
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
from work_breakdown_plot import plot_work_breakdown

st.set_page_config(layout="wide")

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


# Call the function to get the plot
plot = plot_work_breakdown()

# Display the plot in the Streamlit app
st.pyplot(plot)