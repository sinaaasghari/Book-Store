import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns
import random
import plotly.express as px
import numpy as np
import matplotlib.font_manager as fm
# font_path = 'D:\quera\Far_Nazanin.ttf'
# fm.fontManager.addfont(font_path)

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

tab1, tab2 ,tab3 = st.tabs(["📈 Analytical Chart", "🗃 filter book","📈 Analytical Chart Extra"])

with tab1:
    col1, col2 = st.columns([1, 3])

    with col1:
        type=st.radio(
            "Analytical charts",
            key="Analytical charts",
            options=["count tag", "count publisher", "count year","count writer","count translator",
                    "Page vs Year" , "Price vs Year" , "Price vs Rate" ,"count ghate"])
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
        elif type == "count year":
            # plot question 3
            st.header('count year book')
            
            release_year = st.selectbox(
                'release year',
                ('miladi', 'shamsi'))

            st.write('You selected:', release_year)
            if release_year=="miladi":
                release_year ="release_year_mi"
                start_year = 1950
                end_year = 2030
                end_count = 10000
            else:
                release_year ="release_year_sh"
                start_year = 1370
                end_year = 1405
                end_count = 30000

            number = st.number_input('Choose number', step=1,value=10,min_value=5,max_value =30)
            cursor.execute(f"select {release_year},count(*) as count_book from book group by \
                            {release_year} order by count_book desc limit {number}")
            result = cursor.fetchall()
            df = pd.DataFrame(
                    result,
                        columns=(f"{release_year}","count_book"))
            df.dropna(subset=[f"{release_year}"],inplace=True)
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
        elif type == "count writer":
            # plot question 4
            st.header('count writer book')
            cursor.execute(f"select name , count(*) as book_code from crew \
                           inner join person p on crew.person_counter = p.counter\
                               where role ='writer'group by name \
                               order by book_code desc limit 10")
            result = cursor.fetchall()
            df = pd.DataFrame(
                    result,
                        columns=("name","count_book"))
            ###
            st.title('bar chart')
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('name', title=" نویسندگان "),
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
        elif type == "count translator":
            # plot question 5
            st.header('count translator book')
            cursor.execute(f"select name , count(*) as book_code from crew \
                           inner join person p on crew.person_counter = p.counter\
                               where role ='translator'group by name \
                               order by book_code desc limit 10")
            result = cursor.fetchall()
            df = pd.DataFrame(
                    result,
                        columns=("name","count_book"))
            ###
            st.title('bar chart')
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('name', title=" مترجمان "),
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
        # plot question 6
        elif type == "Page vs Year":
            st.header('Relationship between the :blue[number of pages] and the :blue[year of publication]')
            cursor.execute(f"select release_year_sh  as Year, AVG(page_count) as Count from book \
                               group by release_year_sh")
            result = cursor.fetchall() 
            df = pd.DataFrame(
                    result,
                        columns=("Year","Count"))
            
            st.title('scatter chart')
            # plot
            mean_height = df['Count'].mean()
            scatter_plot = sns.scatterplot(data=df, x='Year', y='Count')
            plt.axhline(mean_height, color='red', label = 'Average' , alpha=0.5)
            scatter_plot.set_xlabel('Year', fontname='Times New Roman', fontsize=14)
            scatter_plot.set_ylabel('Price', fontname='Times New Roman', fontsize=14)
            plt.xticks(fontname='Times New Roman')
            plt.yticks(fontname='Times New Roman')
            sns.despine()
            plt.xlim(1360,1403)
            plt.legend()
            st.pyplot(scatter_plot.figure)
            
        
        # plot question 7
        elif type == "Price vs Year":
            st.header('Relationship between the :blue[Price] and the :blue[year of publication]')
            cursor.execute(f"select release_year_sh  as Year, AVG(price) as Price from book \
                               group by release_year_sh")
            result = cursor.fetchall() 
            df = pd.DataFrame(
                    result,
                        columns=("Year","Price"))
            # plot
            st.title('scatter chart')
            mean_height = df['Price'].mean()
            scatter_plot = sns.scatterplot(data=df, x='Year', y='Price')
            plt.axhline(mean_height, color='red', label = 'Average' , alpha=0.5)
            scatter_plot.set_xlabel('Year', fontname='Times New Roman', fontsize=14)
            scatter_plot.set_ylabel('Price', fontname='Times New Roman', fontsize=14)
            plt.xticks(fontname='Times New Roman')
            plt.yticks(fontname='Times New Roman')
            sns.despine()
            plt.xlim(1360,1403)
            plt.legend()
            st.pyplot(scatter_plot.figure)
            
        # plot question 8 
        elif type == "Price vs Rate":
            st.header('Relationship between the :blue[Price] and the :blue[Rate]')
            cursor.execute(f"select grade  as Rate, AVG(price) as Price from book \
                               group by Rate")
            result = cursor.fetchall() 
            df = pd.DataFrame(
                    result,
                        columns=("Rate","Price"))
            # plot
            mean_height = df['Price'].mean()
            scatter_plot = sns.scatterplot(data=df, x='Rate', y='Price')
            plt.axhline(mean_height, color='red', label = 'Average')
            plt.xticks([2.0,3.0,4.0,5.0])
            scatter_plot.set_xlabel('Rate', fontname='Times New Roman', fontsize=14)
            scatter_plot.set_ylabel('Price', fontname='Times New Roman', fontsize=14)
            plt.xticks(fontname='Times New Roman')
            plt.yticks(fontname='Times New Roman')
            sns.despine()
            plt.legend()
            st.pyplot(scatter_plot.figure)
        
        # plot question 9
        elif type == "count ghate":
            cursor.execute(f"select ghate , count(*) as quantity from book\
                           where ghate is not NULL and ghate != 'وزیریباکاغذمعطر'\
                           group by ghate\
                           order by quantity DESC;")
            result = cursor.fetchall() 
            df = pd.DataFrame(
                    result,
                        columns=("Ghate","Quantity"))
            name_list = list(df['Ghate'])
            
            #plot
            st.title('bar chart')
            chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                x=alt.X('Quantity', title=" تعداد"),
                y=alt.Y('Ghate', title="نوع قطع ", sort=name_list)).properties(
                width=600,
                height=400).configure_axis(
                labelFontSize=16,
                titleFontSize=16)
            st.altair_chart(chart, use_container_width=True)
with tab2:
    text_search = st.text_input('text to search')
    fields_book = st.multiselect(
    'search fields',
    ['عنوان فارسی', 'عنوان انگلیسی', 'نویسنده', 'مترجم'],
    ['عنوان فارسی'])
    change_persion_to_English ={'title_persian':'عنوان فارسی','title_english': 'عنوان انگلیسی',
                                'person_writer':'نویسنده','person_translator': 'مترجم',
                                }
    ## slider 
    st.text('search shamsi date:')
    values_shamsi = st.slider('Select a range of date shamsi',1380, 1390, (1350,1410),step=1)
    st.text('search miladi date:')
    values_miladi = st.slider('Select a range of date miladi',1950, 2030, (1950,2030),step=1)
    st.text('search price:')
    price = st.slider('Select a range of price',1000, 1000000, (1000,1000000),step=1000)
    ## select box
    #publisher
    cursor.execute("select name from publisher")
    publisher = cursor.fetchall()
    options_publisher =["انتشارات همه"]+[f"{i[0]}" for i in publisher] 
    selected_publisher = st.selectbox("Select an publisher", options_publisher)
    #cover
    cursor.execute("select cover from book group by cover")
    cover = cursor.fetchall()
    options_cover =["همه جلدها"]+[f"{i[0]}" for i in cover] 
    selected_cover = st.selectbox("Select an cover", options_cover)
    #ghate
    cursor.execute("select ghate from book group by ghate")
    ghate = cursor.fetchall()
    options_ghate =["همه قطع"]+[f"{i[0]}" for i in ghate] 
    selected_ghate = st.selectbox("Select an ghate", options_ghate)
    if fields_book ==[]:
        list_search ={'title_persian':'عنوان فارسی','title_english': 'عنوان انگلیسی',
                            'release_year_mi':'سال انتشار میلادی','release_year_sh':'سال انتشار شمسی',
                            'person_writer':'نویسنده','person_translator': 'مترجم',
                            'p.name':'ناشر','cover':'نوع جلد',
                            'ghate':'قطع'}
    else:
        list_search ={}
        for field in fields_book:
            for k, v in change_persion_to_English.items():
                if field == v:
                    list_search[k] = field
    # search all
    base_query =f"SELECT code,title_persian,title_english,price,release_year_sh,release_year_mi,\
            cover,ghate,p.name as publisher,p2.name as person,role\
            FROM book inner join book_publisher bp on book.code = bp.book_code\
            inner join publisher p on bp.publisher_id = p.id\
            inner join  crew c on book.code = c.book_code\
            inner join  person p2 on c.person_counter = p2.counter WHERE release_year_sh BETWEEN {int(values_shamsi[0])} AND {int(values_shamsi[1])} and \
                release_year_mi BETWEEN {int(values_miladi[0])} AND {int(values_miladi[1])} and \
                price BETWEEN {int(price[0])} AND {int(price[1])} and "
    # search box query
    if selected_publisher !="انتشارات همه":
        base_query = base_query + f" p.name = '{selected_publisher}' and "
    if selected_cover != 'همه جلدها':
        base_query = base_query + f" cover = '{selected_cover}' and "
    if selected_ghate != 'همه قطع':
        base_query = base_query + f" ghate = '{selected_ghate}' and "    
    i = 0
    where_query = " "
    for k, v in list_search.items():
        i= i + 1
        if k == "person_translator":
            where_query = " " + where_query +f" p2.name LIKE '%{text_search}%' "+" "+ "and"+" "                
            where_query = " " + where_query +f"role = 'translator'" +" "               
        elif k == "person_writer":
            where_query = " " + where_query +f" p2.name LIKE '%{text_search}%' "+" "+ "and"+" "                
            where_query = " " + where_query +f"role = 'writer'" +" "
        else:
            where_query = " " + where_query +f" {k} LIKE '%{text_search}%' "                
        if len(list_search) != i: 
            where_query = where_query +" "+ "and"+" "
    query = base_query +where_query
    st.header('filter book')
    cursor.execute(query+""+"limit 20")
    result = cursor.fetchall()
    df = pd.DataFrame(
            result,
                columns=("code","title_persian","title_english","price",
                        "release_year_sh","release_year_mi",
                        "cover","ghate","publisher",
                        "person","role"))
    st.table(df)
            
with tab3:
    col1, col2 = st.columns([1, 3])
    
    with col1:
                type=st.selectbox(
                    "Analytical charts",
                    key="Analytical charts_part3",
                    options=["1. The most expensive publisher","2. The most active publishers",
                             "3. variety of Writers VS Grade" , "4. variety of Publish VS Grade"])
    with col2:
                if type == "1. The most expensive publisher":
                    # plot question 1
                    cursor.execute(f"Select name as Publisher_name , AVG(price) as Price from(\
                           SELECT name as name_new  , COUNT(DISTINCT title_persian) AS BookCount FROM book\
                           join book_publisher on book_publisher.book_code = book.code\
                           join publisher on book_publisher.publisher_id = publisher.id GROUP BY name\
                           HAVING BookCount > 10)as book_publisher_with_more_than_ten\
                           join publisher on book_publisher_with_more_than_ten.name_new = publisher.name\
                           join book_publisher on publisher.id = book_publisher.publisher_id\
                           join book on book_publisher.book_code = book.code\
                           group by book_publisher_with_more_than_ten.name_new\
                           order by price DESC limit 10;")
                    result = cursor.fetchall() 
                    df = pd.DataFrame(result,
                        columns=("Publisher_name","Price"))
                    df['Price'] = df['Price'].astype(int)
                    name_list = list(df['Publisher_name'])
                    st.title('bar chart')
                    chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                        x=alt.X('Price', title="متوسط قیمت"),
                        y=alt.Y('Publisher_name', title="نام انتشارات", sort=name_list)).properties(
                        width=600,
                        height=400)
                    st.altair_chart(chart, use_container_width=True)

                elif type == "2. The most active publishers":
                    cat = st.selectbox('ادبیات داستانی',('اجتماعی','وحشت','علمی','درام','تاریخی','فلسفی','جنگی','جنایی','سیاسی','ماجرایی','معمایی','عاشقانه'))
                    cursor.execute(f"SELECT publisher.name, count(book.code)  as numb from book\
                    join book_publisher on book.code = book_publisher.book_code\
                    join publisher on book_publisher.publisher_id = publisher.id\
                    join group_book on book.code = group_book.book_code\
                    join `group` on group_book.group_id = `group`.id\
                    join group_category on `group`.id = group_category.group_id\
                    join category on group_category.category_id = category.id\
                    join crew on book.code = crew.book_code\
                    join person on crew.person_counter = person.counter\
                    where category.name = 'داستان {cat}'\
                    group by publisher.name\
                    order by numb DESC\
                    limit 10;")            
                    result = cursor.fetchall() 
                    df = pd.DataFrame(
                        result,
                        columns=("pub","numb"))
                    df['numb'] = df['numb'].astype(int)
                    name_list = list(df['pub'])
                    st.title('bar chart')
                    chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                        x=alt.X('numb', title="تعداد کتاب"),
                        y=alt.Y('pub', title="ناشر", sort=name_list)).properties(
                        width=800,
                        height=500)
                    st.altair_chart(chart, use_container_width=True)
                    
                elif type == "3. variety of Writers VS Grade":
                    cursor.execute(f"SELECT release_year_sh , AVG(grade) as num from book\
                                   join crew on book.code = crew.book_code\
                                   where release_year_sh is not NULL and release_year_sh<1402 and release_year_sh>1369\
                                   group by release_year_sh\
                                   order by release_year_sh DESC")
                    result = cursor.fetchall() 
                    df = pd.DataFrame(
                        result,
                        columns=("year","grade"))
                    df['grade'] = df['grade'].astype(float)
                    name_list = list(df['year'])
                    cursor.execute(f"SELECT release_year_sh , count(distinct crew.id) as num from book\
                                   join crew on book.code = crew.book_code\
                                   where release_year_sh is not NULL and release_year_sh<1402 and release_year_sh>1369\
                                   and release_year_sh>1359 and crew.role = 'writer'\
                                   group by release_year_sh\
                                   order by release_year_sh DESC")
                    result_2 = cursor.fetchall() 
                    df_2 = pd.DataFrame(
                        result_2,
                        
                        columns=("year","count_writer"))
                    df_2['count_writer'] = df_2['count_writer'].astype(int)
                    name_list = list(df['year'])
                    cursor.execute(f"SELECT release_year_sh , count(distinct crew.id) as num from book\
                                   join crew on book.code = crew.book_code\
                                   where release_year_sh is not NULL and release_year_sh<1402 and release_year_sh>1369 \
                                   and release_year_sh>1359 and crew.role = 'translator'\
                                   group by release_year_sh\
                                   order by release_year_sh DESC")
                    result_3 = cursor.fetchall() 
                    df_3 = pd.DataFrame(
                        result_3,
                        columns=("year","count_translator"))
                    df_3['count_translator'] = df_3['count_translator'].astype(int)
                    
                    st.title('line')
                    line1 = alt.Chart(df).mark_line().encode(
                        x=alt.X('year', title="سال انتشار"),
                        y=alt.Y('grade', title="متوسط نمره", sort=name_list))
                    line2 = alt.Chart(df_2).mark_line(color='red').encode(
                        x=alt.X('year', title="سال انتشار"),
                        y=alt.Y('count_writer', title="نوع جلد", sort=name_list))
                    line3 = alt.Chart(df_3).mark_line(color='green').encode(
                        x=alt.X('year', title="سال انتشار"),
                        y=alt.Y('count_translator', title="نوع جلد", sort=name_list))
                    chart = alt.layer(line1, line2,line3).resolve_scale(y='independent')
                    st.altair_chart(chart, use_container_width=True)
                    
                elif type == "4. variety of Publish VS Grade":
                    cursor.execute(f"SELECT title_english , COUNT(DISTINCT publisher.name) AS NumBooks\
                                   FROM book\
                                   join book_publisher on book.code = book_publisher.book_code\
                                   join publisher on book_publisher.publisher_id = publisher.id\
                                   join group_book on book.code = group_book.book_code\
                                   join `group` on group_book.group_id = `group`.id\
                                   join group_category on `group`.id = group_category.group_id\
                                   join category on group_category.category_id = category.id\
                                   join crew on book.code = crew.book_code\
                                   join person on crew.person_counter = person.counter\
                                   where title_english is not NULL\
                                   GROUP BY title_english\
                                   order by NumBooks DESC\
                                   limit 10;")
                    result = cursor.fetchall() 
                    df = pd.DataFrame(
                        result,
                        columns=("num","grade"))
                    df['grade'] = df['grade'].astype(float)
                    #name_list = list(df['year'])
                    st.title('line')
                    scatter_plot = sns.scatterplot(data=df, x='num', y='grade')
                    scatter_plot.set_xlabel('title book', fontname='Times New Roman', fontsize=14)
                    scatter_plot.set_ylabel('count publisher', fontname='Times New Roman', fontsize=14)
                    plt.xticks(fontname='Times New Roman',rotation=90)
                    plt.yticks(fontname='Times New Roman')
                    #plt.ylim(0, 500)   
                    sns.despine()
                    #plt.xlim(1360,1403)
                    plt.legend()
                    st.pyplot(scatter_plot.figure)               