import tkinter as tk
from logic.ids_solver import IDSSolver
from ui.board_widget import BoardWidget

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle IDS Visualizer")
        self.root.configure(bg="#2c3e50")
        
        self.is_auto_playing = False
        self.solution_path = []
        self.step_count = 0
        
        initial_board = (1, 2, 3, 
                         4, 5, 6, 
                         7, 8, 9) 
        
        self.solver = IDSSolver(initial_board)

        self.setup_ui()
        self.show_initial_state()

    def show_initial_state(self):
        self.node_center.update_board(self.solver.initial_node.board, highlight=True)
        self.frontier_boards[0].update_board(self.solver.initial_node.board)
        self.lbl_stats.config(text="Limit (l): 0 | Step: 0 | Frontier: 1")

    def setup_ui(self):
        # --- TOP FRAME: FRONTIER (HÀNG ĐỢI) ---
        self.frontier_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        self.frontier_frame.pack(fill=tk.X)
        
        tk.Label(self.frontier_frame, text="Frontier (Queue):", fg="white", bg="#2c3e50", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.frontier_boards = []
        for _ in range(5): 
            bw = BoardWidget(self.frontier_frame, size="mini")
            bw.pack(side=tk.LEFT, padx=5)
            self.frontier_boards.append(bw)

        # --- BODY FRAME (CHỨA KHU VỰC KHAI TRIỂN VÀ KHU VỰC KẾT QUẢ NẰM NGANG NHAU) ---
        self.body_frame = tk.Frame(self.root, bg="#2c3e50")
        self.body_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Khu vực bên trái: Khai triển (Expansion Area)
        self.expand_frame = tk.Frame(self.body_frame, bg="#34495e", padx=15, pady=15, relief=tk.SUNKEN, bd=3)
        self.expand_frame.grid(row=0, column=0, padx=10, sticky="nsew")

        self.node_up = BoardWidget(self.expand_frame, bd=4)
        self.node_up.grid(row=0, column=1, pady=5)

        self.node_left = BoardWidget(self.expand_frame, bd=4)
        self.node_left.grid(row=1, column=0, padx=5)

        self.node_center = BoardWidget(self.expand_frame, bd=4)
        self.node_center.grid(row=1, column=1, padx=15, pady=15)

        self.node_right = BoardWidget(self.expand_frame, bd=4)
        self.node_right.grid(row=1, column=2, padx=5)

        self.node_down = BoardWidget(self.expand_frame, bd=4)
        self.node_down.grid(row=2, column=1, pady=5)

        # Khu vực bên phải: Hiển thị đường đi kết quả (Solution Path)
        self.path_frame = tk.Frame(self.body_frame, bg="#34495e", padx=15, pady=15, relief=tk.SUNKEN, bd=3)
        self.path_frame.grid(row=0, column=1, padx=10, sticky="nsew")

        tk.Label(self.path_frame, text="Solution Path (Click to view):", fg="white", bg="#34495e", font=('Arial', 11, 'bold')).pack(pady=5)
        
        self.path_listbox = tk.Listbox(self.path_frame, font=('Arial', 10), bg="#2c3e50", fg="white", selectbackground="#e67e22", width=30, height=15)
        self.path_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.path_listbox.bind('<<ListboxSelect>>', self.on_path_select)

        self.body_frame.columnconfigure(0, weight=1)
        self.body_frame.columnconfigure(1, weight=1)

        # --- BOTTOM FRAME: ĐIỀU KHIỂN & THỐNG KÊ ---
        self.control_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        self.control_frame.pack(fill=tk.X)

        self.button_container = tk.Frame(self.control_frame, bg="#2c3e50")
        self.button_container.pack(anchor=tk.CENTER)

        self.btn_next = tk.Button(self.button_container, text="Next Step", command=self.next_step, 
                                  font=('Arial', 12, 'bold'), bg="#e67e22", fg="white", width=12)
        self.btn_next.grid(row=0, column=0, padx=10)

        self.btn_auto = tk.Button(self.button_container, text="Auto Play", command=self.toggle_auto_play, 
                                  font=('Arial', 12, 'bold'), bg="#2980b9", fg="white", width=12)
        self.btn_auto.grid(row=0, column=1, padx=10)

        self.lbl_stats = tk.Label(self.button_container, text="Reached: 0 | Frontier: 0", 
                                  fg="#bdc3c7", bg="#2c3e50", font=('Arial', 12))
        self.lbl_stats.grid(row=0, column=2, padx=15)
    
    def next_step(self):
        self.step_count += 1
        state_data = self.solver.step()
        self.update_ui_from_state(state_data)
    
    def colorize_node(self, widget, move_name, children_info):
        """Hàm nhuộm màu nền viền dựa vào trạng thái duyệt của Node"""
        if move_name not in children_info:
            widget.update_board(None) # Đường cụt -> Màu xám mặc định
            widget.config(bg="#2c3e50") 
            return
            
        info = children_info[move_name]
        board_data = info["node"].board
        widget.update_board(board_data)
        
        if info["type"] == "new":
            widget.config(bg="#2ecc71")      # Trạng thái mới thành màu xanh lá
        elif info["type"] == "reached":
            widget.config(bg="#e74c3c")      # Trạng thái đã có trong reached thì màu đỏ, không đưa vào frontier
        elif info["type"] == "success":
            widget.config(bg="#f1c40f")

    def update_ui_from_state(self, data):
        if data is None:
            return
            
        current_board = data["current"].board
        self.node_center.update_board(current_board, highlight=True)
        self.node_center.config(bg="#a55b00")

        # Xử lý khi thuật toán nâng giới hạn độ sâu l lên mức mới
        if data["status"] == "next_depth":
            # Làm trống các ô xung quanh
            for widget in [self.node_up, self.node_down, self.node_left, self.node_right]:
                widget.update_board(None)
                widget.config(bg="#2c3e50")
            self.lbl_stats.config(
                text=f"TĂNG GIỚI HẠN LÊN l = {data['current_l']}!", 
                fg="#f1c40f"
            )
            return

        if "children_info" in data:
            info = data["children_info"]
            self.colorize_node(self.node_up, 'UP', info)
            self.colorize_node(self.node_down, 'DOWN', info)
            self.colorize_node(self.node_left, 'LEFT', info)
            self.colorize_node(self.node_right, 'RIGHT', info)

        if data["status"] == "success":
            self.is_auto_playing = False
            self.btn_next.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED, text="Auto Play", bg="#2980b9")
            self.lbl_stats.config(text="ĐÃ TÌM THẤY ĐÍCH BẰNG IDS!!!", fg="#2ecc71")
            
            current_board = data["solution_node"].board
            self.node_center.update_board(current_board, highlight=True)
            self.node_center.config(bg="#f1c40f")
            
            for widget in [self.node_up, self.node_down, self.node_left, self.node_right]:
                widget.update_board(None)
                widget.config(bg="#2c3e50")
            
            self.solution_path = data["path"]
            self.path_listbox.delete(0, tk.END)
            for idx, node in enumerate(self.solution_path):
                move_val = getattr(node, 'move')
                move_str = f"Step {idx}: " + (str(move_val) if move_val else "START")
                self.path_listbox.insert(tk.END, move_str)
            return

        if data["status"] == "failure":
            self.lbl_stats.config(text="KHÔNG TÌM THẤY ĐƯỜNG ĐI!!!", fg="#e74c3c")
            self.btn_next.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED)
            return

        # Cập nhật frontier Queue/Stack
        frontier_list = data["frontier_preview"]
        for i in range(5):
            if i < len(frontier_list):
                self.frontier_boards[i].update_board(frontier_list[i])
            else:
                self.frontier_boards[i].update_board(None)

        # Hiển thị độ sâu giới hạn (l) hiện tại thay vì reached_count
        self.lbl_stats.config(
            text=f"Limit (l): {data['current_l']} | Step: {self.step_count} | Frontier: {data['frontier_count']}",
            fg="#bdc3c7"
        )
    
    def on_path_select(self, event):
        """Khi click vào một bước trong danh sách kết quả, ô trung tâm sẽ hiển thị cấu hình bước đó"""
        selection = self.path_listbox.curselection()
        if selection:
            index = selection[0]
            selected_node = self.solution_path[index]
            # Cập nhật ô giữa thành trạng thái của bước được chọn
            self.node_center.update_board(selected_node.board, highlight=True)
            self.node_center.config(bg="#f1c40f") 
            
            # Làm trống 4 ô xung quanh để tập đỡ rối mắt
            self.node_up.update_board(None)
            self.node_up.config(bg="#2c3e50")
            
            self.node_down.update_board(None)
            self.node_down.config(bg="#2c3e50")
            
            self.node_left.update_board(None)
            self.node_left.config(bg="#2c3e50")
            
            self.node_right.update_board(None)
            self.node_right.config(bg="#2c3e50")

    def toggle_auto_play(self):
        """Bật/Tắt chế độ tự động chạy"""
        if not self.is_auto_playing:
            self.is_auto_playing = True
            self.btn_auto.config(text="Stop Auto", bg="#c0392b") 
            self.btn_next.config(state=tk.DISABLED) 
            self.run_auto_step()
        else:
            self.is_auto_playing = False
            self.btn_auto.config(text="Auto Play", bg="#2980b9") 
            self.btn_next.config(state=tk.NORMAL) 

    def run_auto_step(self):
        """Vòng lặp tự động chạy mỗi 0.5 giây"""
        if self.is_auto_playing:
            self.step_count += 1
            state_data = self.solver.step()
            self.update_ui_from_state(state_data)
            
            if state_data and state_data["status"] not in ["success", "failure"]:
                self.root.after(500, self.run_auto_step)
            else:
                self.toggle_auto_play()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("760x520")
    app = MainWindow(root)
    root.mainloop()