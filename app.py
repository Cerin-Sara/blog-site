import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from blog_db import *
from wordcloud import *



title_temp ="""
        <div style="background-color:#C3F8FF;padding:10px;border-radius:10px;margin:10px;">
            <h3 style="color:#0E1117;text-align:center;">{}</h3>
            <h6 style="color:#0E1117;text-align:center;">{}</h6>
            <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
            <p style="text-align:justify;color:#0E1117">{}</p>
        </div>
"""

article_temp ="""
        <div style="background-color:#C3F8FF;padding:10px;border-radius:5px;margin:10px;">
        <h4 style="color:#0E1117;text-align:center;">{}</h1>
        <h6 style="color:#0E1117;text-align:center">By:{}</h6> 
        <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
        <br/>
        <p style="text-align:justify;color:#0E1117">{}</p>
        <h6 style="float:right;color:#0E1117">Posted on:{}</h6>
        <br/>
        <br/>
        </div>
"""


st.title('Blog')
def get_choice():
    menu = ['Home', 'Add blog', 'View blog', 'Manage blog', 'Search blog']
    choice = st.sidebar.selectbox('Select', menu)
    return choice
choice=get_choice()

if choice == 'Home':
    st.subheader('Home')
    result = view_all_blogs()
    for i in result:
        b_author = i[0]
        b_title = i[1]
        b_content = i[2][:190]
        b_tag = i[3]
        b_date = i[4]
        st.markdown(title_temp.format( b_title, b_author, b_content), unsafe_allow_html=True)

elif choice == 'Add blog':
    create_table()
    st.subheader('Add blog')
    blog_author=st.text_input("Author name", max_chars=20)
    blog_title=st.text_input("Blog title")
    blog_content=st.text_area("Blog content")
    blog_tag=st.text_input("Blog tag")
    blog_date=st.date_input("Blog date")
    if st.button("Add"):
        add_data(blog_author, blog_title, blog_content,blog_tag, blog_date)
        st.success("Blog added successfully")

elif choice == 'View blog':
    st.subheader('View blog')
    all_titles = view_all_titles()
    title_list = []
    for i in all_titles:
        title_list.append(i[0])
    selected_title = st.sidebar.selectbox('Select blog', title_list)
    single_full_blog = view_selected_blog_by_title(selected_title)
    for i in single_full_blog:
        b_author = i[0]
        b_title = i[1]
        b_content = i[2]
        b_tag = i[3]
        b_date = i[4]
        st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
        st.markdown(article_temp.format(b_title, b_author, b_content, b_date), unsafe_allow_html=True)

elif choice == 'Manage blog':
    st.subheader('Manage blog')
    result = view_all_blogs()
    clean_db = pd.DataFrame(result, columns=['Author', 'Title', 'Content', 'Tag', 'Date'])
    st.dataframe(clean_db)
    selected_title = st.selectbox('Select blog to delete', clean_db['Title'])
    st.warning("Are you sure you want to delete {}?".format(selected_title))
    if st.button("Delete"):
        delete_blog_by_title(selected_title)
        st.warning("Deleted {} successfully".format(selected_title))
    
    if st.sidebar.checkbox("Statistics"):
        newDf=clean_db
        newDf['Length']=newDf['Content'].str.len()
        st.dataframe(newDf)

        st.subheader("Author Staticss")
        newDf['Author'].value_counts().plot(kind='bar')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        newDf['Author'].value_counts().plot.pie(autopct="%1.1f%%")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.axis("off")
        st.pyplot()

    if st.sidebar.checkbox("Word Cloud"):
        newDf=clean_db
        st.subheader("Generating Word Cloud")
        text = ",".join(newDf['Content'])
        wc = WordCloud().generate(text)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        st.pyplot()
    
    if st.sidebar.checkbox("Article Length"):
        newDf=clean_db
        st.subheader("Article Length")
        newDf['Length']= newDf['Content'].str.len()
        barPlot = newDf.plot.barh(x='Author', y='Length', rot=0)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


    

elif choice == 'Search blog':
    st.subheader('Search blog')
    search_field = st.radio("Select the field", ('author', 'title', 'tag', 'date'))
    search_item = st.text_input("Enter the {}'s name by which you want to Search".format(search_field))
    if search_field=='author':
        result = view_selected_blog_by_author(search_item)
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_content = i[2]
            b_tag = i[3]
            b_date = i[4]
            st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
            st.markdown(article_temp.format(b_title, b_author, b_content, b_date), unsafe_allow_html=True)

    elif search_field=='title':
        result = view_selected_blog_by_title(search_item)
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_content = i[2]
            b_tag = i[3]
            b_date = i[4]
            st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
            st.markdown(article_temp.format(b_title, b_author, b_content, b_date), unsafe_allow_html=True)
    
    elif search_field=='tag':
        result = view_selected_blog_by_tag(search_item)
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_content = i[2]
            b_tag = i[3]
            b_date = i[4]
            st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
            st.markdown(article_temp.format(b_title, b_author, b_content, b_date), unsafe_allow_html=True)
    
    elif search_field=='date':
        result = view_selected_blog_by_date(search_item)
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_content = i[2]
            b_tag = i[3]
            b_date = i[4]
            st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
            st.markdown(article_temp.format(b_title, b_author, b_content, b_date), unsafe_allow_html=True)
    

st.sidebar.write('Made with ❤️ by saracerin')