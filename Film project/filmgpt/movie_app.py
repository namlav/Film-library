import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import requests
# Nếu cần crawl dữ liệu từ HTML, có thể dùng BeautifulSoup:
# from bs4 import BeautifulSoup

# ---------- CÁC HÀM HỖ TRỢ FILE JSON ----------
def load_json(file_path):
    """Đọc dữ liệu từ file JSON. Nếu file không tồn tại thì trả về dữ liệu mặc định."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(file_path, data):
    """Ghi dữ liệu vào file JSON."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------- CÁC HÀM QUẢN LÝ NGƯỜI DÙNG ----------
def load_users():
    """Đọc dữ liệu người dùng từ file JSON."""
    if not os.path.exists("users.json"):
        # Tạo file với một admin mặc định nếu chưa tồn tại
        default_users = [
            {"username": "admin", "password": "admin123", "role": "admin"},
            {"username": "user", "password": "user123", "role": "user"}
        ]
        save_json("users.json", default_users)
        return default_users
    return load_json("users.json")

def check_login(username, password):
    """Kiểm tra đăng nhập và trả về role nếu thành công."""
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user["role"]
    return None

# ---------- CHỨC NĂNG CRAWL / CALL API ----------
def fetch_movies_from_api():
    """
    Ví dụ sử dụng API lấy dữ liệu phim.
    Ở đây sử dụng một API mẫu hoặc bạn có thể dùng requests.get đến URL API thật.
    """
    try:
        # Ví dụ gọi API (API mẫu dưới đây có thể thay đổi)
        response = requests.get("https://api.sampleapis.com/movies/action")
        if response.status_code == 200:
            movies = response.json()
            # Lấy một số thông tin cần thiết của từng phim
            processed_movies = []
            for movie in movies:
                processed_movies.append({
                    "id": movie.get("id", ""),
                    "title": movie.get("title", "Chưa có tiêu đề"),
                    "year": movie.get("year", "N/A"),
                    "description": movie.get("description", "")
                })
            return processed_movies
        else:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ API!")
            return []
    except Exception as e:
        messagebox.showerror("Lỗi", f"Exception: {str(e)}")
        return []

# ---------- LỚP ỨNG DỤNG CHÍNH ----------
class MovieApp:
    def __init__(self, master, user_role):
        self.master = master
        self.user_role = user_role
        self.master.title("Ứng dụng Xem Phim")
        self.file_path = "movies.json"
        self.movies = load_json(self.file_path)
        
        # Frame chứa danh sách phim và nút chức năng
        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        # Danh sách phim
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Title", "Year"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Tiêu đề")
        self.tree.heading("Year", text="Năm")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.load_treeview()

        # Scrollbar cho treeview
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Nút chức năng
        self.btn_frame = tk.Frame(master)
        self.btn_frame.pack(pady=10)

        self.btn_create = tk.Button(self.btn_frame, text="Thêm mới", command=self.create_movie)
        self.btn_create.grid(row=0, column=0, padx=5)

        self.btn_update = tk.Button(self.btn_frame, text="Cập nhật", command=self.update_movie)
        self.btn_update.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(self.btn_frame, text="Xóa", command=self.delete_movie)
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_fetch = tk.Button(self.btn_frame, text="Lấy dữ liệu từ API", command=self.fetch_data)
        self.btn_fetch.grid(row=0, column=3, padx=5)

        # Phân quyền: Nếu người dùng là user thường, có thể ẩn đi một số chức năng (ví dụ: cập nhật và xóa)
        if self.user_role != "admin":
            self.btn_update.config(state="disabled")
            self.btn_delete.config(state="disabled")

    def load_treeview(self):
        """Load dữ liệu phim lên treeview"""
        # Xóa dữ liệu cũ
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Thêm dữ liệu mới
        for movie in self.movies:
            self.tree.insert("", tk.END, values=(movie.get("id", ""), movie.get("title", ""), movie.get("year", "")))

    def create_movie(self):
        """Thêm mới một phim"""
        new_id = simpledialog.askstring("Nhập ID", "Nhập ID của phim:")
        new_title = simpledialog.askstring("Nhập tiêu đề", "Nhập tiêu đề của phim:")
        new_year = simpledialog.askstring("Nhập năm", "Nhập năm sản xuất:")
        new_desc = simpledialog.askstring("Nhập mô tả", "Nhập mô tả phim:")

        if new_id and new_title:
            new_movie = {"id": new_id, "title": new_title, "year": new_year, "description": new_desc}
            self.movies.append(new_movie)
            save_json(self.file_path, self.movies)
            self.load_treeview()
            messagebox.showinfo("Thành công", "Đã thêm phim mới!")
        else:
            messagebox.showerror("Lỗi", "ID và tiêu đề không được để trống.")

    def update_movie(self):
        """Cập nhật thông tin phim đã chọn (chỉ admin)"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn phim cần cập nhật.")
            return
        item = self.tree.item(selected)
        movie_id = item["values"][0]
        # Tìm phim theo id
        for movie in self.movies:
            if movie["id"] == movie_id:
                new_title = simpledialog.askstring("Cập nhật tiêu đề", "Nhập tiêu đề mới:", initialvalue=movie["title"])
                new_year = simpledialog.askstring("Cập nhật năm", "Nhập năm mới:", initialvalue=movie["year"])
                new_desc = simpledialog.askstring("Cập nhật mô tả", "Nhập mô tả mới:", initialvalue=movie["description"])
                if new_title:
                    movie["title"] = new_title
                    movie["year"] = new_year
                    movie["description"] = new_desc
                    save_json(self.file_path, self.movies)
                    self.load_treeview()
                    messagebox.showinfo("Thành công", "Đã cập nhật phim!")
                else:
                    messagebox.showerror("Lỗi", "Tiêu đề không được để trống!")
                break

    def delete_movie(self):
        """Xóa phim đã chọn (chỉ admin)"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn phim cần xóa.")
            return
        item = self.tree.item(selected)
        movie_id = item["values"][0]
        # Xác nhận xóa
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phim này?"):
            self.movies = [m for m in self.movies if m.get("id") != movie_id]
            save_json(self.file_path, self.movies)
            self.load_treeview()
            messagebox.showinfo("Thành công", "Đã xóa phim!")

    def fetch_data(self):
        """Lấy dữ liệu phim từ API hoặc crawl website và cập nhật vào file JSON"""
        new_movies = fetch_movies_from_api()
        if new_movies:
            # Gộp dữ liệu mới với dữ liệu hiện có (có thể cần kiểm tra trùng ID)
            for nm in new_movies:
                if not any(m.get("id") == nm.get("id") for m in self.movies):
                    self.movies.append(nm)
            save_json(self.file_path, self.movies)
            self.load_treeview()
            messagebox.showinfo("Thành công", "Đã cập nhật dữ liệu phim từ API!")

# ---------- CỬA SỔ ĐĂNG NHẬP ----------
class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng nhập")
        self.master.geometry("300x150")
        
        self.lbl_user = tk.Label(master, text="Username:")
        self.lbl_user.pack(pady=5)
        self.entry_user = tk.Entry(master)
        self.entry_user.pack(pady=5)
        
        self.lbl_pass = tk.Label(master, text="Password:")
        self.lbl_pass.pack(pady=5)
        self.entry_pass = tk.Entry(master, show="*")
        self.entry_pass.pack(pady=5)
        
        self.btn_login = tk.Button(master, text="Đăng nhập", command=self.login)
        self.btn_login.pack(pady=10)
    
    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        role = check_login(username, password)
        if role:
            messagebox.showinfo("Thành công", f"Đăng nhập thành công! Quyền: {role}")
            self.master.destroy()
            root = tk.Tk()
            app = MovieApp(root, role)
            root.mainloop()
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")

# ---------- CHƯƠNG TRÌNH CHÍNH ----------
if __name__ == "__main__":
    # Khởi chạy cửa sổ đăng nhập trước
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()

'''
Dùng pyinstaller để đóng gói với lệnh:
pyinstaller --onefile --noconsole tên_app.py
'''