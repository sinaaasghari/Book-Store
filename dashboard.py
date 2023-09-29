import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import random
import plotly.express as px

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='13771377Mnn@',
    database='book_store'
)

cursor = conn.cursor()
#color
color =[
            "#4477dd",
            "#00a67e",
            "#8ffe09",
            "#c90b42",
            "#ffaa0088"
            ]


st.title('BOOK STORE')

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

with tab1:
    col1, col2 = st.columns([1, 3])

    with col1:
        type=st.radio(
            "Analytical charts",
            key="Analytical charts",
            options=["count tag", "count publisher", "count year"],
        )
    with col2:
        # First part: Analytical charts
        if type == "count tag":
            # plot question 1
            st.header('count tag book')
            number = st.number_input('Choose number', step=1,value=20,min_value=5)
            cursor.execute(f"select name,count(*) as count_book from group_category \
                        inner join category c on group_category.category_id = c.id\
                                group by name order by count_book desc limit {number}")
            result = cursor.fetchall()
            df = pd.DataFrame(
                    result,
                        columns=("name","count_book"))
            ###
            st.title('bar chart')
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('name', title="دسته بندی ها"),
                y=alt.Y('count_book', title="تعداد کتاب ها"),
                color=alt.ColorValue(random.choice(color))
            ).properties(
                width=500,
                height=300
            )

            st.altair_chart(chart, use_container_width=True)
            ###
            st.title('Pie chart')
            fig = px.pie(df, values='count_book', names='name')

            st.plotly_chart(fig, use_container_width=True)
        elif type == "count publisher":
            # plot question 2
            st.header('count publisher book')
            cursor.execute(f"select name,count(*) as count_book from book_publisher \
                           inner join publisher p on book_publisher.publisher_id = p.id \
                            group by publisher_id order by count_book desc limit 10")
            result = cursor.fetchall()
            df = pd.DataFrame(
                    result,
                        columns=("name","count_book"))
            ###
            st.title('bar chart')
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('name', title=" انتشارات "),
                y=alt.Y('count_book', title="تعداد کتاب ها"),
                color=alt.ColorValue(random.choice(color))
            ).properties(
                width=500,
                height=300
            )

            st.altair_chart(chart, use_container_width=True)
            ###
            st.title('Pie chart')
            fig = px.pie(df, values='count_book', names='name')

            st.plotly_chart(fig, use_container_width=True)    
        if type == "count year":
            # plot question 1
            st.header('count year book')
            
            release_year = st.selectbox(
                'release year',
                ('miladi', 'shamsi'))

            st.write('You selected:', release_year)
            if release_year=="miladi":
                release_year ="release_year_mi"
                start_year = 1980
                end_year = 2030
                end_count = 300
            else:
                release_year ="release_year_sh"
                start_year = 1370
                end_year = 1405
                end_count = 1000

            number = st.number_input('Choose number', step=1,value=10,min_value=5,max_value =30)
            cursor.execute(f"select {release_year},count(*) as count_book from book group by \
                            {release_year} order by count_book desc limit {number}")
            result = cursor.fetchall()
            df = pd.DataFrame(
                    result,
                        columns=(f"{release_year}","count_book"))
            df.dropna(subset=[f"{release_year}"],inplace=True)
            print(df)
            ###
            st.title('bar chart')
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(f'{release_year}', title="سال انتشار",
                        scale=alt.Scale(domain=(start_year, end_year)),
                        axis=alt.Axis(tickCount=4)),
                y=alt.Y('count_book', title="تعداد کتاب ها",
                        scale=alt.Scale(domain=(0, end_count))),
                color=alt.ColorValue(random.choice(color))
            ).properties(
                width=500,
                height=300
            )

            st.altair_chart(chart, use_container_width=True)
            ###
            st.title('Pie chart')
            fig = px.pie(df, values='count_book', names=f'{release_year}')

            st.plotly_chart(fig, use_container_width=True)