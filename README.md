# 8_puzzle_ids_visualizer
Dự án trực quan hóa thuật toán Tìm kiếm theo chiều sâu dần (Iterative-Deepening Search - IDS) để giải bài toán 8-Puzzle. Đây là bài tập cho môn học **Trí tuệ nhân tạo**.

## Thông tin sinh viên
* **Họ và tên:** Nguyễn Phước Minh Triết
* **Mã số sinh viên (MSSV):** 24110357
* **Giảng viên:** TS. Phan Thị Huyền Trang
* **Mã lớp học phần:** 252ARIN330585_08
* **Trường:** Đại học Công nghệ Kỹ thuật TP.HCM (HCMUTE)
* **Link Github bài tập:** https://github.com/ChissZar/8_puzzle_bfs_visualizer

---

## Cấu trúc thư mục dự án
Dự án được thiết kế theo mô hình tách biệt rõ ràng giữa Logic toán học (Thuật toán) và Giao diện người dùng (UI):

```text
8_puzzle_ids_visualizer/
│
├── main.py                # Điểm bắt đầu (Entry point) để kích hoạt ứng dụng
│
├── logic/                 # Thư mục chứa thuần logic thuật toán
│   ├── __init__.py
│   ├── puzzle_state.py    # Định nghĩa cấu trúc Node, các bước di chuyển hợp lệ
│   └── ids_solver.py      # Trái tim của thuật toán IDS
│
└── ui/                    # Thư mục quản lý toàn bộ giao diện Tkinter
    ├── __init__.py
    ├── main_window.py     # Sân khấu chính, bố cục Frontier, khu vực Expansion và Controls
    └── board_widget.py    # Thành phần (Component) vẽ ma trận 3x3 tái sử dụng liên tục
```
## Hướng dẫn cài đặt và khởi chạy
**1. Yêu cầu hệ thống**

- Máy tính đã cài đặt sẵn Python 3.x.

- Dự án này sử dụng thư viện giao diện đồ họa Tkinter (thư viện core đã được tích hợp sẵn khi cài đặt Python, không cần cài thêm từ bên ngoài).

**2. Cách khởi chạy chương trình**
- Để tránh lỗi nạp gói dữ liệu (ImportError), bạn cần đảm bảo rằng VS Code hoặc Terminal của bạn đang mở chính xác tại thư mục dự án.

- Mở Terminal hoặc Command Prompt lên.

- Di chuyển vào thư mục gốc của dự án:

`
cd đường_dẫn_đến_thư_mục/8_puzzle_ids_visualizer
`

- Khởi chạy ứng dụng bằng lệnh:

`
python main.py
`
## Hướng dẫn tùy chỉnh cấu hình Trạng thái (Quan trọng)

Để thay đổi các bài toán test hoặc cấu hình lại trò chơi, bạn có thể chỉnh sửa trực tiếp trong mã nguồn theo các lưu ý sau:

- **1/ Thay đổi Trạng thái Đích (Goal State).**<br>

    - Vị trí file: **logic/puzzle_state.py**

    - Nơi chỉnh sửa: Bên trong lớp PuzzleState, tìm hàm is_goal(self).

    - Cách sửa: Thay đổi mảng Tuple 1 chiều đại diện cho 9 ô số (với số 0 là ô trống) theo ý muốn.

    - Ví dụ cấu hình đích mặc định: 1 2 3, 4 5 6, 7 8 0

```text
def is_goal(self):
        return self.board = (1, 2, 3, 
                             4, 5, 6, 
                             7, 8, 0)
```

- **2/ Thay đổi Trạng thái Ban đầu (Initial State)**<br>
    - Vị trí file: ui/main_window.py

    - Nơi chỉnh sửa: Bên trong lớp MainWindow, tìm hàm khởi tạo __init__(self, root).

    - Cách sửa: Thay đổi giá trị của biến initial_board.

    - Ví dụ cấu hình trạng thái ban đầu cần giải:

```text
initial_board = (2, 8, 3, 
                 1, 6, 4,
                 7, 0, 5)
```

---

## Các tính năng chính trên UI
- Frontier (Stack): Hiển thị hàng ngang 5 ma trận mini đại diện cho các trạng thái đang nằm đầu hàng đợi LIFO, chuẩn bị được lấy ra xét với độ sâu l.
 
- Khu vực Expansion: Trực quan hóa hàm EXPAND. Ô trung tâm màu cam là Node đang xét, 4 ô xung quanh đại diện cho 4 hướng trượt (Lên, Xuống, Trái, Phải). Ô nào bị làm mờ xám nghĩa là hướng đi đó bị cụt (không hợp lệ). Ô viền xanh nghĩa là trạng thái hợp lệ có thể đưa vào frontier. Ô viền đỏ có nghĩa là trạng thái đã có trong reached nên không đưa vào frontier nữa.

- Next Step: Bấm chuột để AI tính toán và nhảy từng bước một theo đúng tiến trình thuật toán BFS.

- Auto Play: AI tự động giải liên tục mỗi 0.5 giây. Nút bấm sẽ đổi sang màu đỏ ("Stop Auto") cho phép tạm dừng bất cứ lúc nào.

- Thống kê thời gian thực: Cập nhật liên tục số lượng trạng thái duy nhất đã duyệt (Reached) và số lượng trạng thái đang xếp hàng chờ (Frontier).

- Truy vết đường đi: Khi thuật toán tìm thấy đích, hệ thống tận dụng thuộc tính Node cha (`parent`) để truy vết ngược từ Node Đích về Node Gốc, từ đó xuất ra danh sách các bước di chuyển chi tiết ở khung bên phải màn hình.

- Chế độ xem lại: Người dùng có thể click chuột vào từng bước đi trong danh sách kết quả (Solution Path) chương trình sẽ tự động khôi phục lại chính xác cấu hình ma trận tại bước đi đó.

- Xử lý ngoại lệ: Thuật toán được xây dựng chặt chẽ cùng bộ đếm bước lặp. Đối với các thế cờ vô nghiệm, hệ thống sẽ tự động vét cạn mọi trường hợp hợp lệ và dừng chương trình an toàn, hiển thị thông báo thất bại thay vì bị treo máy.
