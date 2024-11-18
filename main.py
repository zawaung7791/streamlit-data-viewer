import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Streamlit Test 1")     

left_column, right_column = st.columns([1,1])

with left_column:

    st.header("File")   

    # a button to upload the file, excel or csv
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])

    # if the file is uploaded, show the file name
    if uploaded_file is not None:
        # st.write(uploaded_file.name + " has been uploaded.")   
        
        df = pd.read_csv(uploaded_file)

        # a label, "Data shape"
        st.text("Data profile")
        st.write(df.shape)
        st.write(df.describe())
        st.text("DataFrame")
        st.dataframe(df)

        # save the dataframe in session state
        st.session_state['df'] = df
        numeric_df = df.select_dtypes(include=['number'])


with right_column:

    st.header("Graphs")

    if uploaded_file is not None:
        # a st dropdown to select the column
        column = st.selectbox("Select a column for histogram", numeric_df.columns)
        fig = px.histogram(df, x=column)
        st.plotly_chart(fig)

        # draw a box plot of only the numeric columns
        st.text("Box Plot")
        column2 = st.selectbox("Select a column for box plot", numeric_df.columns)
        fig = px.box(df, y=column2)
        st.plotly_chart(fig)

        # draw a heatmap of only the numeric columns
        st.text("Correlation Heatmap")
        fig = px.imshow(numeric_df.corr())
        st.plotly_chart(fig)

        # draw a scatter plot of only the numeric columns
        # allow the user to select the x and y columns
        # show regression, the r squared value, p value and equation of the line
        st.text("Scatter Plot")
        x_column = st.selectbox("Select x column", numeric_df.columns)
        y_column = st.selectbox("Select y column", numeric_df.columns)
        add_regression = st.checkbox("Add regression line")
        fig = px.scatter(df, x=x_column, y=y_column, trendline="ols" if add_regression else None)
        st.plotly_chart(fig)

    else:
        st.write("Please upload a file.")