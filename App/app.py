#import relevant libraries
import pandas as pd
import base64
import plotly as py
import plotly.express as px
import streamlit as st

#load data
vdf_clean = pd.read_csv('vdf_clean.csv')
col1, col2, col3 = st.columns([1, 3, 1])
#open and set title image
with col2:
    # Display the image in the center column
    st.image("https://github.com/sonia-joseph/Car_advertisement_app/blob/main/App/logo.png?raw=true", width=1000)

#title and description
st.title('Used Car Data App')
st.markdown("""
This app looks at the change in used car model availability and price changes over time
""")
#expandable about bar
expander_bar = st.expander("**About**")
expander_bar.markdown("""
***Python Libraries:*** pandas, base64, plotly, streamlit

***Credit*** [Data Professor Chanin Nantasenamat (aka Data Professor)](https://www.youtube.com/watch?v=JwSS70SZdyM)"
""")

# create a text header above the dataframe
st.header('Data Viewer') 
# display the dataframe with streamlit
st.dataframe(vdf_clean)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="vehicle.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(vdf_clean), unsafe_allow_html=True)

#New section title
st.header('Distribution and number of models introduced over time')
#group the vehicle database by year and types to see the distribution of the types by year
yearly_type = vdf_clean.groupby(['model_year','type']).count().reset_index()
yearly_type.rename(columns={'price': 'number_of_vehicles'}, inplace=True)
yearly_type.drop(columns=['model','condition','cylinders','fuel','odometer','transmission','paint_color','is_4wd','date_posted','days_listed'], inplace=True)

#slider for the years
yr_select = st.slider('Select a time range', 1920,2019,(1990,2019))
start,end = yr_select
yearly_type_x = yearly_type[(yearly_type['model_year'] >=start) & (yearly_type['model_year'] <= end)]

#if checkbox is selected numerical data for the various car types is displayed
if st.checkbox('Show more details'):
    detailed_types_bar2 = px.bar(yearly_type_x,
                            x ='model_year', 
                            y = 'number_of_vehicles', 
                            color = 'type', 
                            title='Vehicles yearly distribution classified by type', 
                            text = 'number_of_vehicles',
                            labels = dict(model_year = 'Year', number_of_vehicles = 'Number of vehicles of the type'),
                            height=600,
                            width=1000
                            )
    st.write(detailed_types_bar2)
else:
    detailed_types_bar = px.bar(yearly_type_x,
                            x ='model_year', 
                            y = 'number_of_vehicles', 
                            color = 'type', 
                            title='Vehicles yearly distribution classified by type',
                            labels = dict(model_year = 'Year', number_of_vehicles = 'Number of vehicles of the type'),
                            height=600,
                            width=1000
                            )
    st.write(detailed_types_bar)
#show a scatter for price change for a manufacturer over time

#new section
st.header('Price change over time')
#select manufacturer
sorted_brand = sorted( vdf_clean['manufacturer'].unique())
selected_brands = st.multiselect('Manufacturer', sorted_brand, sorted_brand)
yr_select2 = st.slider('Select a time range', 1920,2019,(2000,2019))
start2,end2 = yr_select2
#filter on selection
df_x = vdf_clean[(vdf_clean['model_year'] >=start2) & (vdf_clean['model_year'] <= end2)]
df_selected_brands = df_x[ (df_x['manufacturer'].isin(selected_brands)) ]

#scatter plot on filtered data
Price_scatter = px.scatter(df_selected_brands, 
                            x='model_year', 
                            y='price',
                            title='Price vs year, by type', 
                            color = 'manufacturer',
                            hover_name = 'model',
                            hover_data=['model', 'condition', 'odometer'],
                            labels = dict(model_year = 'Year', price = 'Price', manufacturer = 'Manufacturer'),
                            color_discrete_sequence= px.colors.qualitative.Light24,
                            height=600,
                            width=800)
st.write(Price_scatter)
