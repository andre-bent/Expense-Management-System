import streamlit as st
from analytics_ui import analytics_stacked_tab
from analytics_ui import analytics_donut_tab
from add_update_ui import add_update_tab
from add_update_ui import view_expenses_tab

#Page browser title and tab icon setup
st.set_page_config(
    page_title="Expense Tracking System",
    page_icon = "📊"
)

#Homepage title
st.title("Expense Tracking System")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Add/Update Expenses",
     "View Expenses",
     "Expense Breakdown by Month",
     "Expense Breakdown By Category"]
)

with tab1:
    add_update_tab()
with tab2:
    view_expenses_tab()
with tab3:
    analytics_stacked_tab()
with tab4:
    analytics_donut_tab()

