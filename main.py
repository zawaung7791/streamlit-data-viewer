from pickle import FALSE
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.title("Streamlit Data Previewer")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Data Profile", "Histogram", "Boxplot","Correlation Heatmap", "Scatter Plot", "Tree Map"])

# create sidebar
st.sidebar.title("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['csv', 'xlsx'])
st.sidebar.text("By Zaw Aung 2024")

with tab1:
    st.header("Data Profile")

    # If the file is uploaded, show the file name
    if uploaded_file is not None:
        try:
            # Handle if csv or excel file loaded
            if uploaded_file.name.endswith('.xlsx'):
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                sheet = st.selectbox("Select the Excel sheet", sheet_names)
                df = pd.read_excel(uploaded_file, sheet_name=sheet)
            else:
                df = pd.read_csv(uploaded_file)

            numeric_df = df.select_dtypes(include=['number'])
            category_df = df.select_dtypes(include=['object', 'datetime'])

            # A label, "Data profile"
            st.text("Data shape")
            st.write(df.shape)

            # Display the dataframe
            st.text("Data preview")
            st.write(df.head())

            # Display the data types
            st.text("Summary stats")
            st.write(df.describe())

            # Display dataframe info
            st.text("Dataframe Info")
            info_df = pd.DataFrame({
                "Datatype": df.dtypes,
                "Count": df.count(),
                "Distinct Count": df.nunique(),
                "Null Values": df.isnull().sum(),
                "Blanks": (df == '').sum()
            })
            st.write(info_df)

        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()
    else:
        st.write("No file uploaded yet.")

with tab2:
    if uploaded_file is not None:
        st.header("Histogram")
        # Select variable for histogram
        column = st.selectbox("Select a numeric column for histogram", numeric_df.columns)
        if column:
            st.text(f"Histogram for {column}")
            fig = px.histogram(numeric_df, x=column, marginal="violin", nbins=30, text_auto=True)
            st.plotly_chart(fig)
        else:
            st.write("No suitable columns available for histogram.")
    else:
        st.write("No data loaded for histogram.")

with tab3:
    if uploaded_file is not None:
        st.header("Boxplot")
        # Select variable for boxplot
        column = st.selectbox("Select a numeric column for boxplot", numeric_df.columns)
        if column:
            st.text(f"Boxplot for {column}")
            fig = px.box(numeric_df, y=column, points='all')
            fig.update_traces(boxpoints='all', jitter=0.3, pointpos=-1.8)
            st.plotly_chart(fig)
        else:
            st.write("No suitable columns available for boxplot.")
    else:
        st.write("No data loaded for boxplot.")
    

with tab4:
    if uploaded_file is not None:
        st.header("Correlation Heatmap")
        # Plotting correlation heatmap for numeric data
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, cmap='coolwarm', ax=ax)
            # show correlation values in heatmap
            for (i, j), val in np.ndenumerate(corr):
                ax.text(j + 0.5, i + 0.5, f"{val:.2f}", ha='center', va='center', color='black')
            

            

            st.pyplot(fig)
        else:
            st.write("No numeric columns available for correlation heatmap.")
    else:
        st.write("No data loaded for correlation heatmap.")

with tab5:
    if uploaded_file is not None:
        st.header("Scatter Plot")
        # Select variables for scatter plot
        x_column = st.selectbox("Select X-axis column for scatter plot", numeric_df.columns)
        y_column = st.selectbox("Select Y-axis column for scatter plot", numeric_df.columns)
        add_regression = st.checkbox("Add regression line")
        if x_column and y_column:
            st.text(f"Scatter plot for {x_column} vs {y_column}")
            fig = px.scatter(numeric_df, x=x_column, y=y_column, trendline="ols" if add_regression else None)
            st.plotly_chart(fig)
        else:
            st.write("No suitable columns available for scatter plot.")
    else:
        st.write("No data loaded for scatter plot.")

with tab6:
    if uploaded_file is not None:
        st.header("Treemap")
        # Select variables for treemap
        category_column = st.selectbox("Select a categorical column for treemap", category_df.columns)
        value_column = st.selectbox("Select a numeric column for treemap values", numeric_df.columns)
        if category_column and value_column:
            st.text(f"Treemap for {category_column} with values from {value_column}")
            fig = px.treemap(df, path=[category_column], values=value_column)
            fig.update_traces(textinfo="label+value")
            st.plotly_chart(fig)
        else:
            st.write("No suitable columns available for tree map.")
    else:
        st.write("No data loaded for pie chart.")