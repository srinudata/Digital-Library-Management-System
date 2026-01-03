import sqlite3
import streamlit as st

# ---- Setup Database ----
def setup_database():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---- Add Book ----
def add_books(book_id, title, author):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books (id, title, author) VALUES (?, ?, ?)",
                (book_id, title, author))
    conn.commit()
    conn.close()
    return "Book added successfully!"

# ---- Update Book ----
def update_books(user, pwd, book_id, new_title, new_author):
    if user != "srinu" or pwd != "123":
        return "Access Denied!"

    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET title = ?, author = ? WHERE id = ?",
                (new_title, new_author, book_id))
    conn.commit()
    conn.close()
    return "Book updated successfully!"

# ---- Display Books ----
def display_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No books found in the database."
    else:
        return rows

# ---- Search Books ----
def search_books(keyword):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                   ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No matching books found."
    else:
        return rows

# ---- Delete Book ----
def delete_book(user, pwd, book_id):
    if user != "srinu" or pwd != "123":
        return "Access Denied!"

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return "Book deleted successfully!"

# ---- Streamlit Interface ----
def main():
    setup_database()

    st.header("Digital Library Management System\n")

    menu = ["Add Book", "Update Book", "Display Books", "Search Book", "Delete Book", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Add Book":
        st.subheader(" Add Book")
        book_id = st.number_input("Enter the book ID:", min_value=1, step=1)
        title = st.text_input("Enter the book title:")
        author = st.text_input("Enter the book author:")
        
        if st.button("Add Book"):
            try:
                result = add_books(int(book_id), title, author)
                st.success(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif choice == "Update Book":
        st.subheader(" Update Book")
        user = st.text_input("Enter username:")
        pwd = st.text_input("Enter password:", type="password")
        book_id = st.number_input("Enter book ID to update:", min_value=1, step=1)
        new_title = st.text_input("Enter new title:")
        new_author = st.text_input("Enter new author:")
        
        if st.button("Update Book"):
            result = update_books(user, pwd, book_id, new_title, new_author)
            if "Access Denied" in result:
                st.error(result)
            else:
                st.success(result)
    
    elif choice == "Display Books":
        st.subheader(" Display Books")
        
        if st.button("Show All Books"):
            rows = display_books()
            
            if isinstance(rows, str):
                st.info(rows)
            else:
                st.write("\n Book List ")
                for row in rows:
                    st.write(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}")
    
    elif choice == "Search Book":
        st.subheader(" Search Book")
        keyword = st.text_input("Enter book name or author name:")
        
        if st.button("Search"):
            rows = search_books(keyword)
            
            if isinstance(rows, str):
                st.info(rows)
            else:
                st.write("\n Search Results ")
                for row in rows:
                    st.write(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}")
    
    elif choice == "Delete Book":
        st.subheader(" Delete Book")
        user = st.text_input("Enter username:")
        pwd = st.text_input("Enter password:", type="password")
        book_id = st.number_input("Enter book ID to delete:", min_value=1, step=1)
        
        if st.button("Delete Book"):
            result = delete_book(user, pwd, book_id)
            if "Access Denied" in result:
                st.error(result)
            else:
                st.success(result)
    
    elif choice == "Exit":
        st.subheader(" Exit")
        st.write("Exiting... Thank you!")
        st.stop()

# ---- Run the Program ----
if __name__ == "__main__":
    main()