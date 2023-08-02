import streamlit as st
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv
import holoviews as hv
hv.extension('bokeh', logo=False)

# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("mapbox")
px.set_mapbox_access_token(map_box_api)

# Import the necessary CSVs to Pandas DataFrames
# YOUR CODE HERE!

file_path = Path("Data/sfo_neighborhoods_census_data.csv")
sfo_data = pd.read_csv(file_path, index_col="year")
sfo_data.head()

'''
### Real Estate Analysis of San Francisco from 2010 to 2016

'''

# Define Panel Visualization Functions
def housing_units_per_year():
    housing_units = sfo_data.groupby('year')['housing_units'].mean()
    min_units = housing_units.min()
    max_units = housing_units.max()
    std_units = housing_units.std()
    fig = plt.figure()
    housing_units.plot(kind = 'bar')
    plt.xlabel('Year')
    plt.ylabel('Housing Units')
    plt.title('Housing units by year')
    plt.ylim(min_units - std_units, max_units + std_units)
    return fig

    
    # YOUR CODE HERE!


def average_gross_rent():
    avg_gross_years = sfo_data.groupby('year')['gross_rent'].mean()
    min_units = avg_gross_years.min()
    max_units = avg_gross_years.max()
    std_units = avg_gross_years.std()
    fig = plt.figure() 
    avg_gross_years.plot(kind = 'line', color='red')
    plt.xlabel('Year')
    plt.ylabel('average gross rent')
    plt.title('average gross rent over the years')
    plt.ylim(min_units - std_units, max_units + std_units)
    return fig

    
    # YOUR CODE HERE!



def average_sales_price():
    avg_sale_years = sfo_data.groupby('year')['sale_price_sqr_foot'].mean()
    min_units = avg_sale_years.min()
    max_units = avg_sale_years.max()
    std_units = avg_sale_years.std()
    fig = plt.figure()
    avg_sale_years.plot(kind = 'line')
    plt.xlabel('Year')
    plt.ylabel('Sale price (Sqft)')
    plt.title('Average sale price/Sqft over the years')
    plt.ylim(min_units - std_units, max_units + std_units)
    return fig

    
    # YOUR CODE HERE!



def average_price_by_neighborhood():
    year_nbhd = sfo_data.groupby([sfo_data.index, 'neighborhood']).mean().reset_index()
    model = year_nbhd.hvplot.line(x='year', y='sale_price_sqr_foot', groupby='neighborhood').opts(xlabel = 'Year', ylabel='Sale Price/Sqft')
    return hv.render(model)




    
    # YOUR CODE HERE!



def top_most_expensive_neighborhoods():
    expensive_hoods = sfo_data.groupby('neighborhood')['gross_rent'].mean()
    top_10_hoods = expensive_hoods.nlargest(10)
    model = top_10_hoods.hvplot.bar(rot=37)
    return hv.render(model)



    # YOUR CODE HERE!


def most_expensive_neighborhoods_rent_sales():
    year_nbhd = sfo_data.groupby([sfo_data.index, 'neighborhood']).mean().reset_index()
    model = year_nbhd.hvplot.bar('year', ['sale_price_sqr_foot', 'gross_rent'], rot=37, groupby='neighborhood').opts(xlabel= 'Year', ylabel='gross rent vs price per sqft')
    return hv.render(model)

    
    # YOUR CODE HERE!



def neighborhood_map():
    coordpath = Path("Data/neighborhoods_coordinates.csv")
    hood_coords = pd.read_csv(coordpath)
    hood_coords.rename(columns={'Neighborhood': 'neighborhood'}, inplace=True)
    means = sfo_data.groupby(["neighborhood"]).mean()
    means.reset_index(inplace=True)
    joined_df = means.merge(hood_coords, on='neighborhood')
    re_mapbox = px.scatter_mapbox(
        joined_df,
        lat='Lat',
        lon='Lon',
        hover_name='neighborhood',
        color='gross_rent',
        size='sale_price_sqr_foot',
        zoom=10,
        mapbox_style='carto-positron'
    )
    re_mapbox.update_layout(mapbox=dict(accesstoken=map_box_api))
    return re_mapbox
    

    # YOUR CODE HERE!

tab1, tab2, tab3 = st.tabs(['Welcome', 'Yearly Market Analysis', 'Neighborhood Analysis'])
with tab1:
    st.write('This is an analysis of the housing market in San Francisco covering the years 2010-2016. You can use the tabs above to navigate through different types of information wtih visualizations. This shows various data such as what neighborhoods are most expensive to live in, charts showing changes in rent or housing units available, as well as sale price data.')
    st.subheader("Average sale price and gross rent per square foot in San Francisco")
    st.plotly_chart(neighborhood_map())
with tab2:
    st.header('Yearly Market Analysis')
    st.write('These charts show the shocking revelation that as housing availability went up, so did the price per square foot, and the average gross rent.')
   
    st.pyplot(housing_units_per_year())
   
    st.pyplot(average_gross_rent())
    
    st.pyplot(average_sales_price())
    
with tab3:
    st.write('This tab shows some different information about the individual neighbordhoods in a bit more detail. the first chart is Average prices by neighborhood and how they\'ve changed over the years. The second chart depicts the average gross rent in the top ten most expensive neighborhoods, whereas the third chart compares the most expensive neighborhoods\' gross rent and sales price per square foot.' )
    st.bokeh_chart(average_price_by_neighborhood())
    st.bokeh_chart(top_most_expensive_neighborhoods())
    st.bokeh_chart(most_expensive_neighborhoods_rent_sales())
                            


# Start Streamlit App
# YOUR CODE HERE!
