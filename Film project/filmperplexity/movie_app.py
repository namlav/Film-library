import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests
from bs4 import BeautifulSoup

def load_movies():
    try:
        with open('movies.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
        
def save_movies(data):
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

class MovieApp:
    def __init__(self, root, user_role):
        self.root = root
        self.user_role = user_role
        self.root.title("Hệ thống Quản lý Phim")
        
        # TreeView hiển thị danh sách phim
        self.tree = ttk.Treeview(root, columns=("Title", "Year", "Genre"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Title", text="Tên phim")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Nút chức năng
        btn_frame = tk.Frame(root)
        tk.Button(btn_frame, text="Thêm phim", command=self.add_movie).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Sửa", command=self.edit_movie).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Xóa", command=self.delete_movie).pack(side=tk.LEFT)
        btn_frame.pack(pady=10)
        
        self.load_data()
        
    def load_data(self):
        movies = load_movies()
        for movie in movies:
            self.tree.insert('', tk.END, text=movie['id'], 
                           values=(movie['title'], movie['year'], movie['genre']))

#crawl dữ liệu phim
def crawl_imdb_movies():
    url = "https://www.imdb.com/chart/moviemeter/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    movies = []
    for item in soup.select('.lister-list tr'):
        title = item.select_one('.titleColumn a').text
        year = item.select_one('.secondaryInfo').text.strip('()')
        rating = item.select_one('.imdbRating').text.strip()
        movies.append({
            'title': title,
            'year': year,
            'rating': rating
        })
    return movies

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        
        tk.Label(root, text="Username:").grid(row=0, column=0)
        self.username = tk.Entry(root)
        self.username.grid(row=0, column=1)
        
        tk.Label(root, text="Password:").grid(row=1, column=0)
        self.password = tk.Entry(root, show="*")
        self.password.grid(row=1, column=1)
        
        tk.Button(root, text="Login", command=self.authenticate).grid(row=2, columnspan=2)

    def authenticate(self):
        users = load_users()  # Hàm tương tự load_movies()
        # Xác thực và phân quyền...

def add_movie(self):
    add_window = tk.Toplevel()
    # Form nhập liệu
    entries = {}
    fields = ['title', 'year', 'genre', 'director']
    for idx, field in enumerate(fields):
        tk.Label(add_window, text=field.capitalize()).grid(row=idx, column=0)
        entries[field] = tk.Entry(add_window)
        entries[field].grid(row=idx, column=1)
    
    tk.Button(add_window, text="Lưu", 
             command=lambda: self.save_new_movie(entries)).grid(row=len(fields), columnspan=2)

'''
Dùng pyinstaller để đóng gói với lệnh:
pyinstaller --onefile --windowed movie_app.py
'''