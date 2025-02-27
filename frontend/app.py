import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("📚 Book Management App")

# --- Function to fetch all books ---
def get_books():
    response = requests.get(f"{BASE_URL}/books")
    return response.json() if response.status_code == 200 else []

# --- Function to fetch a book by ID ---
def get_book_by_id(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    return response.json() if response.status_code == 200 else None

# --- Function to filter books by rating ---
def get_books_by_rating(rating):
    response = requests.get(f"{BASE_URL}/books/filter?book_rating={rating}")
    return response.json() if response.status_code == 200 else []

# --- Function to filter books by published date ---
def get_books_by_published_date(year):
    response = requests.get(f"{BASE_URL}/books/publish?published_date={year}")
    return response.json() if response.status_code == 200 else []

# --- Function to add a new book ---
def add_book(title, author, description, rating, published_date):
    book_data = {
        "title": title,
        "author": author,
        "description": description,
        "rating": rating,
        "published_date": published_date,
    }
    response = requests.post(f"{BASE_URL}/books", json=book_data)
    return response.status_code == 201

# --- Function to update a book ---
def update_book(book_id, title, author, description, rating, published_date):
    book_data = {
        "title": title,
        "author": author,
        "description": description,
        "rating": rating,
        "published_date": published_date,
    }
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=book_data)
    return response.status_code == 200

# --- Function to delete a book ---
def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    return response.status_code == 204

# --- Display books ---
st.subheader("📖 Book List")
books = get_books()

if books:
    for book in books:
        st.markdown(f"**{book['title']}** by {book['author']} - Rating: {book['rating']} ⭐")
        st.caption(book["description"])
        if st.button(f"❌ Delete {book['title']}", key=f"del_{book['id']}"):
            if delete_book(book["id"]):
                st.success(f"Deleted {book['title']}. Refresh to see the updates.")
else:
    st.write("No books found.")

# --- Search Book by ID ---
st.subheader("🔍 Search Book by ID")
book_id = st.number_input("Enter Book ID", min_value=1, step=1)
if st.button("Search by ID"):
    book = get_book_by_id(book_id)
    if book:
        st.write(book)
    else:
        st.error("Book not found!")

# --- Filter Books by Rating ---
st.subheader("⭐ Filter Books by Rating")
rating = st.slider("Select Rating", 1, 5, 3)
if st.button("Filter by Rating"):
    filtered_books = get_books_by_rating(rating)
    if filtered_books:
        for book in filtered_books:
            st.write(book)
    else:
        st.write("No books found with this rating.")

# --- Filter Books by Published Year ---
st.subheader("📆 Filter Books by Published Year")
year = st.number_input("Enter Published Year", min_value=2000, max_value=2030, step=1)
if st.button("Filter by Year"):
    filtered_books = get_books_by_published_date(year)
    if filtered_books:
        for book in filtered_books:
            st.write(book)
    else:
        st.write("No books found from this year.")

# --- Add a new book ---
st.subheader("➕ Add a New Book")
with st.form("add_book_form"):
    title = st.text_input("Title")
    author = st.text_input("Author")
    description = st.text_area("Description")
    rating = st.slider("Rating (1-5)", 1, 5, 3)
    published_date = st.number_input("Published Year", min_value=2000, max_value=2030, step=1)

    submit = st.form_submit_button("Add Book")
    if submit:
        if title and author:
            if add_book(title, author, description, rating, published_date):
                st.success("Book added successfully! Refresh to see updates.")
            else:
                st.error("Failed to add book.")
        else:
            st.warning("Title and Author are required.")

# --- Update a Book ---
st.subheader("✏️ Update a Book")
update_id = st.number_input("Enter Book ID to Update", min_value=1, step=1)
with st.form("update_book_form"):
    new_title = st.text_input("New Title")
    new_author = st.text_input("New Author")
    new_description = st.text_area("New Description")
    new_rating = st.slider("New Rating (1-5)", 1, 5, 3)
    new_published_date = st.number_input("New Published Year", min_value=2000, max_value=2030, step=1)

    update_submit = st.form_submit_button("Update Book")
    if update_submit:
        if new_title and new_author:
            if update_book(update_id, new_title, new_author, new_description, new_rating, new_published_date):
                st.success("Book updated successfully! Refresh to see updates.")
            else:
                st.error("Failed to update book.")
        else:
            st.warning("Title and Author are required.")