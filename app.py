import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def basic_info(df):
    st.header("FULL DATA")
    st.dataframe(df)

def data_schema(df):
    st.header("DATA SCHEMA")
    st.info(f"RECORD : ")
    st.text(len(df))
    st.info(f"SIZE OF DATA(ROW,COLUMN) :")
    st.text(df.shape)
    st.info("COLUMNS TYPE :")
    st.dataframe(df.dtypes)
    st.info("MISSING VALUES :")
    st.dataframe(df.isnull().sum())
    st.info(f"Duplicate rows found: {df.duplicated().sum()}")

def statistics(df):
    st.header("STATISTICS")
    st.write(df.describe())

def missing_values(df): 
    st.header("MISSING VALUES")
    st.info("TICK represents missing value")
    st.write(df.isnull())

def visualization(df):
    st.header("VISUALIZATION")
    numeric_col=df.select_dtypes(include='number').columns.tolist()
    category_col=df.select_dtypes(include='object').columns.tolist()
    if not numeric_col or not category_col:
        st.warning("Need a numerical and category column both")
        return
    else:
        selected_num= st.selectbox("Select Numeric Column", numeric_col)
        selected_cat= st.selectbox("Select category Column", category_col)
        chart_data=df.groupby(selected_cat)[selected_num].sum()
        graph_type=st.selectbox("Select which chart type you want", ['Bar chart', 'Pie chart', 'Line chart','Histogram'])

        if graph_type=='Bar chart':
            fig, ax = plt.subplots()
            chart_data.plot(kind="bar", ax=ax)
            st.pyplot(fig)
        elif graph_type=='Pie chart':
            fig, ax = plt.subplots()
            chart_data.plot(kind="pie", ax=ax, autopct="%1.1f%%")
            st.pyplot(fig)
        elif graph_type=='Line chart':
            fig, ax = plt.subplots()
            chart_data.plot(kind="line", ax=ax, marker="o")
            st.pyplot(fig)
        elif graph_type=='Histogram':
            fig, ax = plt.subplots()
            df[selected_num].plot(kind="hist", ax=ax)
            st.pyplot(fig)

def corr_matrix(df):
    st.header("CORRELATION MATRIX")
    numerical_df=df.select_dtypes(include="number")
    if len(numerical_df.columns)<2:
        st.warning("Need atleast 2 numeric columns for correlation")
    else:
        corr=numerical_df.corr()
        fig,ax=plt.subplots()
        sns.heatmap(corr,annot=True,cmap='coolwarm',ax=ax)
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)

def main():
    st.title("INTERACTIVE EDA TOOL")
    st.header("Upload File")
    uploaded_file=st.file_uploader("Upload your CSV file",type=["csv"])
    if uploaded_file is None:
        st.warning("No file uploaded yet!")
    else:
        df=pd.read_csv(uploaded_file)
        st.sidebar.title("EDA MENU")
        st.sidebar.markdown("---")
        options=[" ","DATA VIEW","SUMMARY STATISTICS","DATA SCHEMA", "MISSING VALUES","VISUALIZATION", "CORRELATION MATRIX"]
        page=st.sidebar.selectbox("SELECT OPTIONS", options)

        if page=="DATA VIEW":
            basic_info(df)
        elif page=="SUMMARY STATISTICS":
            statistics(df)
        elif page=="DATA SCHEMA":
            data_schema(df)
        elif page=="MISSING VALUES":
            missing_values(df)
        elif page=="VISUALIZATION":
            visualization(df)
        elif page=="CORRELATION MATRIX":
            corr_matrix(df)


main()