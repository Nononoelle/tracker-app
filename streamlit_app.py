import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

# 1. set a title
st.title("Key Role Tracker")

# 2. load data
@st.cache_data
def load_data():
    df_main = pd.read_excel('Tracker_dataset.xlsx')

    return df_main


# 3. save file
def save_file():
    df.to_excel('/Users/jiewu/Documents/Streamlit/Tracker/Tracker_dataset_new.xlsx', index=False)

# 4. page layout
## Left sidebar
st.sidebar.header("Upload File")
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

## right container
st.write('<div class="table-container">', unsafe_allow_html=True)
with st.container():
    if uploaded_file is not None:
        try:
            df_upload = pd.read_excel(uploaded_file)
            df_upload["Employee ID"] = df_upload["Employee ID"].str.capitalize()
            df_upload = df_upload[["Employee ID", "New Key Role"]]
            df_main = load_data()
            df = pd.merge(df_main, df_upload, on="Employee ID", how="left")
            for i in df_upload["Employee ID"]:
                df.loc[df["Employee ID"]==i, "Key Role"] = df.loc[df["Employee ID"]==i, "New Key Role"]
                df.loc[df["Employee ID"]==i, "Last Modified Date"] = datetime.now()

            df = df.drop("New Key Role", axis=1)
            df_show = df.copy()

            unique_countries = ["All"] + list(df_show["Country"].unique())
            unique_eid = ["All"] + list(df_show["Employee ID"].unique())

            st.sidebar.subheader("Select a Country")
            selected_country = st.sidebar.selectbox("Select a country", unique_countries)

            st.sidebar.subheader("Select an Employee ID")
            selected_eid = st.sidebar.selectbox("Select an Employee ID", unique_eid)

            # filter and display the data based on the selected filters
            if selected_country == "All" and selected_eid == "All":
                filtered_data = df_show
            elif selected_country == "All":
                filtered_data = df_show[df_show["Employee ID"]==selected_eid]
            elif selected_eid == "All":
                filtered_data = df_show[df_show["Country"]==selected_country]
            else:
                filtered_data = df_show[(df_show["Country"]==selected_country) & (df_show[df_show["Employee ID"]==selected_eid])]

            if st.checkbox("Show the result"):
                st.write(filtered_data)

            # save button
            button_clicked = st.button("Save", key="save_file")
            button_executed = False

            if button_clicked:
                save_file()
                button_executed = True

            if button_executed:
                st.write("The File has been updated and saved")
            # bar chart on key role
            st.subheader("Key Role Distribution")
            category_columns = ["Country", "Business Line", "Department"]
            chart_category_columns = st.selectbox("Select a column for classification", category_columns)

            grouped_data = filtered_data.groupby(chart_category_columns)["Key Role"].count()

            st.bar_chart(grouped_data)

        except Exception as e:
            if str(e) == "buffer source array is ready-only":
                empty_df = pd.DataFrame()
                st.table(empty_df)
            else:
                st.error(f"An error occurred: {e}")


st.write('</div>', unsafe_allow_html=True)
