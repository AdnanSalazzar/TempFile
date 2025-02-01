
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


# @reactive.calc
# def printCode():
#     df = dat()
#      # Group by Department and Attrition
#     department_attrition = df.groupby(['Department', 'Attrition']).size().reset_index(name='Count')
#     # print(department_attrition)   

################################################# app_ui
app_ui = ui.page_fluid(
    ui.include_css("basic-app\style.css"),
    
    # ui.div(
    #     {"class": "header"},
    #     ui.div(
    #         {"class": "logo-container"},
    #         ui.div(
    #         {"class": "logo-container"},
    #         ui.output_image("image"),  # Changed to output_image
    #     ),
    #     ),
    #     ui.h1("Age Group Analysis")
    # ),
    
    
    
    # ui.panel_title("ARCED"),
    
    ui.tags.head(
        ui.tags.style(
            """
            .selectize-input {
                border-radius: 15px;
            }
            """
        )
    ),
    ui.div(
        {"class": "header"},
        ui.div(
            {"class": "logo-container"},
            # Option 1: Using local image file
            ui.output_image("image" , inline=True ),
            # Option 2: Using online image URL
            # ui.img({"src": "https://example.com/logo.png", "class": "logo"})
         
        ),
        ui.h1("ARCED")
    ),
    
    
    
    ui.layout_column_wrap(  
        ui.card(
            ui.card_header("Overall Emplyee"),
            ui.output_text("getTotalPeople"),
            ),
        
        ui.card(
            ui.card_header("Attrition"),
            ui.output_text("getTotalAttrition"),
            ),
        ui.card(
            ui.card_header("Attrition Rate"),
            ui.output_text("getTotalAttritionRate"),
            ),
        ui.card(
            ui.card_header("Active Employee"),
            ui.output_text("activeEmployee"),
            ),
        ui.card(
            ui.card_header("Average Age"),
            ui.output_text("averageAge"),
            ),
        width = 1 / 5,  
    ),
    
    
    
    # Pie chart bar table 
    ui.layout_column_wrap( 
                           
        # ui.card(
        #     "Department Wise Attrition",
        #     ui.output_plot("departmentWiseAttrition"),
        #         ),
                
        ui.card("Department Wise Attrition",  
                
                ui.output_plot("departmentWiseAttritionPie"),  
                
                ),
        ui.card("Employee Distribution by Age Groups and Gender",
                
                ui.output_plot("noOfEmployeebyAgeGroup")
                
                
                
                ),
        ui.card("Card 3",
                
                ui.output_data_frame("jobRoleSatisfactionTable")
                
                
                ),
        width=1 / 3,  
    ),
    
    ui.layout_columns(
        ui.card("Education Field Wise Attrition",
                ui.output_plot("educationFieldAttritionHistogram")
                ),
        ui.card("Attrition Rate by Gender for Different Age Groups",
                ui.output_plot("under25"), 
                ui.output_plot("under35to44") 
                
                ),
        col_widths=(6 , 6 ),
    ),
    
    ui.card(
        ui.card_header("Random Data Histogram"),
        ui.input_selectize(
            "distribution",
            "Select Distribution",
            choices=["Normal", "Uniform"],
            selected="Normal"
        ),
        output_widget("hist")
    ),
    
    ui.card(
        ui.card_header("Education Field-Wise Attrition"),
        output_widget("attrition_plot")
    ),
    
    
    ui.layout_column_wrap(
            
        ui.card(
            ui.card_header("Department wise Attribution"),
            output_widget("departmentWiseAttritionPiePlotly")
        ),
        
        ui.card(
            ui.card_header("No Of Employeeby Age Group Plotly"),
            output_widget("noOfEmployeebyAgeGroupPlotly")
        ),
        
        
        
    ),
    
    ui.layout_column_wrap(
        
        ui.card(
            
            ui.row(
                ui.column(4,
                    ui.input_selectize(
                        "age_group",
                        "Select Age Group",
                        choices=['Under 25', '25 to 34', '35 to 44', '45 to 54', 'Over 55'],
                        selected='25 to 34'
                    ),
        ),
        ),
            ui.row(
                ui.column(8,
                    output_widget("age_gender_pie_plotly"),
                )
            ),
            
        ),
        
        ui.card("Sth else goes here")
        
    ),
    
    
    
    
    # Table 
    ui.card(
        ui.card_header("Main HR Table information"),
        ui.output_data_frame("fullHrTable"),
    ),
    
    # Table 
    ui.card(
        ui.card_header("dta file table "),
        ui.output_data_frame("dta"),
    ),



    # ui.card(
    #     ui.card_header("SCS DATASET"),
    #     ui.output_data_frame("datScsc"),
    # )

    # stata to opd
    
    # ui.card(
    #     "Printing", 
    #     ui.output_text("departmentWiseAttrition")
        
    # )
    
)


################################################# server
def server(input, output, session):
    
    @reactive.calc
    def dat():
        # Define the directory
        dir = Path(__file__).parent
        # Load the Excel file using the Path object
        df = pd.read_excel(dir / "HR Data.xlsx")
        df['Male'] = (df['Gender'] == 'Male').astype(int)
        df['Female'] = (df['Gender'] == 'Female').astype(int)
        print(df)
        return df
    
    @render.data_frame
    def fullHrTable():
        #print(dat().columns.tolist())
        return dat().head(5)
    
   
    @reactive.calc
    def dtafile():
        # Replace 'file.dta' with the path to your .dta file
        # input stata --> pd
        dir = Path(__file__).parent
        df = pd.read_stata(dir / "SCS_data.dta")
        # print(df)
        return df
    
    @render.data_frame
    def dta():
        return render.DataGrid(dtafile().head(2))


# Display the first few rows of the DataFrame
    
    # @output
    # @reactive.calc
    # def datScsc():
    #     # Assuming the .dta file is in the same directory as the app
    #     dir = Path(__file__).parent
    #     df = pd.read_stata(dir / "SCS_data.dta", 
    #                       convert_categoricals=True, 
    #                       convert_dates=True)
    #     return df
    
    @render.image  
    def image():
        img = {"src": "basic-app\img\Logo.png" , "width": "100px"}  
        return img
    
   
    
    @render.text
    def getTotalPeople():
        total_rows = dat().shape[0]
        #print(f"Total number of rows: {total_rows}")
        return total_rows
    
    @render.text
    def getTotalAttrition():
        attrition_counts = dat()['Attrition'].value_counts()
        employees_left = attrition_counts.get('Yes', 0)
        #print(f"Total number of employees_left: {employees_left}")
        return employees_left
        
    @render.text
    def getTotalAttritionRate():
        total_employees = dat().shape[0]
        attrition_counts = dat()['Attrition'].value_counts()
        employees_left = attrition_counts.get('Yes', 0)
        attrition_rate = (employees_left / total_employees) * 100
        attrition_rate = round(attrition_rate, 2)
        formatted_attrition_rate = f"{attrition_rate}%"
        #print(f"Total number of employees_left: {employees_left}")
        return formatted_attrition_rate
    
    @render.text
    def activeEmployee():
        employee = dat()['Attrition'].value_counts().get('No',0)
        #print(f"Total number of employees_left: {employees_left}")
        return employee
    
    @render.text
    def averageAge():
        totalAge = dat()['Age'].sum()
        total_employees = dat().shape[0]
        average_Age = totalAge / total_employees 
        average_Age = round(average_Age, 2)
        average_Age = f"{average_Age}%"
        
        return  average_Age
    
    @render.plot
    def departmentWiseAttrition():
        df = dat()
        # Group by Department and Attrition
        department_attrition = df.groupby(['Department', 'Attrition']).size().reset_index(name='Count')
        #print(department_attrition)
        # Create a bar plot
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(
            data=department_attrition,
            x='Department',
            y='Count',
            hue='Attrition',  # Separate bars for "Yes" and "No"
            palette='Set2'  # Choose a color palette
        )
                
        # Add titles and labels
        plt.title('Department-Wise Attrition', fontsize=16)
        plt.xlabel('Department', fontsize=14)
        plt.ylabel('Number of Employees', fontsize=14)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.legend(title='Attrition')
        return ax
    
    @render.plot
    def departmentWiseAttritionPie():
        df = dat()
        
        department_attrition = df.groupby(['Department', 'Attrition']).size().reset_index(name='Count')
        #print(department_attrition)
        # Filter only rows with Attrition == 'Yes'
        attrition_yes = department_attrition[department_attrition['Attrition'] == 'Yes']  
        # print(attrition_yes) 
        # Get total attrition cases for all departments
        total_yes_counts = attrition_yes['Count'].sum()
        
        
        # Calculate the percentage for each department
        attrition_yes['Percentage'] = (attrition_yes['Count'] / total_yes_counts) * 100
                
        # Values for the pie chart
        sizes = attrition_yes['Count']
        labels = attrition_yes['Department']
        
                
        # Plot the pie chart
        # plt.figure(figsize=(8, 8))
        fig = plt.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',  # Show percentage
            startangle=140,     # Rotate for better aesthetics
            colors=plt.cm.Paired.colors  # Use a colormap
        )
        
        return fig
        
    @render.plot
    def noOfEmployeebyAgeGroup():
        df = dat()
        # Step 1: Define age groups
        bins = [0, 24, 34, 44, 54, float('inf')]  # Bin edges
        labels = ['Under 25', '25 to 34', '35 to 44', '45 to 54', 'Over 55']  # Group labels
        df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

        # Step 2: Group by Age Group and Gender, then count
        age_gender_counts = df.groupby(['Age Group', 'Gender']).size().unstack(fill_value=0)

        # Step 3: Plot the stacked bar graph
        ax = age_gender_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['lightblue', 'lightcoral'])

        # Step 4: Customize the graph
        # plt.title('Employee Distribution by Age Groups and Gender', fontsize=16)
        plt.xlabel('Age Groups', fontsize=14)
        plt.ylabel('Number of Employees', fontsize=14)
        plt.xticks(rotation=0, fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(title='Gender', fontsize=12)

        # Return the current figure
        return ax
    
    
    @render.data_frame
    def jobRoleSatisfactionTable():
        df = dat()

        # Step 1: Create a pivot table
        pivot_table = df.pivot_table(
            index='Job Role',                      # Vertical column: Job Roles
            columns='Job Satisfaction',           # Horizontal row: Job Satisfaction (1 to 4)
            values='Employee Number',             # A unique identifier for counting
            aggfunc='count',                      # Count the number of employees
            fill_value=0                          # Fill missing values with 0
        )

        # Step 2: Add a "Total" column
        pivot_table['Total'] = pivot_table.sum(axis=1)

        # Step 3: Reset the index to convert pivot table into a regular DataFrame
        result_df = pivot_table.reset_index()
        # Step 3: Return the table
        
        # Ensure all column names are strings
        result_df.columns = [str(col) for col in result_df.columns]
        
        # print(result_df)
        return result_df
    @render.plot
    def educationFieldAttritionHistogram():
        df = dat()

        # Step 1: Filter only rows where Attrition is 'Yes'
        attrition_yes = df[df['Attrition'] == 'Yes']

        # Step 2: Group by Education Field and count the number of employees
        education_attrition_counts = attrition_yes.groupby('Education Field').size()

        # Step 3: Plot the horizontal bar chart
        fig = plt.figure(figsize=(10, 6))
        education_attrition_counts.sort_values().plot(
            kind='barh',  # Horizontal bar chart
            color='skyblue',
            edgecolor='black'
        )

        # Step 4: Customize the chart
        plt.title('Education Field-Wise Attrition', fontsize=16)
        plt.xlabel('Number of Employees (Attrition: Yes)', fontsize=14)
        plt.ylabel('Education Field', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        # Return the figure
        return fig
        
    @render.plot
    def under25():
        df = dat()  # Assuming `dat()` returns your DataFrame

        # Step 1: Create Age Bands
        bins = [0, 24, 34, 44, 54, 100]  # Define age ranges
        labels = ["Under 25", "25-34", "35-44", "45-54", "Above 55"]
        df['Age Band'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

        # Step 2: Group Data by Age Band and Gender
        grouped_data = df.groupby(['Age Band', 'Gender']).size().reset_index(name='Count')

        # Step 3: Filter Data for One Age Band (e.g., "25-34")
        age_band = "25-34"
        subset = grouped_data[grouped_data['Age Band'] == age_band]

        # Get Male and Female Counts
        male_count = subset.loc[subset['Gender'] == 'Male', 'Count'].sum() if 'Male' in subset['Gender'].values else 0
        female_count = subset.loc[subset['Gender'] == 'Female', 'Count'].sum() if 'Female' in subset['Gender'].values else 0
        total = male_count + female_count

        # Step 4: Create Donut Chart
        sizes = [male_count, female_count]
        labels = ['Male', 'Female']
        colors = ['#1f77b4', '#ff7f0e']  # Colors for male and female

        fig = plt.figure(figsize=(2 , 2))
        wedges, texts, autotexts = plt.pie(
            sizes, 
            labels=labels, 
            autopct=lambda p: f"{p:.2f}%", 
            startangle=90, 
            colors=colors,
            wedgeprops=dict(width=0.3, edgecolor='w')  # Donut effect
        )

        # Add the total count at the center
        plt.text(0, 0, f"{total}", ha='center', va='center', fontsize=16, fontweight='bold')
        plt.title(f"Attrition Distribution for {age_band}", fontsize=14)
        
        return fig
    
    
    @render.plot
    def under35to44():
        df = dat()  # Assuming `dat()` returns your DataFrame

        # Step 1: Create Age Bands
        bins = [0, 24, 34, 44, 54, 100]  # Define age ranges
        labels = ["Under 25", "25-34", "35-44", "45-54", "Above 55"]
        df['Age Band'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

        # Step 2: Group Data by Age Band and Gender
        grouped_data = df.groupby(['Age Band', 'Gender']).size().reset_index(name='Count')

        # Step 3: Filter Data for One Age Band (e.g., "25-34")
        age_band = "35-44"
        subset = grouped_data[grouped_data['Age Band'] == age_band]

        # Get Male and Female Counts
        male_count = subset.loc[subset['Gender'] == 'Male', 'Count'].sum() if 'Male' in subset['Gender'].values else 0
        female_count = subset.loc[subset['Gender'] == 'Female', 'Count'].sum() if 'Female' in subset['Gender'].values else 0
        total = male_count + female_count

        # Step 4: Create Donut Chart
        sizes = [male_count, female_count]
        labels = ['Male', 'Female']
        colors = ['#1f77b4', '#ff7f0e']  # Colors for male and female

        fig = plt.figure(figsize=(2,2))
        wedges, texts, autotexts = plt.pie(
            sizes, 
            labels=labels, 
            autopct=lambda p: f"{p:.2f}%", 
            startangle=90, 
            colors=colors,
            wedgeprops=dict(width=0.3, edgecolor='w')  # Donut effect
        )

        # Add the total count at the center
        plt.text(0, 0, f"{total}", ha='center', va='center', fontsize=16, fontweight='bold')
        plt.title(f"Attrition Distribution for {age_band}", fontsize=14)
        
        return fig

    # @render.ui
    # def histogram():
    #     # Generate random data
    #     df = np.random.normal(0, 1, input.n_points())
        
    #     return px.histogram(data, x=input.var())

    # @output
    @render_plotly
    def hist():
        n_points = 1000
        if input.distribution() == "Normal":
            data = np.random.normal(0, 1, n_points)
            title = "Normal Distribution"
        else:
            data = np.random.uniform(-3, 3, n_points)
            title = "Uniform Distribution"
            
        # print(data)
        
        return px.histogram(
            x=data,
            title=title,
            labels={"x": "Value", "count": "Count"}
        )
        
    
    @output
    @render_plotly
    def attrition_plot():
        df = dat()
        
        # Filter for attrition cases and count by education field
        attrition_yes = df[df['Attrition'] == 'Yes']
        education_attrition_counts = (attrition_yes.groupby('Education Field')
                                    .size()
                                    .to_frame(name='Count')
                                    .reset_index())
        
        # Create horizontal bar chart using plotly
        fig = px.bar(
            education_attrition_counts,
            x='Count',
            y='Education Field',
            orientation='h',
            title='Education Field-Wise Attrition',
            labels={'Count': 'Number of Employees (Attrition: Yes)',
                   'Education Field': 'Education Field'}
        )
        
        # Customize the layout
        fig.update_layout(
            title_x=0.5,
            title_font_size=16,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            yaxis={'categoryorder': 'total ascending'},  # Sort bars
            showlegend=False,
            xaxis_gridwidth=1,
            xaxis_gridcolor='rgba(0,0,0,0.1)'
        )
        
        return fig
    
    @render_plotly # Changed to render.plotly
    def departmentWiseAttritionPiePlotly():
        df = dat()
        
        department_attrition = df.groupby(['Department', 'Attrition']).size().reset_index(name='Count')
        attrition_yes = department_attrition[department_attrition['Attrition'] == 'Yes']
        
        # Create pie chart using plotly
        fig = px.pie(
            attrition_yes,
            values='Count',
            names='Department',
            title='Department-wise Attrition Distribution'
        )
        
        # Update layout for better appearance
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        return fig
    
    @render_plotly
    def noOfEmployeebyAgeGroupPlotly():
        df = dat()
        
        # Define age groups
        bins = [0, 24, 34, 44, 54, float('inf')]
        labels = ['Under 25', '25 to 34', '35 to 44', '45 to 54', 'Over 55']
        df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
        
        # Create grouped bar chart using plotly
        fig = px.bar(
            df,
            x='Age Group',
            color='Gender',
            title='Employee Distribution by Age Groups and Gender',
            labels={'value': 'Number of Employees', 'Age Group': 'Age Groups'},
            height=600
        )
        
        # Customize the layout
        fig.update_layout(
            xaxis_title='Age Groups',
            yaxis_title='Number of Employees',
            barmode='group',
            legend_title='Gender',
            xaxis={'categoryorder': 'array', 'categoryarray': labels}  # Preserve age group order
        )
        
        
        # 'stack' (currently used) - Bars are stacked on top of each other
        # 'group' - Bars are placed side by side in groups
        # 'overlay' - Bars are overlaid on top of each other with transparency
        # 'relative' - Bars are stacked, with negative values below zero and positive values above zero
        
        return fig
    
    
    @render_plotly
    def age_gender_pie_plotly():
        df = dat()
        
        # Define age groups
        bins = [0, 24, 34, 44, 54, float('inf')]
        labels = ['Under 25', '25 to 34', '35 to 44', '45 to 54', 'Over 55']
        df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
        
        # Filter data for selected age group
        filtered_df = df[df['Age Group'] == input.age_group()]
        
        # Count gender distribution for selected age group
        gender_counts = filtered_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        
        # Create pie chart
        fig = px.pie(
            gender_counts,
            values='Count',
            names='Gender',
            title=f'Gender Distribution for Age Group: {input.age_group()}',
            # color_discrete_sequence=px.colors.qualitative.Set3
            
            # Option 1: Custom hex colors
            # color_discrete_sequence=['#ab02fa', '#66B2FF']
            
            # Option 2: Using Plotly's built-in color sequences
            # color_discrete_sequence=px.colors.qualitative.Set1
            
            # Option 3: Using sequential colors
            # color_discrete_sequence=px.colors.sequential.Viridis
            
            # Using a different qualitative color sequence
            # color_discrete_sequence=px.colors.qualitative.Dark2  # or Set2, Pastel, Dark2, etc.

            # # Or using other Plotly color sequences:
            color_discrete_sequence=px.colors.sequential.Plasma  # or Plasma, Blues, Viridis etc.
        )
        
        # Update layout
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(
            showlegend=True,
            height=500,
            legend_title='Gender'
        )
        
        return fig
        
app = App(app_ui, server)
