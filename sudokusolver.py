import tkinter as tk
import random
from tkinter import PhotoImage, messagebox
from collections import deque

# Membuat Jendela Tkinter 
root = tk.Tk()
root.title("Sudoku Solver ! (KELOMPOK 4)")

# warna dasar background
root.configure(bg='lightblue')

# Menambahkan gambar latar belakang
background_image = PhotoImage(file="desktop11.png")  # Ganti dengan path gambar Anda
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)  # Gambar akan mencakup seluruh jendela

# Membuat windows menjadi fullscreen
root.geometry('800x1000')

screen_width = root.winfo_screenwidth()  # Lebar layar
screen_height = root.winfo_screenheight()  # Tinggi layar

# Menghitung posisi x dan y untuk menempatkan jendela di tengah
position_top = int(screen_height /  2 - 850 / 2)  # 850 adalah tinggi jendela
position_right = int(screen_width / 2 - 800 / 2)  # 800 adalah lebar jendela

# Menetapkan posisi jendela di tengah
root.geometry(f'800x1000+{position_right}+{position_top}')

# Membuat Class
class SudokuSolver:
    def __init__(self, master):
        self.master = master

        # Frame untuk grid Sudoku
        self.grid_frame = tk.Frame(master, bg="white")
        self.grid_frame.place(relx=0.5, rely=0.45, anchor="center")

        self.cells = {}  # Menyimpan semua kotak Entry
        self.stack = deque()  # Stack untuk backtracking
        cell_size = 50

        # Membuat grid 9x9
        for row in range(9):
            for col in range(9):
                color = 'black'  
                cell = tk.Frame(self.grid_frame, highlightbackground=color, highlightcolor=color, 
                                 highlightthickness=2, width=cell_size, height=cell_size, background='white')
                cell.grid(row=row, column=col, padx=0, pady=0)
                
                entry = tk.Entry(
                    self.grid_frame, 
                    width=2, 
                    font=("Doto Extrabold", 18, 'bold'), 
                    fg='green',
                    justify="center",   
                    bg='white',  
                    bd=0,
                    validate="key", 
                    validatecommand=(master.register(self.validate_input), "%P")
                )
                entry.grid(row=row, column=col, padx=0, pady=0)
                self.cells[(row, col)] = entry

        # Button style
        button_style = {
            'highlightthickness': 0,
            'activebackground': '#D3D3D3',  
            'activeforeground': '#000000',
            'width': 6,  
            'height': 1,
        }

        # Tombol Solve
        solve_btn = tk.Button(master, text="SOLVE", command=self.solve, font=("Doto Extrabold", 16,'bold'), bg="#72BF78", fg="white",**button_style)
        solve_btn.place(relx=0.35, rely=0.85 ,anchor='center')

        # Tombol Visual Solve
        visual_btn = tk.Button(master, text="VISUAL", command=self.visual_solve, font=("Doto Extrabold", 16,'bold'), bg="#1F509A", fg="white",**button_style)
        visual_btn.place(relx=0.5, rely=0.85,anchor='center' )

        # Tombol Clear
        clear_btn = tk.Button(master, text="CLEAR", command=self.clear_board, font=("Doto Extrabold", 16,'bold'), bg="#AF1740", fg="white",**button_style)
        clear_btn.place(relx=0.65, rely=0.85, anchor='center')

        # Mengikat tombol panah ke fungsi move_focus
        master.bind("<KeyPress>", self.move_focus)

    def validate_input(self, value):
        # Validasi hanya angka 1-9 yang bisa diinput
        if value == "" or (value.isdigit() and 1 <= int(value) <= 9):
            return True
        return False

    def get_board(self):
        # Mengubah isi grid menjadi list of lists
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.cells[(row, col)].get()
                current_row.append(int(value) if value.isdigit() else 0)
            board.append(current_row)
        return board

    def is_valid_move(self, board, row, col, num):
        # Periksa baris
        if num in board[row]:
            return False
        # Periksa kolom
        if num in [board[r][col] for r in range(9)]:
            return False
        # Periksa kotak 3x3
        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                if board[r][c] == num:
                    return False
        return True

    def solve_board(self, board):
        # Backtracking solver
        colors = ['red', 'blue', '#740938', '#AF1740',]
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(board, row, col, num):
                            random_color = random.choice(colors)
                            self.cells[(row, col)].config(fg=random_color)
                            board[row][col] = num
                            if self.solve_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def solve(self):
        board = self.get_board()
        
        # Validasi board awal
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != 0:
                    board[row][col] = 0
                    if not self.is_valid_move(board, row, col, num):
                        messagebox.showerror("Error", "Board tidak valid!")
                        return
                    board[row][col] = num

        # Solve Sudoku
        if self.solve_board(board):
            self.update_board(board)
        else:
            messagebox.showerror("Error", "Tidak ada solusi untuk board ini!")

    def visual_solve(self):
        board = self.get_board()

        # Validasi board awal
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != 0:
                    board[row][col] = 0
                    if not self.is_valid_move(board, row, col, num):
                        messagebox.showerror("Error", "Board tidak valid!")
                        return
                    board[row][col] = num

        # Solve Sudoku dengan animasi
        if not self.solve_board_visual(board):
            messagebox.showerror("Error", "Tidak ada solusi untuk board ini!")

    def solve_board_visual(self, board):
        colors = ['red', 'blue', '#740938', '#AF1740',]
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(board, row, col, num):
                            board[row][col] = num
                            self.cells[(row, col)].delete(0, tk.END)
                            self.cells[(row, col)].insert(0, str(num))
                            
                            random_color = random.choice(colors)
                            self.cells[(row, col)].config(fg=random_color)

                            root.update()
                            if self.solve_board_visual(board):
                                return True
                            board[row][col] = 0
                            self.cells[(row, col)].delete(0, tk.END)
                            root.update()
                    return False
        return True

    def update_board(self, board):
        # Update board di UI
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, tk.END)
                if board[row][col] != 0:
                    self.cells[(row, col)].insert(0, str(board[row][col]))

    def clear_board(self):
        # Kosongkan semua kotak
        for row in range(9):
            for col in range(9):
                self.cells[(row,col)].config(fg='green')
                self.cells[(row, col)].delete(0, tk.END)

    def move_focus(self, event):
        current_row, current_col = self.get_current_focus()
        
        if event.keysym == "Up" and current_row > 0:
            self.cells[( current_row - 1, current_col)].focus_set()
        elif event.keysym == "Down" and current_row < 8:
            self.cells[(current_row + 1, current_col)].focus_set()
        elif event.keysym == "Left" and current_col > 0:
            self.cells[(current_row, current_col - 1)].focus_set()
        elif event.keysym == "Right" and current_col < 8:
            self.cells[(current_row, current_col + 1)].focus_set()

    def get_current_focus(self):
        for (row, col), entry in self.cells.items():
            if entry.focus_get() == entry:
                return row, col
        return 0, 0  # Default ke (0, 0) jika tidak ada fokus

SudokuSolver(root)
root.mainloop()