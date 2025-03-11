import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests
import hashlib
import os

# Lớp chính cho ứng dụng
class MovieApp:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.movies = []
        self.users = []
        
        self.load_data()
        self.show_login()

    def load_data(self):
        # Tải dữ liệu phim
        try:
            with open('movies.json', 'r') as f:
                self.movies = json.load(f)
        except FileNotFoundError:
            self.movies = []
        
        # Tải dữ liệu người dùng
        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = []

    def save_movies(self):
        with open('movies.json', 'w') as f:
            json.dump(self.movies, f, indent=4)

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f, indent=4)

    def show_login(self):
        # Cửa sổ đăng nhập
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Đăng nhập")
        
        tk.Label(self.login_window, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(self.login_window, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(self.login_window, text="Đăng nhập", command=self.login).grid(row=2, column=0)
        tk.Button(self.login_window, text="Đăng ký", command=self.show_register).grid(row=2, column=1)

    def show_main(self):
        # Giao diện chính
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Quản lý Phim")
        
        # Treeview hiển thị phim
        self.tree = ttk.Treeview(self.main_window, columns=("ID", "Title", "Year", "Director"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Tên phim")
        self.tree.heading("Year", text="Năm")
        self.tree.heading("Director", text="Đạo diễn")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Nút chức năng
        btn_frame = tk.Frame(self.main_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Thêm phim", command=self.show_add_movie).pack(side=tk.LEFT, padx=5)
        self.update_btn = tk.Button(btn_frame, text="Sửa", command=self.show_edit_movie)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        self.delete_btn = tk.Button(btn_frame, text="Xóa", command=self.delete_movie)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Lấy từ TMDB", command=self.fetch_from_tmdb).pack(side=tk.LEFT, padx=5)
        
        self.update_permissions()
        self.refresh_movies()

    def update_permissions(self):
        if self.current_user['role'] != 'admin':
            self.update_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)

    def refresh_movies(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in self.movies:
            self.tree.insert("", tk.END, values=(movie['id'], movie['title'], movie['year'], movie['director']))

    # Các hàm xử lý đăng nhập/đăng ký
    def login(self):
        username = self.username_entry.get()
        password = self.hash_password(self.password_entry.get())
        
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                self.login_window.destroy()
                self.show_main()
                return
        messagebox.showerror("Lỗi", "Sai thông tin đăng nhập")

    def show_register(self):
        register_window = tk.Toplevel(self.login_window)
        register_window.title("Đăng ký")
        
        # Các trường đăng ký
        tk.Label(register_window, text="Username:").grid(row=0, column=0)
        new_user_entry = tk.Entry(register_window)
        new_user_entry.grid(row=0, column=1)
        
        tk.Label(register_window, text="Password:").grid(row=1, column=0)
        new_pass_entry = tk.Entry(register_window, show="*")
        new_pass_entry.grid(row=1, column=1)
        
        def register():
            new_user = {
                'username': new_user_entry.get(),
                'password': self.hash_password(new_pass_entry.get()),
                'role': 'user'
            }
            self.users.append(new_user)
            self.save_users()
            messagebox.showinfo("Thành công", "Đăng ký thành công")
            register_window.destroy()
        
        tk.Button(register_window, text="Đăng ký", command=register).grid(row=2, columnspan=2)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Các hàm CRUD cho phim
    def show_add_movie(self):
        self.movie_form("Thêm phim mới", self.add_movie)

    def show_edit_movie(self):
        selected = self.tree.selection()
        if not selected:
            return
        movie_id = self.tree.item(selected[0])['values'][0]
        movie = next(m for m in self.movies if m['id'] == movie_id)
        self.movie_form("Sửa thông tin phim", self.update_movie, movie)

    def movie_form(self, title, callback, movie=None):
        form_window = tk.Toplevel(self.main_window)
        form_window.title(title)
        
        fields = ['title', 'year', 'director', 'description']
        entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(form_window, text=field.capitalize()+":").grid(row=i, column=0)
            entry = tk.Entry(form_window)
            entry.grid(row=i, column=1)
            if movie:
                entry.insert(0, movie[field])
            entries[field] = entry
        
        def submit():
            data = {field: entries[field].get() for field in fields}
            if movie:
                data['id'] = movie['id']
            callback(data)
            form_window.destroy()
        
        tk.Button(form_window, text="Lưu", command=submit).grid(row=len(fields), columnspan=2)

    def add_movie(self, data):
        new_id = max(m['id'] for m in self.movies) + 1 if self.movies else 1
        movie = {'id': new_id, **data}
        self.movies.append(movie)
        self.save_movies()
        self.refresh_movies()

    def update_movie(self, data):
        for i, movie in enumerate(self.movies):
            if movie['id'] == data['id']:
                self.movies[i] = data
                break
        self.save_movies()
        self.refresh_movies()

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            return
        movie_id = self.tree.item(selected[0])['values'][0]
        self.movies = [m for m in self.movies if m['id'] != movie_id]
        self.save_movies()
        self.refresh_movies()

    # Lấy dữ liệu từ TMDB API
    def fetch_from_tmdb(self):
        def fetch():
            api_key = 'YOUR_API_KEY'  # Thay bằng API key thật
            query = search_entry.get()
            url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
            response = requests.get(url)
            data = response.json()
            
            for result in data.get('results', [])[:5]:  # Lấy 5 kết quả đầu
                movie_data = {
                    'title': result['title'],
                    'year': result['release_date'][:4] if result['release_date'] else 'N/A',
                    'director': 'Không rõ',  # TMDB không cung cấp đạo diễn trong kết quả tìm kiếm
                    'description': result['overview']
                }
                self.add_movie(movie_data)
            search_window.destroy()
        
        search_window = tk.Toplevel(self.main_window)
        tk.Label(search_window, text="Tìm phim:").pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()
        tk.Button(search_window, text="Tìm kiếm", command=fetch).pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc
    app = MovieApp(root)
    root.mainloop()

'''
Dùng pyinstaller để đóng gói với lệnh:
pyinstaller --onefile --windowed movie_app.py
'''