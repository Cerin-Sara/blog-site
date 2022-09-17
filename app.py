import streamlit as st
import pandas as pd
import numpy as np
from blog_db import *



title_temp ="""
        <div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
            <h3 style="color:white;text-align:center;">{}</h3>
            <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
            <h6>{}</h6>   
            <p style="text-align:justify">{}</p>
        </div>
"""

article_temp ="""
        <div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
        <h4 style="color:white;text-align:center;">{}</h1>
        <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
        <h6>Author:{}</h6> 
        <br/>
        <p style="text-align:justify;color:white">{}</p>
        <h6 style="float:right">Posted on:{}</h6>
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
    single_full_blog = view_selected_blog(selected_title)
    for i in single_full_blog:
        b_author = i[0]
        b_title = i[1]
        b_content = i[2]
        b_tag = i[3]
        b_date = i[4]
        st.markdown(article_temp.format(b_title, b_author, b_content, b_date), unsafe_allow_html=True)

elif choice == 'Manage blog':
    st.subheader('Manage blog')

elif choice == 'Search blog':
    st.subheader('Search blog')

st.sidebar.write('Made with ❤️ by saracerin')