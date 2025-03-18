import json
import os
import streamlit as st

# File path
data_file = "library.txt"

# Functions (waisa hi rahega)
def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    else:
        return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

def add_book(library):
    title = st.text_input("Enter the title of the book:")
    author = st.text_input("Enter the author of the book:")
    year = st.text_input("Enter the year of the book:")
    genre = st.text_input("Enter the genre of the book:")
    read = st.radio("Have you read the book?", ("Yes", "No")) == "Yes"
    
    if st.button("Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }
        library.append(new_book)
        save_library(library)
        st.success(f"Book '{title}' added successfully!")

def remove_book(library):
    title = st.text_input("Enter the title of the book you want to remove:")
    if st.button("Remove Book"):
        initial_length = len(library)
        library = [book for book in library if book["title"].lower() != title.lower()]
        if len(library) < initial_length:
            save_library(library)
            st.success(f"Book '{title}' removed successfully!")
        else:
            st.error(f"Book '{title}' not found in the library.")

def search_library(library):
    search_by = st.selectbox("Search by:", ["title", "author"])
    search_term = st.text_input(f"Enter the {search_by}:")
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book[search_by].lower()]
        if results:
            for book in results:
                status = "Read" if book["read"] else "Unread"
                st.write(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
        else:
            st.warning(f"No books found for '{search_term}' in the {search_by} field.")

def display_all_books(library):
    if library:
        for book in library:
            status = "Read" if book["read"] else "Unread"
            st.write(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
    else:
        st.warning("The library is empty.")

def display_statistics(library):
    total_books = len(library)
    total_read_books = len([book for book in library if book["read"]])
    percentage_read = (total_read_books / total_books) * 100 if total_books > 0 else 0
    
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

# Main Streamlit App
def main():
    st.title("Personal Library Manager 📚")
    library = load_library()
    
    menu = ["Add Book", "Remove Book", "Search Library", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Add Book":
        st.header("Add a New Book")
        add_book(library)
    elif choice == "Remove Book":
        st.header("Remove a Book")
        remove_book(library)
    elif choice == "Search Library":
        st.header("Search the Library")
        search_library(library)
    elif choice == "Display All Books":
        st.header("All Books in the Library")
        display_all_books(library)
    elif choice == "Display Statistics":
        st.header("Library Statistics")
        display_statistics(library)

if __name__ == "__main__":
    main()