import sqlite3

conn = sqlite3.connect('blog.db', check_same_thread=False)
c=conn.cursor()
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtables(author TEXT, title TEXT, content TEXT, tag TEXT,date DATE)')

def add_data(author, title, content, blog_tag, date):
    c.execute('INSERT INTO blogtables(author, title, content, tag, date) VALUES(?, ?, ?, ?, ?)', (author, title, content, blog_tag, date))
    conn.commit()

def view_all_blogs():
    c.execute('SELECT * FROM blogtables')
    data = c.fetchall()
    return data

def view_all_titles():
    c.execute('SELECT title FROM blogtables')
    data = c.fetchall()
    return data

def view_selected_blog(title):
    c.execute('SELECT * FROM blogtables WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data

# def drop_table():
#     c.execute('DROP TABLE blogtable')
#     return 'Table dropped'