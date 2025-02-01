
from pathlib import Path
from shiny import reactive
import plotly.express as px
from shiny.express import render , input, ui
from shinywidgets import render_plotly
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import folium 
from folium.plugins import HeatMap
from ipywidgets import Widget
from shinywidgets import render_widget

ui.tags.style(
    """ 
    """
)

ui.page_opts(window_title="Sales Dashboard", fillable=False)

@reactive.calc
def dat():
    infile = Path(__file__).parent / "data/sales.csv"
    df = pd.read_csv(infile)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    df['hour'] = df['order_date'].dt.hour
    df['value'] = df['quantity_ordered'] * df['price_each']
    return df

@reactive.calc
def color():
    return "red" if input.bar_color() else "blue"

with ui.div(class_ = "header-container"):
    # with ui.div(class_= "logo-container"):
    #     @render.image  
    #     def image():
    #         # here = Path(__file__).parent
    #         img = {"src": "shiny-python-projects/assets/shiny-logo.png", "width": "100px"}  
    #         return img
        
    with ui.div(class_ = "title-container"):
        ui.h2("Sales Dashboard")



with ui.card():  
    ui.card_header("Sales City 2023")

    with ui.layout_sidebar():  
        with ui.sidebar(bg="#f8f8f8"):  
            ui.input_selectize(  
            "city",  
            "Select a City:",  
            ['Dallas (TX)', 'Boston (MA)', 'Los Angeles (CA)', 'San Francisco (CA)', 'Seattle (WA)', 'Atlanta (GA)', 'New York City (NY)', 'Portland (OR)', 'Austin (TX)', 'Portland (ME)'],  
            multiple=False,  
            selected='Dallas (TX)'
            )  
    
            ui.input_checkbox("bar_color", "Make Bars Red?", False)  

        @render_plotly
        def sales_over_time():
            #print(input.city())
            df = dat()
            
            # print(list(df.city.unique()))
            sales = df.groupby(['city' , 'month'])['quantity_ordered'].sum().reset_index()
            #sales_by_city = sales[sales['city'].isin(input.city())]
            sales_by_city = sales[sales['city'] == input.city()]
            #print(sales_by_city)
            month_orderes = calendar.month_name[1:]
            fig = px.bar(sales_by_city , x='month' , y='quantity_ordered' ,title= f"Sales Over Time -- {input.city()}" , category_orders= {'month':month_orderes})
            # fig.update_traces(marker_color = color())
            return fig  


with ui.layout_column_wrap(width=1/2):
    with ui.navset_card_underline(id="tab" , footer=ui.input_numeric("numeric", "Number of Items", 5, min=1, max=10)):  
        with ui.nav_panel("Top Sellers"):
                                                          # start Value
            #ui.input_numeric("numeric", "Number of Items", 5, min=1, max=10)  
        
            @render_plotly
            def plot_top_sellers():
                    df = dat()
                    top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.numeric()).reset_index()
                    return px.bar(top_sales, x="product" , y ='quantity_ordered')        

        with ui.nav_panel("Top Sellers Value ($)"):
            @render_plotly
            def plot_top_sellers_values():
                    df = dat()
                    top_sales = df.groupby('product')['value'].sum().nlargest(input.numeric()).reset_index()
                    return px.bar(top_sales, x="product" , y ='value') 

        with ui.nav_panel("Lowest Sellers"):
            @render_plotly
            def plot_lowest_sellers():
                    df = dat()
                    top_sales = df.groupby('product')['quantity_ordered'].sum().nsmallest(input.numeric()).reset_index()
                    return px.bar(top_sales, x="product" , y ='quantity_ordered') 
        with ui.nav_panel("Lowest Sellers Value($)"):
            @render_plotly
            def plot_lowest_sellers_values():
                    df = dat()
                    top_sales = df.groupby('product')['value'].sum().nsmallest(input.numeric()).reset_index()
                    return px.bar(top_sales, x="product" , y ='value') 
    
    with ui.card():
        ui.card_header("Sales by time of Day Heatmap")  
        @render.plot
        def plot_sales_bt_time():
            df = dat()
            sales_by_hour = df['hour'].value_counts().reindex(np.arange(0,24), fill_value = 0)
            # print(sales_by_hour)
            #plt.bar(x = sales_by_hour['hour'] , height=sales_by_hour['count'])
            heatmap_data = sales_by_hour.values.reshape(24,1)
            sns.heatmap(heatmap_data,
                        annot= True,
                        fmt="d",
                        cbar=False,
                        cmap="coolwarm",
                        xticklabels=[],
                        yticklabels=[f"{i}:00" for i  in range(24)])
            plt.title("Numbers of Orders by Hours of Day")
            plt.xlabel("Hours of Day")
            plt.ylabel("Orderes Count")
        
        
  

with ui.card():
    ui.card_header("Sales by Location map")
    @render.ui
    def plot_us_heatmap():
        df = dat()
        
        heatmap_data = df[['lat' , 'long' , 'quantity_ordered']].values
        
        map = folium.Map(location=[37.0902, -95.7129] , zoom_start=4)
        HeatMap(heatmap_data).add_to(map)
        return map
        # print(heatmap_data)
    



    

# with ui.layout_columns():
with ui.card():
    ui.card_header("Samples Sales Data")
    @render.data_frame
    def sample_sales_data():
        return dat().head(5)  
        # df = dat()
        # print(df)     
     

    
   
    
    

    
        
    

