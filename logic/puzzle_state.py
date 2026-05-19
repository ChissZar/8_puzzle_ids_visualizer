class PuzzleState:
    def __init__(self, board, parent=None, move=None):
        self.board = tuple(board)
        self.parent = parent
        self.move = move  
        # Độ sâu bằng độ sâu của cha cộng 1, nếu không có cha thì bằng 0
        self.depth = 0 if parent is None else parent.depth + 1

    def is_goal(self):
        return self.board == (1, 2, 3, 
                              8, 0, 4, 
                              7, 6, 5)

    def get_children(self):
        children = {}
        idx = self.board.index(0)
        r, c = divmod(idx, 3)
        
        # Giữ nguyên thứ tự trượt đảo ngược để ưu tiên L R U D trong Stack LIFO
        moves = {
            'DOWN': (1, 0),
            'UP': (-1, 0),
            'RIGHT': (0, 1),
            'LEFT': (0, -1)
        }

        for move_name, (dr, dc) in moves.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_idx = nr * 3 + nc
                new_board = list(self.board)
                new_board[idx], new_board[new_idx] = new_board[new_idx], new_board[idx]
                children[move_name] = PuzzleState(new_board, self, move_name)
                
        return children

    def is_cycle(self):
        """Kiểm tra xem trạng thái này đã từng xuất hiện trong nhánh đi từ gốc chưa"""
        current = self.parent
        while current is not None:
            if current.board == self.board:
                return True
            current = current.parent
        return False