import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO
import hashlib
import subprocess
import threading
import webbrowser

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Xem Phim")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Thiết lập biến
        self.current_user = None
        self.current_user_role = None
        self.movies = []
        self.users = []
        self.load_users()
        
        # Frame chính
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Hiển thị màn hình đăng nhập đầu tiên
        self.show_login_screen()

    def load_users(self):
        try:
            if os.path.exists('users.json'):
                with open('users.json', 'r', encoding='utf-8') as file:
                    self.users = json.load(file)
            else:
                # Tạo tài khoản admin mặc định nếu chưa có file users
                admin_password = self.hash_password("admin123")
                self.users = [{"username": "admin", "password": admin_password, "role": "admin"}]
                self.save_users()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu người dùng: {str(e)}")
    
    def save_users(self):
        try:
            with open('users.json', 'w', encoding='utf-8') as file:
                json.dump(self.users, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu người dùng: {str(e)}")
    
    def load_movies(self):
        try:
            if os.path.exists('movies.json'):
                with open('movies.json', 'r', encoding='utf-8') as file:
                    self.movies = json.load(file)
            else:
                # Tạo danh sách phim rỗng nếu chưa có file
                self.movies = []
                self.save_movies()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu phim: {str(e)}")
    
    def save_movies(self):
        try:
            with open('movies.json', 'w', encoding='utf-8') as file:
                json.dump(self.movies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu phim: {str(e)}")
    
    def hash_password(self, password):
        # Mã hóa mật khẩu bằng SHA-256
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_login_screen(self):
        # Xóa các widget hiện tại
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Tạo giao diện đăng nhập
        login_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        login_frame.pack(expand=True)
        
        tk.Label(login_frame, text="ĐĂNG NHẬP ỨNG DỤNG XEM PHIM", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Frame chứa input
        input_frame = tk.Frame(login_frame)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Tên đăng nhập:", font=("Arial", 12)).grid(row=0, column=0, sticky='w', pady=10)
        self.username_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(input_frame, text="Mật khẩu:", font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=10)
        self.password_entry = tk.Entry(input_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Frame chứa buttons
        button_frame = tk.Frame(login_frame)
        button_frame.pack(pady=20)
        
        login_button = tk.Button(button_frame, text="Đăng nhập", font=("Arial", 12), 
                                 command=self.handle_login, width=15, bg="#4CAF50", fg="white")
        login_button.grid(row=0, column=0, padx=10)
        
        register_button = tk.Button(button_frame, text="Đăng ký", font=("Arial", 12), 
                                   command=self.show_register_screen, width=15, bg="#2196F3", fg="white")
        register_button.grid(row=0, column=1, padx=10)
        
        # Bắt sự kiện Enter key
        self.password_entry.bind('<Return>', lambda event: self.handle_login())
    
    def show_register_screen(self):
        # Xóa các widget hiện tại
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Tạo giao diện đăng ký
        register_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        register_frame.pack(expand=True)
        
        tk.Label(register_frame, text="ĐĂNG KÝ TÀI KHOẢN", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Frame chứa input
        input_frame = tk.Frame(register_frame)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Tên đăng nhập:", font=("Arial", 12)).grid(row=0, column=0, sticky='w', pady=10)
        self.reg_username_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.reg_username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(input_frame, text="Mật khẩu:", font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=10)
        self.reg_password_entry = tk.Entry(input_frame, font=("Arial", 12), width=30, show="*")
        self.reg_password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(input_frame, text="Xác nhận mật khẩu:", font=("Arial", 12)).grid(row=2, column=0, sticky='w', pady=10)
        self.reg_confirm_password_entry = tk.Entry(input_frame, font=("Arial", 12), width=30, show="*")
        self.reg_confirm_password_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Frame chứa buttons
        button_frame = tk.Frame(register_frame)
        button_frame.pack(pady=20)
        
        register_button = tk.Button(button_frame, text="Đăng ký", font=("Arial", 12), 
                                   command=self.handle_register, width=15, bg="#4CAF50", fg="white")
        register_button.grid(row=0, column=0, padx=10)
        
        back_button = tk.Button(button_frame, text="Quay lại", font=("Arial", 12), 
                               command=self.show_login_screen, width=15, bg="#f44336", fg="white")
        back_button.grid(row=0, column=1, padx=10)
    
    def handle_register(self):
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()
        
        # Kiểm tra đầu vào
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        # Kiểm tra username đã tồn tại chưa
        for user in self.users:
            if user["username"] == username:
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
                return
        
        # Thêm người dùng mới với vai trò "user"
        hashed_password = self.hash_password(password)
        new_user = {"username": username, "password": hashed_password, "role": "user"}
        self.users.append(new_user)
        self.save_users()
        
        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        self.show_login_screen()
    
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        hashed_password = self.hash_password(password)
        
        for user in self.users:
            if user["username"] == username and user["password"] == hashed_password:
                self.current_user = username
                self.current_user_role = user["role"]
                self.load_movies()
                self.show_main_screen()
                return
        
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    def show_main_screen(self):
        # Xóa các widget hiện tại
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Tạo giao diện chính với menu bên trái
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Frame menu bên trái
        menu_frame = tk.Frame(self.main_frame, bg="#333", width=200)
        menu_frame.grid(row=0, column=0, sticky="nsw")
        menu_frame.pack_propagate(False)
        
        # Frame nội dung bên phải
        self.content_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Cấu hình trọng số
        self.main_frame.columnconfigure(1, weight=10)
        
        # Thêm header cho menu
        tk.Label(menu_frame, text=f"Xin chào, {self.current_user}", font=("Arial", 12, "bold"), 
                 bg="#333", fg="white", anchor="w", padx=10, pady=15).pack(fill=tk.X)
        
        # Vai trò hiện tại
        tk.Label(menu_frame, text=f"Vai trò: {self.current_user_role.upper()}", font=("Arial", 10), 
                 bg="#333", fg="#aaa", anchor="w", padx=10, pady=5).pack(fill=tk.X)
        
        # Nút menu
        buttons = [
            ("Trang chủ", self.show_home_screen),
            ("Tìm kiếm phim", self.show_search_screen),
            ("Phim đã xem", self.show_watched_movies)
        ]
        
        # Thêm các tùy chọn quản trị nếu là admin
        if self.current_user_role == "admin":
            buttons.append(("Quản lý phim", self.show_movie_management))
            buttons.append(("Quản lý người dùng", self.show_user_management))
            buttons.append(("Crawler phim", self.show_crawler_screen))
        
        buttons.append(("Đăng xuất", self.logout))
        
        for text, command in buttons:
            btn = tk.Button(menu_frame, text=text, font=("Arial", 11), 
                           bg="#333", fg="white", bd=0, anchor="w", padx=10, pady=10,
                           activebackground="#555", activeforeground="white",
                           command=command)
            btn.pack(fill=tk.X)
            # Hiệu ứng hover
            btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg="#555"))
            btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg="#333"))
        
        # Hiển thị trang chủ mặc định
        self.show_home_screen()
    
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home_screen(self):
        self.clear_content_frame()
        
        # Header trang chủ
        header_frame = tk.Frame(self.content_frame, bg="#f5f5f5", padx=20, pady=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="PHIM MỚI CẬP NHẬT", font=("Arial", 18, "bold"), 
                 bg="#f5f5f5").pack(anchor="w")
        
        # Tạo frame để hiển thị danh sách phim
        movies_frame = tk.Frame(self.content_frame, bg="#f5f5f5", padx=20, pady=10)
        movies_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tạo canvas để có thể scroll
        canvas = tk.Canvas(movies_frame, bg="#f5f5f5")
        scrollbar = ttk.Scrollbar(movies_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Hiển thị các phim trong lưới
        if not self.movies:
            tk.Label(scrollable_frame, text="Chưa có phim nào!", font=("Arial", 14), 
                     bg="#f5f5f5", padx=20, pady=20).grid(row=0, column=0)
        else:
            # Sắp xếp phim mới nhất trước
            sorted_movies = sorted(self.movies, key=lambda x: x.get("added_date", ""), reverse=True)
            
            # Hiển thị các phim trong lưới 4 cột
            row, col = 0, 0
            max_cols = 4
            
            for movie in sorted_movies:
                self.create_movie_card(scrollable_frame, movie, row, col)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
    
    def create_movie_card(self, parent, movie, row, col):
        # Tạo card hiển thị thông tin phim
        card = tk.Frame(parent, bg="white", padx=10, pady=10, relief=tk.RAISED, bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Thêm ảnh phim
        try:
            image_url = movie.get("poster", "")
            if image_url and image_url.startswith("http"):
                # Tải ảnh từ URL
                response = requests.get(image_url)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((150, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
            else:
                # Sử dụng ảnh mặc định
                img = Image.new('RGB', (150, 200), color = (200, 200, 200))
                photo = ImageTk.PhotoImage(img)
                
            img_label = tk.Label(card, image=photo, bg="white")
            img_label.image = photo  # Giữ tham chiếu
            img_label.pack(pady=5)
        except Exception:
            # Nếu không tải được ảnh, hiển thị placeholder
            placeholder = tk.Label(card, text="No Image", width=20, height=10, bg="#eee")
            placeholder.pack(pady=5)
        
        # Thêm thông tin phim
        title_text = movie.get("title", "Unknown")
        if len(title_text) > 25:
            title_text = title_text[:22] + "..."
            
        title = tk.Label(card, text=title_text, font=("Arial", 12, "bold"), bg="white", wraplength=150)
        title.pack(pady=5)
        
        year = tk.Label(card, text=f"Năm: {movie.get('year', 'N/A')}", font=("Arial", 10), bg="white")
        year.pack(anchor="w")
        
        rating = tk.Label(card, text=f"Đánh giá: {movie.get('rating', 'N/A')}/10", font=("Arial", 10), bg="white")
        rating.pack(anchor="w")
        
        # Nút xem phim
        watch_btn = tk.Button(card, text="Xem phim", bg="#4CAF50", fg="white", 
                               command=lambda m=movie: self.watch_movie(m))
        watch_btn.pack(pady=10, fill=tk.X)
    
    def watch_movie(self, movie):
        # Tạo cửa sổ mới để xem chi tiết phim và phát phim
        movie_window = tk.Toplevel(self.root)
        movie_window.title(movie.get("title", "Movie"))
        movie_window.geometry("800x600")
        
        # Frame chính
        main_frame = tk.Frame(movie_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame chứa poster và thông tin
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Tải poster
        try:
            image_url = movie.get("poster", "")
            if image_url and image_url.startswith("http"):
                response = requests.get(image_url)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((200, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                poster_label = tk.Label(info_frame, image=photo)
                poster_label.image = photo  # Giữ tham chiếu
                poster_label.grid(row=0, column=0, padx=20, pady=10, rowspan=6)
            else:
                # Placeholder nếu không có ảnh
                placeholder = tk.Label(info_frame, text="No Image", width=20, height=15, bg="#eee")
                placeholder.grid(row=0, column=0, padx=20, pady=10, rowspan=6)
        except Exception:
            # Placeholder nếu lỗi
            placeholder = tk.Label(info_frame, text="No Image", width=20, height=15, bg="#eee")
            placeholder.grid(row=0, column=0, padx=20, pady=10, rowspan=6)
        
        # Thông tin phim
        tk.Label(info_frame, text=movie.get("title", ""), font=("Arial", 16, "bold")).grid(
            row=0, column=1, sticky="w", pady=5)
        
        tk.Label(info_frame, text=f"Năm: {movie.get('year', 'N/A')}", font=("Arial", 12)).grid(
            row=1, column=1, sticky="w", pady=3)
        
        tk.Label(info_frame, text=f"Thể loại: {movie.get('genre', 'N/A')}", font=("Arial", 12)).grid(
            row=2, column=1, sticky="w", pady=3)
        
        tk.Label(info_frame, text=f"Đánh giá: {movie.get('rating', 'N/A')}/10", font=("Arial", 12)).grid(
            row=3, column=1, sticky="w", pady=3)
        
        tk.Label(info_frame, text=f"Đạo diễn: {movie.get('director', 'N/A')}", font=("Arial", 12)).grid(
            row=4, column=1, sticky="w", pady=3)
        
        # Mô tả phim
        description_frame = tk.Frame(main_frame)
        description_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(description_frame, text="Mô tả:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        description_text = tk.Text(description_frame, wrap=tk.WORD, height=5, font=("Arial", 11))
        description_text.pack(fill=tk.X, pady=5)
        description_text.insert(tk.END, movie.get("description", "Không có mô tả."))
        description_text.config(state=tk.DISABLED)
        
        # Frame xem phim
        player_frame = tk.Frame(main_frame, pady=10)
        player_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(player_frame, text="Phát phim", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        
        # Giả lập phát phim (sử dụng URL từ trường movie_url)
        movie_url = movie.get("movie_url", "")
        if movie_url:
            # Nếu có URL phim, tạo nút để mở trong trình duyệt
            play_button = tk.Button(player_frame, text="Phát phim trong trình duyệt", 
                                   bg="#4CAF50", fg="white", font=("Arial", 12),
                                   command=lambda: webbrowser.open(movie_url))
            play_button.pack(pady=10)
        else:
            # Nếu không có URL, hiển thị thông báo
            tk.Label(player_frame, text="Không có nguồn phim.", font=("Arial", 12)).pack(pady=10)
        
        # Thêm phim vào danh sách đã xem
        self.add_to_watched(movie)
    
    def add_to_watched(self, movie):
        # Thêm phim vào danh sách đã xem của người dùng
        try:
            watched_file = f"{self.current_user}_watched.json"
            watched_movies = []
            
            if os.path.exists(watched_file):
                with open(watched_file, 'r', encoding='utf-8') as file:
                    watched_movies = json.load(file)
            
            # Kiểm tra xem phim đã tồn tại trong danh sách chưa
            movie_id = movie.get("id", "")
            if not any(m.get("id", "") == movie_id for m in watched_movies):
                # Thêm mới nếu chưa tồn tại
                watched_movies.append(movie)
                
                with open(watched_file, 'w', encoding='utf-8') as file:
                    json.dump(watched_movies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi khi lưu phim đã xem: {str(e)}")
    
    def show_watched_movies(self):
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg="#f5f5f5", padx=20, pady=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="PHIM ĐÃ XEM", font=("Arial", 18, "bold"), 
                 bg="#f5f5f5").pack(anchor="w")
        
        # Tạo frame để hiển thị danh sách phim
        movies_frame = tk.Frame(self.content_frame, bg="#f5f5f5", padx=20, pady=10)
        movies_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tạo canvas để có thể scroll
        canvas = tk.Canvas(movies_frame, bg="#f5f5f5")
        scrollbar = ttk.Scrollbar(movies_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Đọc danh sách phim đã xem
        watched_file = f"{self.current_user}_watched.json"
        watched_movies = []
        
        if os.path.exists(watched_file):
            try:
                with open(watched_file, 'r', encoding='utf-8') as file:
                    watched_movies = json.load(file)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải danh sách phim đã xem: {str(e)}")
        
        # Hiển thị các phim trong lưới
        if not watched_movies:
            tk.Label(scrollable_frame, text="Bạn chưa xem phim nào!", font=("Arial", 14), 
                     bg="#f5f5f5", padx=20, pady=20).grid(row=0, column=0)
        else:
            # Hiển thị các phim trong lưới 4 cột
            row, col = 0, 0
            max_cols = 4
            
            for movie in watched_movies:
                self.create_movie_card(scrollable_frame, movie, row, col)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
    
    def show_search_screen(self):
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg="#f5f5f5", padx=20, pady=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="TÌM KIẾM PHIM", font=("Arial", 18, "bold"), 
                 bg="#f5f5f5").pack(anchor="w")
        
        # Tạo frame tìm kiếm
        search_frame = tk.Frame(self.content_frame, bg="#f5f5f5", padx=20, pady=10)
        search_frame.pack(fill=tk.X)
        
        # Ô tìm kiếm
        tk.Label(search_frame, text="Nhập tên phim:", font=("Arial", 12), 
                 bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Dropdown thể loại
        tk.Label(search_frame, text="Thể loại:", font=("Arial", 12), 
                 bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        
        # Lấy danh sách thể loại từ dữ liệu phim
        genres = set()
        for movie in self.movies:
            genre = movie.get("genre", "")
            if genre:
                # Xử lý trường hợp thể loại là chuỗi hoặc danh sách
                if isinstance(genre, list):
                    genres.update(genre)
                else:
                    # Nếu là chuỗi, tách bằng dấu phẩy
                    for g in genre.split(","):
                        genres.add(g.strip())
        
        genre_list = ["Tất cả"] + sorted(list(genres))
        self.genre_var = tk.StringVar(value="Tất cả")
        genre_dropdown = ttk.Combobox(search_frame, textvariable=self.genre_var, 
                                      values=genre_list, state="readonly", width=15)