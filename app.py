import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_sales_data.csv')
    df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'cleaned_sales_data.csv' not found. Please ensure the file is in the same folder as this script.")
    st.stop()

st.sidebar.header("🔍 Filter Options")

region = st.sidebar.multiselect("Region:", options=df["Region"].unique(), default=df["Region"].unique())
sales_rep = st.sidebar.multiselect("Sales Rep:", options=df["Sales_Rep"].unique(), default=df["Sales_Rep"].unique())
category = st.sidebar.multiselect("Category:", options=df["Product_Category"].unique(), default=df["Product_Category"].unique())
cust_type = st.sidebar.multiselect("Customer Type:", options=df["Customer_Type"].unique(), default=df["Customer_Type"].unique())
payment = st.sidebar.multiselect("Payment Method:", options=df["Payment_Method"].unique(), default=df["Payment_Method"].unique())
channel = st.sidebar.multiselect("Sales Channel:", options=df["Sales_Channel"].unique(), default=df["Sales_Channel"].unique())

df_selection = df.query(
    "Region == @region & Sales_Rep == @sales_rep & Product_Category == @category & "
    "Customer_Type == @cust_type & Payment_Method == @payment & Sales_Channel == @channel"
)

st.title("📊 Sales Dashboard (Native Charts)")
st.markdown("---")

total_sales = df_selection["Sales_Amount"].sum()
st.metric(label="Total Sales Amount", value=f"${total_sales:,.2f}")

st.subheader("📈 Sales Over Time")
line_data = df_selection.groupby("Sale_Date")["Sales_Amount"].sum()
st.line_chart(line_data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product Category")
    cat_data = df_selection.groupby("Product_Category")["Sales_Amount"].sum().sort_values(ascending=False)
    st.bar_chart(cat_data)

with col2:
    st.subheader("Sales by Region")
    region_data = df_selection.groupby("Region")["Sales_Amount"].sum().sort_values(ascending=False)
    st.bar_chart(region_data)

with st.expander("View Filtered Raw Data"):
    st.write(df_selection)