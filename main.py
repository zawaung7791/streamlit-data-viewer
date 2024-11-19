import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Quick Data Previewer")     

st.header("File")   

# a button to upload the file, excel or csv
uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])

# if the file is uploaded, show the file name
if uploaded_file is not None:
    # st.write(uploaded_file.name + " has been uploaded.")   
    
    # handle if csv or excel file loaded

    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)   
    else:
        df = pd.read_csv(uploaded_file)

    numeric_df = df.select_dtypes(include=['number'])

    category_df = df.select_dtypes(include=['object'])

    col1, col2 = st.columns(2)

    with col1:
        # a label, "Data profile"
        st.text("Data profile")
        st.write(df.shape)

        # Display the dataframe
        st.text("Data preview")
        st.write(df.head())

        # Display the data types
        st.text("Summary stats")
        st.write(df.describe())

        # Display the numerical columns
        st.text("Numerical columns")
        st.table([numeric_df.columns, numeric_df.dtypes])

        # Display the categorical columns
        st.text("Categorical columns")
        st.table([category_df.columns, category_df.dtypes])


    with col2:

        # display a histogram
        st.text("Histogram")
        column1 = st.selectbox("Select a column for histogram", df.select_dtypes(include=['float64', 'int64']).columns)
        fig = px.histogram(df, x=column1)
        st.plotly_chart(fig)

        # Display a box plot
        st.text("Box Plot")
        column2 = st.selectbox("Select a column for box plot", df.select_dtypes(include=['float64', 'int64']).columns)
        fig = px.box(df, y=column2)
        st.plotly_chart(fig)

        # Display a correlation heatmap
        st.text("Correlation Heatmap")
        fig = px.imshow(numeric_df.corr())
        st.plotly_chart(fig)

        # Display a scatter plot
        st.text("Scatter Plot")
        x_column = st.selectbox("Select x column", df.select_dtypes(include=['float64', 'int64']).columns)
        y_column = st.selectbox("Select y column", df.select_dtypes(include=['float64', 'int64']).columns)
        add_regression = st.checkbox("Add regression line")
        fig = px.scatter(df, x=x_column, y=y_column, trendline="ols" if add_regression else None)
        st.plotly_chart(fig)

        # Display a pie chart
        st.text("Pie Chart")
        category_column = st.selectbox("Select category column", df.select_dtypes(include=['object']).columns)
        value_column = st.selectbox("Select value column", df.select_dtypes(include=['float64', 'int64']).columns)
        fig = px.pie(df, names=category_column, values=value_column)
        st.plotly_chart(fig)
