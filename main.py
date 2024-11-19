import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Streamlit Data Previewer")
st.header("File")

# A button to upload the file, excel or csv
uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])

# If the file is uploaded, show the file name
if uploaded_file is not None:
    try:
        # Handle if csv or excel file loaded
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    numeric_df = df.select_dtypes(include=['number'])
    category_df = df.select_dtypes(include=['object'])

    col1, col2 = st.columns(2)

    with col1:
        # A label, "Data profile"
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
        # Display a histogram
        st.text("Histogram")
        if not numeric_df.empty:
            column1 = st.selectbox("Select a column for histogram", numeric_df.columns)
            fig = px.histogram(df, x=column1)
            st.plotly_chart(fig)
        else:
            st.warning("No numeric columns available for histogram.")

        # Display a box plot
        st.text("Box Plot")
        if not numeric_df.empty:
            column2 = st.selectbox("Select a column for box plot", numeric_df.columns)
            fig = px.box(df, y=column2)
            st.plotly_chart(fig)
        else:
            st.warning("No numeric columns available for box plot.")

        # Display a correlation heatmap
        st.text("Correlation Heatmap")
        if not numeric_df.empty:
            fig = px.imshow(numeric_df.corr())
            st.plotly_chart(fig)
        else:
            st.warning("No numeric columns available for correlation heatmap.")

        # Display a scatter plot
        st.text("Scatter Plot")
        if len(numeric_df.columns) > 1:
            x_column = st.selectbox("Select x column", numeric_df.columns)
            y_column = st.selectbox("Select y column", numeric_df.columns)
            add_regression = st.checkbox("Add regression line")
            fig = px.scatter(df, x=x_column, y=y_column, trendline="ols" if add_regression else None)
            st.plotly_chart(fig)
        else:
            st.warning("Not enough numeric columns available for scatter plot.")

        # Display a pie chart
        st.text("Pie Chart")
        if not category_df.empty and not numeric_df.empty:
            category_column = st.selectbox("Select category column", category_df.columns)
            value_column = st.selectbox("Select value column", numeric_df.columns)
            fig = px.pie(df, names=category_column, values=value_column)
            st.plotly_chart(fig)
        else:
            st.warning("No suitable columns available for pie chart.")


