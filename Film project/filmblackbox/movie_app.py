import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import requests
from bs4 import BeautifulSoup

# Crawl dữ liệu phim
def crawl_movies():
    url='' #web muốn lấy dữ liệu phim

# Đường dẫn đến file JSON
DATA_FILE = 'movies.json'

# Hàm để đọc dữ liệu từ file JSON
def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Hàm để ghi dữ liệu vào file JSON
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Hàm để thêm phim mới
def add_movie():
    title = simpledialog.askstring("Input", "Enter movie title:")
    genre = simpledialog.askstring("Input", "Enter movie genre:")
    if title and genre:
        movies = read_data()
        movies.append({"title": title, "genre": genre})
        write_data(movies)
        load_movies()
    else:
        messagebox.showwarning("Warning", "Title and genre cannot be empty!")

# Hàm để xóa phim
def delete_movie():
    selected_movie = movie_listbox.curselection()
    if selected_movie:
        movies = read_data()
        del movies[selected_movie[0]]
        write_data(movies)
        load_movies()
    else:
        messagebox.showwarning("Warning", "Select a movie to delete!")

# Hàm để tải danh sách phim
def load_movies():
    movies = read_data()
    movie_listbox.delete(0, tk.END)
    for movie in movies:
        movie_listbox.insert(tk.END, f"{movie['title']} - {movie['genre']}")

# Hàm để cập nhật phim
def update_movie():
    selected_movie = movie_listbox.curselection()
    if selected_movie:
        movies = read_data()
        title = simpledialog.askstring("Input", "Enter new movie title:", initialvalue=movies[selected_movie[0]]['title'])
        genre = simpledialog.askstring("Input", "Enter new movie genre:", initialvalue=movies[selected_movie[0]]['genre'])
        if title and genre:
            movies[selected_movie[0]] = {"title": title, "genre": genre}
            write_data(movies)
            load_movies()
        else:
            messagebox.showwarning("Warning", "Title and genre cannot be empty!")
    else:
        messagebox.showwarning("Warning", "Select a movie to update!")

# Tạo giao diện chính
root = tk.Tk()
root.title("Movie Management App")

# Tạo Listbox để hiển thị danh sách phim
movie_listbox = tk.Listbox(root, width=50)
movie_listbox.pack(pady=20)

# Tạo nút để thêm phim
add_button = tk.Button(root, text="Add Movie", command=add_movie)
add_button.pack(pady=5)

# Tạo nút để xóa phim
delete_button = tk.Button(root, text="Delete Movie", command=delete_movie)
delete_button.pack(pady=5)

# Tải danh sách phim khi khởi động
load_movies()

# Chạy ứng dụng
root.mainloop()