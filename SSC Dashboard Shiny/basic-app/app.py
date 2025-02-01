import faicons as fa
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


from shiny import App, Inputs, Outputs, Session, reactive, render, ui
import plotly.express as px
# from shiny.express import render
from shinywidgets import render_plotly, output_widget
import plotly.graph_objects as go
from pandas.io.stata import StataReader
from shiny import App, reactive, render, ui



ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "wallet": fa.icon_svg("wallet"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),

}

app_ui = ui.page_sidebar(
   # First nav item - Data Table
    ui.sidebar(
               
                ui.input_selectize(
                    "players",
                    "Select the the age of the respondent",
                    multiple=True,
                    choices=['a', 'b'],
                    selected=["893", "2544", "201939"],
                    width="100%",
                ),
                    
               
               title="Filter controls",
               ), 
    
    ui.include_css("basic-app\style.css"),
    
    ui.layout_columns(
        ui.value_box(
            "Number of Supervisor", ui.output_ui("noOfsupervisor"), showcase=ICONS["user"]
        ),
        ui.value_box(
            "Number of Enumurator", ui.output_ui("noOfenum"), showcase=ICONS["user"]
        ),
        
        ui.value_box(
            "No of Male Enumurator",
            ui.output_ui('noOfMaleEnumurator'), showcase=ICONS["user"],
        ),
        
        # ui.value_box(
        #     "No of Female Enumurator",
        #     ui.output_ui('noOfFemaleEnumurator'), showcase=ICONS["user"],
        # ),
        # ui.value_box(
        #     "Average bill",
        #     ui.output_ui("average_bill"),
        #     showcase=ICONS["currency-dollar"],
        # ),
        fill=True,
    ),
    
    
    ui.card(
        "all non contact of enumurator",
        
            ui.navset_card_underline(
                ui.nav_panel(
                    "Top Enumerators",
                    output_widget("topEnumurator")
                ),
                ui.nav_panel(
                    "Bottom Enumurators",
                    output_widget("bottomEnumurator")
                ),
                
                ui.nav_panel(
                    "Male Enumurators",
                    output_widget("MaleEnumurator")
                ),
                
                ui.nav_panel(
                    "Female Enumurators",
                    output_widget("FemaleEnumurator")
                ),
                
                id="tab",
                footer=ui.row(
                ui.column(8, ui.input_numeric("numeric", "Number of Enumurators", 5, min=1, max=27)),
                ui.column(4, ui.output_ui("conditional_checkbox"))
            )

            ),
        ),
    
    
    ui.layout_column_wrap(
        
        ui.card("Distribution of Visits by Day of Week",              
                output_widget('daysofweek_pie')
                
                
                
                
                ),
        ui.card("Time Analysis",
                
                output_widget('time_scatter')
                
                ),
        
        width=1/2,
        ),
        
    ui.card(
        
        "Calender Heat Map",
        output_widget('calendar_heatmap')
        
        ),
    
    ui.card(
            ui.card_header("DTA File Table"),
            ui.output_data_frame("dta"),
        ),    
    
    
    
    title=ui.row(
        ui.column(3, 
             ui.output_image("image" , inline=True), 
        ),
        ui.column(9, 
            ui.h1("ARCED")
        ),
        class_= 'd-flex align-items-center'
    ),
  
    # title="ARCED",
    
    # You can add more nav items as needed
    # ui.nav("Another Tab", ...),
)


def server(input, output, session):
    @reactive.calc
    def dtafile():
        # Replace 'file.dta' with the path to your .dta file
        # input stata --> pd
        dir = Path(__file__).parent
        df = pd.read_stata(dir / "SCS_data.dta")
        # print(df.shape[1])
        # print(df.columns.tolist())
        return df
    
   
    
    @render.data_frame
    def dta():
        df = dtafile()
        distinct_values = df['agegroup_label'].unique().tolist()
        # print(distinct_values)
        return render.DataGrid(dtafile().head(5))    
        
    @reactive.calc
    def age_choices():
        df = dtafile()
        distinct_values = df['agegroup_label'].unique().tolist()
        
        ui.update_selectize(
            "players",
            choices=distinct_values,
            selected=distinct_values[0] 
        )
        
        return sorted(distinct_values)
    
    # Update selectize choices when data is loaded
    @reactive.effect
    def _():
        choices = age_choices()
        ui.update_selectize(
            "players",
            choices=choices,
            selected=choices[0] if choices else None
        )
        
    @render.image  
    def image():
        img = {"src": "basic-app\www\Logo.png", "width": "35px", }
        return img
    
    @render.text
    def value():
        return f"{input.select()}"
    
    @render.ui
    def noOfsupervisor():
        df = dtafile()
        # uniueSupervisor = (df['superid'].unique().tolist())
        uniueSupervisor = len ((df['superid'].unique().tolist()))
        # print(uniueSupervisor)
        
        
        # print(group_data)
        return  uniueSupervisor
    
    @render.ui
    def noOfMaleEnumurator():
        df = dtafile()
        # uniueSupervisor = (df['superid'].unique().tolist())
        male = len(df[df['sex'] == 'Male']['enumid'].unique().tolist()) - 3 
        # print(uniueSupervisor)
        
        
        # print(group_data)
        return  male
    
    
    @render.ui
    def noOfFemaleEnumurator():
        df = dtafile()
        # uniueSupervisor = (df['superid'].unique().tolist())
        male = len(df[df['sex'] == 'Female']['enumid'].unique().tolist()) - 3 
        # print(uniueSupervisor)
        
        
        # print(group_data)
        return  male
    
    @render.ui
    def noOfenum():
        df = dtafile()
        #enumid = (df['enumid'].unique().tolist())
        enumid = len ((df['enumid'].unique().tolist()))
        return  enumid
    
    @render.ui
    def conditional_checkbox():
        if input.tab() == "Top Enumerators":
            return ui.input_checkbox("color_by_gender", "Color by Gender", True)
        return ui.div()  # Return empty div when not on Top Enumerators tab
    
    def modify_enumurator():
        df = dtafile()
        
        axis_labels = {
            'enumid': 'Enumerator ID',
            'allnoncontact': 'Non-Contact Count',
            'sex': 'Gender'
        }
        
        # Check which tab is active by ID 
        if input.tab() == "Top Enumerators":
           group_data = df.groupby(['enumid', 'sex'])['allnoncontact'].sum().reset_index()
           group_data = group_data.nlargest(input.numeric(), 'allnoncontact')
            # Create the plot
           fig = px.bar(group_data, x='enumid', y='allnoncontact' , 
                        color_discrete_sequence=['#ab02fa', '#66B2FF'], 
                        labels=axis_labels)
            # Apply colors if checkbox is checked (only for Top Enumerators)
           if input.color_by_gender():
                fig.update_traces(
                    marker_color=group_data['sex'].map({'Male': '#493D9E', 'Female': '#EFB6C8'})
                )  
                
        elif input.tab() == "Bottom Enumurators" :  # Bottom Enumerators tab
            group_data = df.groupby('enumid')['allnoncontact'].sum().nsmallest(input.numeric()).reset_index()
            
            fig = px.bar(group_data , x ='enumid' , y = 'allnoncontact' , 
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         labels=axis_labels) 
        
        elif input.tab() == "Male Enumurators":
            group_data = ( df[df['sex'] == 'Male']
                          .groupby(['enumid', 'sex'])['allnoncontact']
                          .sum()
                          .nlargest(input.numeric())
                          .reset_index() )
            
            fig = px.bar(group_data , x ='enumid' , y = 'allnoncontact',
                         color_discrete_sequence=px.colors.sequential.Blues,
                         labels=axis_labels)    
            
        elif input.tab() == "Female Enumurators":
            group_data = ( df[df['sex'] == 'Female']
                          .groupby(['enumid', 'sex'])['allnoncontact']
                          .sum()
                          .nlargest(input.numeric())
                          .reset_index() )    
            
            fig = px.bar(group_data , x ='enumid' , y = 'allnoncontact' ,
                         color_discrete_sequence=['#ab02fa', '#66B2FF'],
                         labels=axis_labels) 
        
        return fig
    
    @render_plotly
    def topEnumurator():
        return modify_enumurator()
    
    @render_plotly
    def bottomEnumurator():
        return modify_enumurator()
    
    @render_plotly
    def MaleEnumurator():
        return modify_enumurator()
    
    @render_plotly
    def FemaleEnumurator():
        return modify_enumurator()
    
    
    @render_plotly
    def daysofweek_pie():
        df = dtafile()
        data = df.groupby('day').size().reset_index(name= 'count')
        
        fig = px.pie(data ,
                    values='count',
                    names='day',
                    hover_data=['count'],
                    labels={'count': 'Number of Visits', 'day': 'Day of Week'},
                    color_discrete_sequence=['#493D9E' , '#66B2FF']
                    )
        # Update traces to show percentages in the labels
        fig.update_traces(textposition='inside', 
                     textinfo='percent+label',
                     showlegend=True)
                      
        
        return fig
    
    
    @render_plotly
    def time_scatter():
        df = dtafile()
        
        # Convert Stata time to Python datetime
        # Stata's %tC format measures milliseconds since 01jan1960
        stata_epoch = pd.Timestamp('1960-01-01')
        df['starttime_dt'] = stata_epoch + pd.to_timedelta(df['starttime'], unit='ms')
        df['endtime_dt'] = stata_epoch + pd.to_timedelta(df['endtime'], unit='ms')
        
        # Create the scatter plot
        fig = px.scatter(df, 
                        x='starttime_dt', 
                        y='endtime_dt',
                        title='Start Time vs End Time Distribution',
                        labels={
                            'starttime': 'Start Time',
                            'endtime': 'End Time'
                        },
                        color_discrete_sequence=px.colors.sequential.Plasma)
        
        # Update layout for better readability
        fig.update_layout(
            xaxis_title="Start Time",
            yaxis_title="End Time",
            showlegend=False
        )
        
        # Add a diagonal reference line (y=x)
        fig.add_scatter(
            x=[df['starttime_dt'].min(), df['starttime_dt'].max()],
            y=[df['starttime_dt'].min(), df['starttime_dt'].max()],
            mode='lines',
            line=dict(dash='dash', color='red'),
            name='Equal Time Line'
        )
        
        return fig
    
    @render_plotly
    def calendar_heatmap():
        df = dtafile()
        
        # Convert Stata time to Python datetime
        stata_epoch = pd.Timestamp('1960-01-01')
        df['starttime_dt'] = stata_epoch + pd.to_timedelta(df['starttime'], unit='ms')
        
        # Extract date and count surveys per day
        # Instead of using datetime.date objects
        df['date'] = df['starttime_dt'].dt.strftime('%Y-%m-%d')
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        # Create calendar heatmap
        fig = go.Figure(data=go.Heatmap(
            x=daily_counts.date,
            y=[1],  # Single row
            z=[daily_counts['count']],
            colorscale='Viridis',
            showscale=True,
            text=[[str(x) for x in daily_counts['count']]],
            texttemplate="%{text}",
            hoverongaps=False,
        ))

        # Update layout
        fig.update_layout(
            title='Survey Distribution Calendar',
            xaxis_title='Date',
            yaxis_visible=False,
            height=200,  # Adjust height as needed
            xaxis=dict(
                tickformat='%Y-%m-%d',
                tickangle=45,
            )
        )
        
        return fig



app = App(app_ui, server)