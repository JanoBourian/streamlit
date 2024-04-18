"""
# My first app
Here's our first attempt at using data to create a table:
"""
import time
import streamlit as st
import numpy as np
import pandas as pd
from dotenv import dotenv_values
import os
import contextlib
import sys
import logging
import psycopg2
import psycopg2.extras
import matplotlib 
import altair as alt

logging.basicConfig(
    encoding="utf-8",
    format="%(levelname)7s:%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
    force=True,
)
logger = logging.getLogger()

config = {
    **dotenv_values(".env")
}

@contextlib.contextmanager
def create_conn():
    conn_string = "host=%s user=%s password=%s dbname=%s port=%s" % (
        config.get("DB_HOST"),
        config.get("DB_USERNAME"),
        config.get("DB_PASSWORD"),
        config.get("DB_NAME"),
        config.get("DB_PORT"),
    )
    conn = None
    try:
        logger.info("Before connection established")
        conn = psycopg2.connect(conn_string)
        logger.info("Connection established")
        yield conn
        conn.commit()
        logger.warning("SUCCESS: Connection commited")
    except Exception as e:
        _, _, traceback = sys.exc_info()
        if isinstance(conn, psycopg2.extensions.connection):
            conn.rollback()
            logger.error("ERROR: Connection rollbacked")
        error_detail = f"Error: {e.__doc__}\n Line: {traceback.tb_lineno}"
        raise psycopg2.OperationalError(f"ERROR: {error_detail}")
    finally:
        if isinstance(conn, psycopg2.extensions.connection):
            conn.close()
            logger.warning("SUCCESS: Connection closed")
            
def get_dbinfo_fetchall(query: str):
    try:
        data = None
        with create_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query)
                fields = [i[0] for i in cursor.description]
                data = cursor.fetchall()
        return data, fields
    except Exception as e:
        logger.error(f"Failed operation in get_dbinfo_fetchall.\n{e}")
        raise e
    
    
def convert_pd_dataframe(data, columns: list):
    try:
        return pd.DataFrame(
            data,
            columns=columns,
        )
    except Exception as e:
        logger.error(f"Failed operation in convert_pd_dataframe.\n{e}")
        raise e   


data, fields = get_dbinfo_fetchall(config.get("QUERY"))
pandas_df = convert_pd_dataframe(data, fields)
pandas_df = pandas_df.astype(str)
# pandas_df['date'] = pandas_df['date'].strftime("%Y-%m-%d %H:%M:%S")
# print(pandas_df.to_string())
print(pandas_df.describe())
st.dataframe(data = pandas_df)  

chosen = st.radio(
    'Product',
    ("product_1", "product_2"))
if chosen == "product_1":
    st.line_chart(data = pandas_df[pandas_df['name'] == config.get("PRODUCT_1")], x = 'date', y = 'margen')
elif chosen == "product_2":
    st.line_chart(data = pandas_df[pandas_df['name'] == config.get("PRODUCT_2")], x = 'date', y = 'margen')
# st.bar_chart(data = pandas_df.groupby(['name'])) #, x = 'date', y = 'margen')

chart = alt.Chart(pandas_df).mark_line().encode(
    x = alt.X("date"),
    y = alt.Y("margen"), 
    color = alt.Color("name")
)
st.altair_chart(chart, use_container_width=True)

# Use magic
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

# st.table(df)
df

# 
st.write("Hello @janobourian from streamlit")

# Write and dataframe
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))


dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)
st.table(dataframe)

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

#
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

# Draw a line chart
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# Plot a map
@st.cache_data
def map_information():
    map_data = pd.DataFrame(
    # np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    np.random.randn(1000, 2) / [5, 5] + [19.432608, -99.133209],
    columns=['lat', 'lon'])
    
    return map_data

# st.map(map_data)
st.map(map_information())

# Widgets
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.text_input("Your name", key="name")
# You can access the value at any point with:
st.session_state.name

print(st.session_state)
print(dir(st.session_state))

# Use checkboxes to show/hide data
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

# Use a selectbox for options
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

value = st.selectbox(
    'Which number do you prefer?',
     df['second column'])

'You selected: ', option, 'Value: ', value

# Layout
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

# Show progress
'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'

# Stream data, Iterator and Generator
_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""


def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)