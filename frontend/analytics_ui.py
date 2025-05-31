import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt




API_URL = "http://localhost:8000"

def get_payload(key_start, key_end):
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2025, 1, 1), key=key_start)
    with col2:
        end_date = st.date_input("End Date", datetime.today(), key=key_end)

    payload = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }
    return payload

def analytics_stacked_tab():
    payload = get_payload("start_date_key_alpha", "end_date_key_alpha")
    response_stacked = requests.post(f"{API_URL}/analytics/stack", json=payload)
    response_stacked = response_stacked.json()

    months = list(response_stacked.keys())
    data_stacked = {"Month": months}

    categories = response_stacked[months[0]].keys()  # Extract unique category names
    for category in categories:
        data_stacked[category] = [response_stacked[month].get(category, 0) for month in data_stacked["Month"]]

    df_stacked = pd.DataFrame(data_stacked)

    # Convert DataFrame to long format
    df_long = df_stacked.melt(id_vars=['Month'], var_name='Category', value_name='Total($)')

    # Create the stacked bar chart
    chart = alt.Chart(df_long).mark_bar().encode(
        x='Month:N',
        y='Total($):Q',
        color='Category:N',
        order = alt.Order("Total($):Q", sort="descending")
    ).properties(title="Expense Breakdown by Month")

    # Display in Streamlit
    st.altair_chart(chart, use_container_width=True)

    #Table dataframe formatting and table display
    df_stacked_sort = df_stacked.sort_values("Month")
    df_stacked_sort["Month"] = pd.to_datetime(df_stacked["Month"]).dt.strftime("%B %Y")
    df_stacked_sort["Total"] = df_stacked_sort.loc[:, df_stacked_sort.columns != "Month"].sum(axis=1)
    numeric_cols = df_stacked_sort.select_dtypes(include=np.number).columns
    df_stacked_sort[numeric_cols] = df_stacked_sort[numeric_cols].map("{:,.2f}".format)
    st.table(df_stacked_sort)


def analytics_donut_tab():
    payload = get_payload("start_date_key_beta", "end_date_key_beta")
    response_donut = requests.post(f"{API_URL}/analytics/", json=payload)
    response_donut = response_donut.json()
    data = {
        "Category": list(response_donut.keys()),
        "Total": [response_donut[category]["total"] for category in response_donut],
        "Percentage": [response_donut[category]["percentage"] for category in response_donut]
    }
    df_donut = pd.DataFrame(data)
    donut_chart = px.pie(df_donut, values='Percentage', names='Category', hole=0.6,
                         title='Expense Breakdown by Category')
    st.plotly_chart(donut_chart)

    df_sorted = df_donut.sort_values(by="Percentage", ascending=False)

    df_sorted["Total"] = df_sorted["Total"].map("{:,.2f}".format)
    df_sorted['Percentage'] = df_sorted["Percentage"].map("{:.1f}".format)

    st.table(df_sorted)
