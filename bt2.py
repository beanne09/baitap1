import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Kết nối tới cơ sở dữ liệu và tạo bảng nếu chưa tồn tại
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Tạo bảng người dùng
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL
                 )''')

    # Tạo bảng sách
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL
                 )''')

    # Thêm người dùng mặc định
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password')")

    conn.commit()
    conn.close()

# Đăng nhập
def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Kiểm tra thông tin đăng nhập
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    conn.close()

    if user:
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        main_menu()  # Chuyển sang giao diện chính sau khi đăng nhập thành công
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu.")

# Giao diện chức năng tìm kiếm sách
def search_books():
    keyword = entry_search.get()

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Tìm kiếm sách
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
    results = c.fetchall()

    conn.close()

    listbox_books.delete(*listbox_books.get_children())
    if results:
        for book in results:
            listbox_books.insert("", tk.END, values=(book[0], book[1], book[2]))
    else:
        messagebox.showinfo("Thông báo", "Không tìm thấy sách nào phù hợp.")

# Giao diện chức năng thêm sách
def add_book():
    title = entry_title.get()
    author = entry_author.get()

    if not title or not author:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        return

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Thêm sách mới
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))

    conn.commit()
    conn.close()

    messagebox.showinfo("Thành công", f"Đã thêm sách: {title} của tác giả {author}")

# Xóa sách được chọn
def delete_book():
    selected_item = listbox_books.selection()  # Lấy mục sách đang chọn
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần xóa.")
        return

    book_id = listbox_books.item(selected_item, 'values')[0]  # Lấy ID sách

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Xóa sách khỏi cơ sở dữ liệu
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    # Cập nhật lại bảng hiển thị
    listbox_books.delete(selected_item)
    messagebox.showinfo("Thành công", "Đã xóa sách thành công.")

# Giao diện chính sau khi đăng nhập thành công
def main_menu():
    login_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)

# Khởi tạo giao diện đăng nhập
def init_login_window():
    global entry_username, entry_password, login_frame

    login_frame = tk.Frame(root, bg="#e6f2ff")  # Màu nền sáng cho cửa sổ đăng nhập
    login_frame.pack(fill="both", expand=True, padx=20, pady=20)

    lbl_title = tk.Label(login_frame, text="Quản lý sách", font=("Arial", 18, "bold"), bg="#e6f2ff", fg="#003366")
    lbl_title.pack(pady=10)

    lbl_username = tk.Label(login_frame, text="Tên đăng nhập:", font=("Arial", 12), bg="#e6f2ff", fg="#003366")
    lbl_username.pack(pady=5)
    entry_username = ttk.Entry(login_frame, font=("Arial", 12), width=30)
    entry_username.pack(pady=5)

    lbl_password = tk.Label(login_frame, text="Mật khẩu:", font=("Arial", 12), bg="#e6f2ff", fg="#003366")
    lbl_password.pack(pady=5)
    entry_password = ttk.Entry(login_frame, show="*", font=("Arial", 12), width=30)
    entry_password.pack(pady=5)

    btn_login = ttk.Button(login_frame, text="Đăng nhập", command=login, style="TButton")
    btn_login.pack(pady=20)

# Khởi tạo giao diện chính (menu)
def init_menu_window():
    global entry_search, listbox_books, entry_title, entry_author, menu_frame

    menu_frame = tk.Frame(root, bg="#f0f8ff")  # Màu nền nhẹ cho cửa sổ menu chính

    # Tìm kiếm sách
    lbl_search = tk.Label(menu_frame, text="Tìm kiếm sách:", font=("Arial", 12), bg="#f0f8ff", fg="#003366")
    lbl_search.grid(row=0, column=0, pady=10, padx=10, sticky="w")
    entry_search = ttk.Entry(menu_frame, font=("Arial", 12), width=30)
    entry_search.grid(row=0, column=1, padx=10)
    btn_search = ttk.Button(menu_frame, text="Tìm kiếm", command=search_books)
    btn_search.grid(row=0, column=2, padx=10)

    # Nút xóa kết quả tìm kiếm
    btn_clear = ttk.Button(menu_frame, text="Xóa kết quả", command=lambda: listbox_books.delete(*listbox_books.get_children()))
    btn_clear.grid(row=0, column=3, padx=10)

    # Bảng hiển thị kết quả tìm kiếm
    columns = ('ID', 'Tên sách', 'Tác giả')
    listbox_books = ttk.Treeview(menu_frame, columns=columns, show='headings', height=10)
    listbox_books.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
    listbox_books.heading('ID', text='ID')
    listbox_books.heading('Tên sách', text='Tên sách')
    listbox_books.heading('Tác giả', text='Tác giả')

    # Nút xóa sách
    btn_delete = ttk.Button(menu_frame, text="Xóa sách", command=delete_book)
    btn_delete.grid(row=2, column=2, pady=10)

    # Thêm sách mới
    lbl_title = tk.Label(menu_frame, text="Tên sách:", font=("Arial", 12), bg="#f0f8ff", fg="#003366")
    lbl_title.grid(row=3, column=0, pady=10, padx=10, sticky="w")
    entry_title = ttk.Entry(menu_frame, font=("Arial", 12), width=30)
    entry_title.grid(row=3, column=1, padx=10)

    lbl_author = tk.Label(menu_frame, text="Tác giả:", font=("Arial", 12), bg="#f0f8ff", fg="#003366")
    lbl_author.grid(row=4, column=0, pady=10, padx=10, sticky="w")
    entry_author = ttk.Entry(menu_frame, font=("Arial", 12), width=30)
    entry_author.grid(row=4, column=1, padx=10)

    btn_add = ttk.Button(menu_frame, text="Thêm sách", command=add_book)
    btn_add.grid(row=5, column=1, pady=20)

    # Thoát ứng dụng
    btn_exit = ttk.Button(menu_frame, text="Thoát", command=root.quit)
    btn_exit.grid(row=6, column=1, pady=10)

# Khởi tạo cửa sổ giao diện
root = tk.Tk()
root.title("Ứng dụng Quản lý Sách")
root.geometry("600x500")
root.configure(bg="#f0f8ff")  # Màu nền sáng và dễ nhìn

# Khởi tạo database
init_db()

# Khởi tạo giao diện đăng nhập và menu
init_login_window()
init_menu_window()

# Chạy ứng dụng
root.mainloop()
