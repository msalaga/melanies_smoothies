# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())

insert_btn = st.button("Submit Order")
#fv_df = st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

options = st.multiselect(
    "Choose smoothies",
    my_dataframe)

    
if(insert_btn):
    if options:
        concatenated_string = ''

    for option in options:
        concatenated_string += option + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ option)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients) values ('""" + concatenated_string + """')"""
    if concatenated_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
