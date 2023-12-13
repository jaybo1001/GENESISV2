import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image



# Define default values
default_revenue = 15.10
default_ebit = 2.10
default_northstar = 0.015


# Display an image in the sidebar
image_path = '/Users/polaris/PMPx/genesis_main/app/GENESISV2/images/gen_small.png'
try:
    image = Image.open(image_path)
    st.sidebar.image(image, use_column_width=True)
except FileNotFoundError:
    st.sidebar.error("Image not found. Please check the path.")
st.sidebar.markdown("Adjust the Northstar parameter.")

northstar_value = st.sidebar.slider("Northstar", min_value=-0.05, max_value=0.05, value=default_northstar)


# Chart at the top of the page

st.image('GENESISV2/images/uipath_northstar.png', use_column_width=600) 
#st.title("Intelligent Automation Benchmarks Net Impact")
st.markdown("""
    <hr style="border: 4px solid '#F6F6F6'; margin-bottom: 25px give me; margin-top: 0px;" />
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    .title-font {
        font-size: 30px;
        font-weight: bold;
        color: white;
        font-family: 'Arial';
    }
    </style>
    <h1 class="title-font">Intelligent Automation Benchmarks Net Impact</h1>
    """, unsafe_allow_html=True)



st.markdown("""
    <hr style="border:2px solid #004289; margin-bottom: 25px give me; margin-top: 0px;" />
""", unsafe_allow_html=True)

# Two columns below the chart for sliders
left_column, right_column = st.columns(2)

# Left column - Annual Productivity Gain slider
with left_column:
    st.image('GENESISV2/images/prod_benchmark.png', use_column_width=600)    
    annual_productivity_gain = st.slider("Annual Productivity Gain", min_value=0.05, max_value=0.10, value=0.02)

# Right column - Annual % Impact to EBIT slider
with right_column:
    st.image('GENESISV2/images/ebit_benchmark.png', use_column_width=600)
    
    annual_impact_to_ebit = st.slider("Annual % Impact to EBIT", min_value=0.10, max_value=0.40, value=0.15)

# Perform the calculations
years = list(range(1, 6))
productivity_benchmarks = [default_revenue * annual_productivity_gain * year for year in years]
ebit_benchmarks = [default_ebit * annual_impact_to_ebit * year for year in years]
northstar_assessments = [default_revenue * northstar_value * year for year in years]



#with real_right:
    # Plotting the chart
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.plot(years, productivity_benchmarks, label='Productivity Benchmark', linewidth=3, color='#F4A700')
ax.plot(years, ebit_benchmarks, label='EBIT Benchmark', linewidth=3, color='#DC2560')
ax.plot(years, northstar_assessments, label='Northstar Assessment', linewidth=3, color='#0BA2B3')
#ax.set_xlabel('')
#ax.set_ylabel('')
#ax.set_xlabel('Year', color='white')
#ax.set_ylabel('Value', color='white')
ax.set_title('Net Impact', color='white')
ax.spines['bottom'].set_color('white')
#ax.spines['top'].set_color('white') 
#ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
legend = ax.legend(facecolor='black',  edgecolor='none', fontsize='xx-small')  # Set legend background color to black
for text in legend.get_texts():
    text.set_color('white') 
st.pyplot(fig)

st.divider() 