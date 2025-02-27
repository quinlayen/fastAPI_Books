# FastAPI + Streamlit Book Management App

## 📌 Overview
This is a **Book Management Application** built using **FastAPI** for the backend and **Streamlit** for the frontend. It allows users to:

✅ View all books
✅ Search for books by ID
✅ Filter books by rating
✅ Filter books by published year
✅ Add a new book
✅ Update an existing book
✅ Delete a book

The application uses **PostgreSQL** as the database and **SQLAlchemy** as the ORM.

---

## 🚀 Tech Stack
- **Backend:** FastAPI, Uvicorn, SQLAlchemy, PostgreSQL
- **Frontend:** Streamlit
- **Database:** PostgreSQL
- **Virtual Environment:** Python venv
- **Dependency Management:** pip

---

## 📂 Project Structure
```
├── backend/                # FastAPI Backend
│   ├── main.py             # FastAPI app with CRUD endpoints
│   ├── database.py         # Database connection setup
│   ├── fastapi.log         # FastAPI log file
├── frontend/               # Streamlit Frontend
│   ├── app.py              # Streamlit UI for interacting with FastAPI
│   ├── streamlit.log       # Streamlit log file
├── setup.sh                # Script to set up virtual environment & dependencies
├── run.sh                  # Script to start backend and frontend
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
```

---

## 🔧 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/book-management-app.git
cd book-management-app
```

### 2️⃣ Set Up the Virtual Environment
```bash
chmod +x setup.sh
./setup.sh
```

### 3️⃣ Configure the Database
1. Ensure PostgreSQL is installed and running.
2. Create a database:
   ```sql
   CREATE DATABASE booksdb;
   ```
3. Update `DATABASE_URL` in `backend/database.py` with your credentials.

---

## ▶ Running the Application
### 1️⃣ Start Backend and Frontend
```bash
chmod +x run.sh
./run.sh
```

### 2️⃣ Access the Application
- **Backend API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Frontend UI:** [http://localhost:8501](http://localhost:8501)

---

## 📡 API Endpoints
| Method  | Endpoint                  | Description                 |
|---------|---------------------------|-----------------------------|
| GET     | `/books`                   | Retrieve all books         |
| GET     | `/books/{book_id}`         | Retrieve book by ID        |
| GET     | `/books/filter?book_rating={rating}` | Filter books by rating |
| GET     | `/books/publish?published_date={year}` | Filter by year |
| POST    | `/books`                   | Add a new book             |
| PUT     | `/books/{book_id}`         | Update a book              |
| DELETE  | `/books/{book_id}`         | Delete a book              |

---

## 📜 License
This project is licensed under the MIT License.

---

## 💡 Future Improvements
- Add authentication with JWT
- Implement Alembic migrations for database changes
- Improve UI with more features

---

## ✨ Contributing
1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch`
3. Make changes and commit: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature-branch`
5. Open a Pull Request

---

## 📞 Contact
For any questions, feel free to reach out:
- **Email:** your.email@example.com
- **GitHub:** [yourusername](https://github.com/yourusername)

