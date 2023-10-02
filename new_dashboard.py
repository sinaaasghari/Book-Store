import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns
import random
import plotly.express as px
import numpy as np

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Amir1376%',
    database='bookstores'
)

cursor = conn.cursor()

def main():
    
    Menu = ['Part 1','Part 2','Part 3']
    choice = st.sidebar.selectbox('MENU',Menu)
    
    if choice == 'Part 1':
        
        st.subheader("Part 1")
        tab1, tab2 = st.tabs(["📈 Analytical Chart", "🗃 Data"])
        
        with tab1:
            col1, col2 = st.columns([1,3])
            with col1:
                type=st.selectbox(
                    "Analytical charts",
                    key="Analytical charts",
                    options=["1. Tag counting", "2. Publisher counting", "3. Annual publication",
                             "4. Writers counting","5. Translators counting","6. Page vs Year" , 
                             "7. Price vs Year" , "8. Price vs Rate" ,"9. Book Type"])
        with col2:
            if type == "1. Tag counting":
                # plot question 1
                st.header('Count the book :blue[tags]')
                number = st.number_input('Choose number', step=1,value=20,min_value=5)
                cursor.execute(f"select name,count(*) as count_book from group_category \
                        inner join category c on group_category.category_id = c.id\
                                group by name order by count_book desc limit {number}")
                result = cursor.fetchall()
                df = pd.DataFrame(
                    result,
                        columns=("name","count_book"))
                name_list = list(df['name'])
                ###
                st.title('bar chart')
                chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                    x=alt.X('count_book', title="تعداد کتاب‌ها"),
                    y=alt.Y('name', title="دسته بندی‌ها", sort= name_list)).properties(
                    width=600,
                    height=400)
                st.altair_chart(chart, use_container_width=True)
                ###
                st.title('Pie chart')
                fig = px.pie(df, values='count_book', names='name')
                st.plotly_chart(fig, use_container_width=True)
                
            elif type == "2. Publisher counting":
                # plot question 2
                st.header(':blue[Publishers] counting')
                cursor.execute(f"select name,count(*) as count_book from book_publisher \
                           inner join publisher p on book_publisher.publisher_id = p.id \
                            group by publisher_id order by count_book desc limit 10")
                result = cursor.fetchall()
                df = pd.DataFrame(
                    result,
                    columns=("name","count_book"))
                name_list = list(df['name'])
                ###
                st.title('bar chart')
                chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                    x=alt.X('count_book', title="تعداد کتاب‌ها"),
                    y=alt.Y('name', title="نام انتشارات" , sort=name_list)).properties(
                    width=600,
                    height=400)
                st.altair_chart(chart, use_container_width=True)
                ###
                st.title('Pie chart')
                fig = px.pie(df, values='count_book', names='name')
                st.plotly_chart(fig, use_container_width=True) 
                
            elif type == "3. Annual publication":
                # plot question 3
                st.header('Annual :blue[publication]')
                release_year = st.selectbox(
                    'release year',('miladi', 'shamsi'))
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
                ###
                st.title('bar chart')
                chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                    x=alt.X(f'{release_year}', title="سال انتشار",
                            scale=alt.Scale(domain=(start_year, end_year)),
                            axis=alt.Axis(tickCount=4)),
                    y=alt.Y('count_book', title="تعداد کتاب ها",
                            scale=alt.Scale(domain=(0, end_count)))).properties(
                    width=500,
                    height=300)
                st.altair_chart(chart, use_container_width=True)
                ###
                st.title('Pie chart')
                fig = px.pie(df, values='count_book', names=f'{release_year}')
                st.plotly_chart(fig, use_container_width=True)
                
            elif type == "4. Writers counting":
                # plot question 4
                st.header(':blue[Writers] counting')
                cursor.execute(f"select name , count(*) as book_code from crew \
                           inner join person p on crew.person_counter = p.counter\
                               where role ='writer'group by name \
                               order by book_code desc limit 10")
                result = cursor.fetchall()
                df = pd.DataFrame(
                    result,
                    columns=("name","count_book"))
                name_list = list(df['name']) 
                ###
                st.title('bar chart')
                chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                    x=alt.X('count_book', title=" نویسندگان "),
                    y=alt.Y('name', title="تعداد کتاب ها", sort=name_list)).properties(width=500,height=300)
                
                st.altair_chart(chart, use_container_width=True)
                ###
                st.title('Pie chart')
                fig = px.pie(df, values='count_book', names='name')
                st.plotly_chart(fig, use_container_width=True) 
                
            elif type == "5. Translators counting":
                # plot question 5
                st.header(':blue[Translators] counting')
                cursor.execute(f"select name , count(*) as book_code from crew \
                           inner join person p on crew.person_counter = p.counter\
                               where role ='translator'group by name \
                               order by book_code desc limit 10")
                result = cursor.fetchall()
                df = pd.DataFrame(
                    result,
                    columns=("name","count_book"))
                name_list = list(df['name'])
                ###
                st.title('bar chart')
                chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                    x=alt.X('count_book', title="تعداد"),
                    y=alt.Y('name', title="نام مترجمان", sort=name_list)).properties(
                    width=500,
                    height=300)
                st.altair_chart(chart, use_container_width=True)
                ###
                st.title('Pie chart')
                fig = px.pie(df, values='count_book', names='name')
                st.plotly_chart(fig, use_container_width=True)
                
            elif type == "6. Page vs Year":
                # plot question 6
                st.header('Relationship between the :blue[number of pages] and the :blue[year of publication]')
                cursor.execute(f"select release_year_sh  as Year, AVG(page_count) as Count from book \
                               group by release_year_sh")
                result = cursor.fetchall() 
                df = pd.DataFrame(
                    result,
                    columns=("Year","Count"))
                st.title('scatter chart')
                mean_height = df['Count'].mean()
                scatter_plot = sns.scatterplot(data=df, x='Year', y='Count')
                #plt.axhline(mean_height, color='red', label = 'Average' , alpha=0.5)
                scatter_plot.set_xlabel('Year', fontname='Times New Roman', fontsize=14)
                scatter_plot.set_ylabel('Page', fontname='Times New Roman', fontsize=14)
                plt.xticks(fontname='Times New Roman')
                plt.yticks(fontname='Times New Roman')
                plt.ylim(0, 500)
                sns.despine()
                plt.xlim(1360,1403)
                plt.legend()
                st.pyplot(scatter_plot.figure) 
                
            elif type == "7. Price vs Year":
                # plot question 7
                st.header('Relationship between the :blue[Price] and the :blue[year of publication]')
                cursor.execute(f"select release_year_sh  as Year, AVG(price) as Price from book \
                               group by release_year_sh")
                result = cursor.fetchall() 
                df = pd.DataFrame(
                    result,
                        columns=("Year","Price"))
                st.title('scatter chart')
                mean_height = df['Price'].mean()
                scatter_plot = sns.scatterplot(data=df, x='Year', y='Price')
                #plt.axhline(mean_height, color='red', label = 'Average' , alpha=0.5)
                scatter_plot.set_xlabel('Year', fontname='Times New Roman', fontsize=14)
                scatter_plot.set_ylabel('Price', fontname='Times New Roman', fontsize=14)
                plt.xticks(fontname='Times New Roman')
                plt.ylim(0,500000)
                plt.yticks(fontname='Times New Roman')
                sns.despine()
                plt.xlim(1360,1403)
                plt.legend()
                st.pyplot(scatter_plot.figure)
                          
            elif type == "8. Price vs Rate":
                # plot question 8 
                st.header('Relationship between the :blue[Price] and the :blue[Rate]')
                cursor.execute(f"select grade  as Rate, AVG(price) as Price from book \
                               group by Rate")
                result = cursor.fetchall() 
                df = pd.DataFrame(
                    result,
                        columns=("Rate","Price"))
                df['Rate'] = df['Rate'].astype(float)
                mean_height = df['Price'].mean()
                scatter_plot = sns.scatterplot(data=df, x='Rate', y='Price')
                #plt.axhline(mean_height, color='red', label = 'Average')
                plt.xticks([2.0,3.0,4.0,5.0])
                scatter_plot.set_xlabel('Rate', fontname='Times New Roman', fontsize=14)
                scatter_plot.set_ylabel('Price', fontname='Times New Roman', fontsize=14)
                plt.xticks(fontname='Times New Roman')
                plt.yticks(fontname='Times New Roman')
                sns.despine()
                plt.legend()
                st.pyplot(scatter_plot.figure)
                
            elif type == "9. Book Type":
                # plot question 9
                cursor.execute(f"select ghate , count(*) as quantity from book\
                           where ghate is not NULL and ghate != 'وزیریباکاغذمعطر'\
                           group by ghate\
                           order by quantity DESC;")
                result = cursor.fetchall() 
                df = pd.DataFrame(
                    result,
                        columns=("Ghate","Quantity"))
                name_list = list(df['Ghate']) 
                st.title('bar chart')
                chart = alt.Chart(df).mark_bar(color='#3182bd').encode(
                    x=alt.X('Quantity', title=" تعداد"),
                    y=alt.Y('Ghate', title="نوع قطع ", sort=name_list)).properties(
                    width=600,height=400).configure_axis(
                    labelFontSize=16,
                    titleFontSize=16)
                st.altair_chart(chart, use_container_width=True)
        with tab2:
            col1, col2 = st.columns([1,3])
            with col1:
                type=st.selectbox(
                    "Analytical Dayaframes",
                    key="Analytical Dayaframes",
                    options=["1. Tag counting", "2. Publisher counting", "3. Annual publication",
                             "4. Writers counting","5. Translators counting","6. Page vs Year" , 
                             "7. Price vs Year" , "8. Price vs Rate" ,"9. Book Type"])
            with col2:
                if type == "1. Tag counting":
                    # question 1
                    st.header('Count the book :blue[tags]')
                    number_1 = st.number_input('Choose number', step=1,value=20,min_value=5)
                    cursor.execute(f"select name,count(*) as count_book from group_category \
                        inner join category c on group_category.category_id = c.id\
                                group by name order by count_book desc limit {number_1}")
                    result = cursor.fetchall()
                    df = pd.DataFrame(
                        result,columns=("name","count_book"))
                    st.table(df)
                elif type == "2. Publisher counting":
                    # question 2
                    st.header(':blue[Publishers] counting')
                    cursor.execute(f"select name,count(*) as count_book from book_publisher \
                           inner join publisher p on book_publisher.publisher_id = p.id \
                            group by publisher_id order by count_book desc limit 10")
                    result = cursor.fetchall()
                    df = pd.DataFrame(result,
                    columns=("name","count_book"))
                    st.table(df)
                    
                elif type == "3. Annual publication":
                    # question 3
                    st.header('Annual :blue[publication]')
                    release_year = st.selectbox(
                        'release year_df',('miladi', 'shamsi'))
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
                    number = st.number_input('Choose number_df', step=1,value=10,min_value=5,max_value =30)
                    cursor.execute(f"select {release_year},count(*) as count_book from book group by \
                    {release_year} order by count_book desc limit {number}")
                    result = cursor.fetchall()
                    df = pd.DataFrame(result,
                                      columns=(f"{release_year}","count_book"))
                    df.dropna(subset=[f"{release_year}"],inplace=True)
                    df.iloc[:,0] = df.iloc[:,0].astype(int)
                    st.table(df)
                    
                elif type == "4. Writers counting":
                    # question 4
                    st.header(':blue[Writers] counting')
                    cursor.execute(f"select name , count(*) as book_code from crew \
                           inner join person p on crew.person_counter = p.counter\
                               where role ='writer'group by name \
                               order by book_code desc limit 10")
                    result = cursor.fetchall()
                    df = pd.DataFrame(result,
                                      columns=("name","count_book"))
                    st.table(df)
                    
                elif type == "5. Translators counting":
                    # question 5
                    st.header(':blue[Translators] counting')
                    cursor.execute(f"select name , count(*) as book_code from crew \
                           inner join person p on crew.person_counter = p.counter\
                               where role ='translator'group by name \
                               order by book_code desc limit 10")
                    result = cursor.fetchall()
                    df = pd.DataFrame(result,columns=("name","count_book"))
                    st.table(df)
                
                elif type == "6. Page vs Year":
                    # plot question 6
                    st.header('Relationship between the :blue[number of pages] and the :blue[year of publication]')
                    cursor.execute(f"select release_year_sh  as Year, AVG(page_count) as Count from book \
                               group by release_year_sh")
                    result = cursor.fetchall() 
                    df = pd.DataFrame(result,columns=("Year","Count"))
                    st.table(df)
                    
                elif type == "7. Price vs Year":
                    # plot question 7
                    st.header('Relationship between the :blue[Price] and the :blue[year of publication]')
                    cursor.execute(f"select release_year_sh  as Year, AVG(price) as Price from book \
                               group by release_year_sh")
                    result = cursor.fetchall() 
                    df = pd.DataFrame(
                        result,columns=("Year","Price"))
                    st.table(df)
                
                elif type == "8. Price vs Rate":
                    # plot question 8 
                    st.header('Relationship between the :blue[Price] and the :blue[Rate]')
                    cursor.execute(f"select grade  as Rate, AVG(price) as Price from book \
                               group by Rate")
                    result = cursor.fetchall() 
                    df = pd.DataFrame(result,columns=("Rate","Price"))
                    st.table(df)
                    
                elif type == "9. Book Type":
                    # plot question 9
                    cursor.execute(f"select ghate , count(*) as quantity from book\
                           where ghate is not NULL and ghate != 'وزیریباکاغذمعطر'\
                           group by ghate\
                           order by quantity DESC;")
                    result = cursor.fetchall() 
                    df = pd.DataFrame(result,columns=("Ghate","Quantity"))
                    st.table(df)
                    
    if choice == 'Part 2':
        st.subheader('Part 2')
        
    if choice == 'Part 3':
        st.subheader('Part 3')
        tab1, tab2 = st.tabs(["📈 Analytical Chart", "🗃 Data"])
        
        with tab1:
            col1, col2 = st.columns([1,3])
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
                    cursor.execute(f"SELECT title_english , COUNT(DISTINCT publisher.name) AS NumBooks, AVG(grade) AS AvgRating\
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
                    scatter_plot.set_xlabel('Year', fontname='Times New Roman', fontsize=14)
                    scatter_plot.set_ylabel('Page', fontname='Times New Roman', fontsize=14)
                    plt.xticks(fontname='Times New Roman')
                    plt.yticks(fontname='Times New Roman')
                    #plt.ylim(0, 500)
                    sns.despine()
                    #plt.xlim(1360,1403)
                    plt.legend()
                    st.pyplot(scatter_plot.figure)
        
if __name__ == '__main__':
    main()