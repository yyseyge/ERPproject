import tkinter as tk
import tkinter.messagebox as msgbox

from color import Color

# 최종 수정일 250306 11:08
class TableWidget(tk.Frame):
    def __init__(self, master, data=None, col_name=None, col_width=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.col_name = [] # 열 이름
        self.data = {} # 데이터
        self.last_index = 0 # 데이터 마지막 행 번호

        self.rows = 0 # 행 개수
        self.cols = 0 # 열 개수 (체크박스 포함)
        self.selected_row = 0 # 선택된 행
        self.selected_col = 0 # 선택된 열

        self.origin_cell_width = 40 # 기준 셀 너비
        self.origin_cell_height = 30 # 기준 셀 높이
        self.checkbox_cell_width = 30 # 체크박스 셀 너비

        self.col_widths = [self.checkbox_cell_width] # 셀 너비
        self.cell_height = 30 # 셀 높이

        self.width = kwargs.get("width", self.origin_cell_width + self.checkbox_cell_width) # 프레임 너비
        self.height = kwargs.get("height", self.origin_cell_height + self.cell_height) # 프레임 높이

        self.start_row = 0 # canvas에 보여질 첫 행 번호
        self.row_count = (self.height - self.origin_cell_height) // self.cell_height # canvas에 보여질 행 개수

        self.entry = None # 수정할 때 나타날 entry
        self.is_editing = False  # Entry 위젯이 활성화 여부

        self.scroll_h = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height - self.scroll_h.winfo_height())  # canvas

        self.scroll_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_h.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.scroll_h.set)
        self.canvas.pack()
        self.focus = True # 현재 포커스 여부

        self.changed = { # 원본 데이터 대비 바뀐 행들
            "updated": {},
            "added": {},
            "deleted": {}
        }

        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<Up>", lambda e: self.move_up())
        self.bind("<Down>", lambda e: self.move_down())
        self.bind("<Left>", lambda e: self.move_left())
        self.bind("<Right>", lambda e: self.move_right())
        self.bind("<Return>", lambda e: self.edit_cell())
        self.canvas.bind("<MouseWheel>", lambda e: self.on_scroll(e))
        self.bind("<F7>", lambda e: self.delete_row())

        self.from_data(data=data, col_name=col_name, col_width=col_width)
    
    # 특정 list로 테이블 만들기
    def from_data(self, data: list[list], col_name: list[str] = None, col_width: list[int] = None):
        self.data = {
            i: {
                "checked": False,
                "data": [j for j in d]
            }  for i, d in enumerate(data) # 원본 데이터 유지
        }
        self.last_index = len(data) - 1
        if col_name is None:
            self.col_name = [f"Col{i + 1}" for i in range(len(data[0]))]
        else:
            self.col_name = col_name
        if col_width is None:
            self.col_widths = [self.checkbox_cell_width] + [(self.width - self.origin_cell_width - self.checkbox_cell_width) / len(data[0]) for _ in range(len(data[0]))]
        else:
            self.col_widths = [self.checkbox_cell_width] + col_width
        self.rows = len(data)
        self.cols = len(data[0]) + 1
        self.changed = {
            "updated": {},
            "added": {},
            "deleted": {}
        }
        self.canvas.config(scrollregion=(0, 0, self.origin_cell_width + sum(self.col_widths), self.origin_cell_height + self.rows * self.cell_height))

        self.add_row()
        self.draw_table()
    
    # index로부터 key 찾기 
    def get_key(self, index):
        return list(self.data.keys())[index]
    
    # 셀의 row col index로 데이터 값 찾기
    def get_data_from_cell(self, row, col=None):
        if col is None:
            return self.data[self.get_key(row)]["data"]
        return self.data[self.get_key(row)]["data"][col - 1]

    # 셀의 row col index로 데이터 값 설정
    def set_data_from_cell(self, row, col, value):
        self.data[self.get_key(row)]["data"][col - 1] = value

    # 데이터의 key로부터 데이터 값 찾기
    def get_data_from_key(self, key, col=None):
        if col is None:
            return self.data[key]["data"]
        return self.data[key]["data"][col]

    # 셀의 row index의 체크 여부
    def is_checked(self, row):
        return self.data[self.get_key(row)]["checked"]

    # 셀의 row index의 체크 토글
    def toggle_check(self, row):
        self.data[self.get_key(row)]["checked"] = not self.data[self.get_key(row)]["checked"]
    
    # 맨 아래 빈 줄 추가
    def add_row(self):
        self.last_index += 1
        self.data[self.last_index] = {
            "checked": False,
            "data": ["" for _ in range(self.cols - 1)]
        }
        self.changed["added"][self.last_index] = self.data[self.last_index]["data"]
        self.rows += 1
    
    # 테이블 그리기
    def draw_table(self):
        self.canvas.delete("all") # 이전 그려진 내용을 지움

        # 체크박스 열
        self.canvas.create_rectangle(self.origin_cell_width, 0, self.origin_cell_width + self.checkbox_cell_width, self.origin_cell_height, outline=Color.BLACK, fill=Color.FOCUS, tags="header")

        # 열 이름
        current_x = self.origin_cell_width + self.checkbox_cell_width
        for col in range(1, self.cols):
            x1 = current_x
            x2 = x1 + self.col_widths[col]
            self.canvas.create_rectangle(x1, 0, x2, self.origin_cell_height, outline=Color.BLACK, fill=Color.FOCUS, tags="header")
            self.canvas.create_text(x1 + self.col_widths[col] / 2, 0 + self.cell_height / 2, text=self.col_name[col - 1], tags="header")
            current_x = x2
        
        # canvas에 보이는 각 행
        for row in range(self.row_count):
            current_row = self.start_row + row
            if current_row >= len(self.data):
                break
            
            # 행 번호
            y1 = self.origin_cell_height + row * self.cell_height
            y2 = y1 + self.cell_height

            self.canvas.create_rectangle(0, y1, self.origin_cell_width, y2, outline=Color.BLACK, fill=Color.FOCUS, tags="header")
            self.canvas.create_text(0 + self.origin_cell_width / 2, y1 + self.origin_cell_height / 2, text=str(self.start_row + row + 1), tags="header")

            # 체크박스 셀
            if current_row < self.rows:
                self.canvas.create_rectangle(self.origin_cell_width, y1, self.origin_cell_width + self.checkbox_cell_width, y2, outline=Color.BLACK, fill=Color.GRAY if current_row == self.selected_row else Color.WHITE, tags="cell")
                self.draw_checkbox(self.origin_cell_width + 10, y1 + 10, self.is_checked(current_row))

            # 데이터 셀
            current_x = self.origin_cell_width + self.checkbox_cell_width
            for col in range(1, self.cols):
                x1 = current_x
                x2 = x1 + self.col_widths[col]

                self.canvas.create_rectangle(x1, y1, x2, y2, outline=Color.BLACK, fill=Color.GRAY if current_row == self.selected_row else Color.WHITE, tags="cell")
                self.canvas.create_text(x1 + 5, y1 + self.cell_height / 2, text=self.get_data_from_cell(current_row, col), tags="text", anchor="w")
                current_x = x2

        # 선택된 셀 강조
        if self.start_row <= self.selected_row < self.start_row + self.row_count:
            x1 = self.origin_cell_width + sum(self.col_widths[:self.selected_col])
            y1 = (self.selected_row - self.start_row) * self.cell_height + self.origin_cell_height
            x2 = x1 + self.col_widths[self.selected_col]
            y2 = y1 + self.cell_height
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=Color.BUTTON, width=2, tags="highlight")
    
    # 체크박스 그리기
    def draw_checkbox(self, x, y, checked=False):
        self.canvas.create_rectangle(x, y, x + 10, y + 10, outline=Color.BLACK, fill=Color.BLACK if checked else Color.WHITE, width=2)

    # 위 키 눌렀을 때
    def move_up(self):
        if self.is_editing:
            return
        if self.selected_row > 0:
            if self.selected_row == self.start_row:
                self.start_row -= 1
            self.selected_row -= 1
            self.draw_table()

    # 아래 키 눌렀을 때
    def move_down(self):
        if self.is_editing:
            return
        if self.selected_row < self.rows - 1:
            if self.selected_row == self.start_row + self.row_count - 1:
                self.start_row += 1
            self.selected_row += 1
            self.draw_table()

    # 왼쪽 키 눌렀을 때
    def move_left(self):
        if self.is_editing:
            return
        if self.selected_col > 0:
            self.selected_col -= 1
            self.draw_table()

    # 오른쪽 키 눌렀을 때
    def move_right(self):
        if self.is_editing:
            return
        if self.selected_col < self.cols - 1:
            self.selected_col += 1
            self.draw_table()

    # 마우스 눌렀을 때
    def on_click(self, event):
        # 체크박스 전체 선택
        if self.origin_cell_width <= event.x < self.origin_cell_width + self.checkbox_cell_width and 0 <= event.y < self.origin_cell_height:
            if all(i["checked"] for i in self.data.values()):
                for key in self.data:
                    self.data[key]["checked"] = False
            else:
                for key in self.data:
                    self.data[key]["checked"] = True
            self.draw_table()
            self.focus_set()
            return
        # 행/열 이름 부분
        if event.x <= self.origin_cell_width or event.y <= self.origin_cell_height: # 열 이름과 행 번호 부분을 클릭한 경우
            return
        # 영역 밖
        if event.x < 0 or event.x > self.origin_cell_width + sum(self.col_widths) or event.y < 0 or event.y > self.origin_cell_height + self.row_count * self.cell_height:
            self.focus = False
            return

        # 선택된 row/col 계산
        col = 0
        current_x = self.origin_cell_width
        for i, width in enumerate(self.col_widths):
            if event.x <= current_x + width:
                col = i
                break
            current_x += width
        row = (event.y - self.origin_cell_height) // self.cell_height

        if self.is_editing:
            self.save_cell()

        self.selected_row = self.start_row + row
        self.selected_col = col

        if col == 0:
            self.toggle_check(self.selected_row)
        self.draw_table()
        self.focus_set()
        self.focus = True

    # 마우스 스크롤했을 때
    def on_scroll(self, event):
        if event.delta > 0:
            self.start_row = max(self.start_row - 3, 0)
        else:
            self.start_row = min(self.start_row + 3, self.rows - min(self.rows, self.row_count))
        self.draw_table()

    # 엔트리 만들어서 셀 수정
    def edit_cell(self):
        if self.is_editing:
            return
        self.focus = False

        if self.selected_col > 0:
            self.entry = tk.Entry(self)
            self.entry.insert(0, self.get_data_from_cell(self.selected_row, self.selected_col))
            self.entry.config(font=('Arial', 10))
            self.entry.place(x=self.origin_cell_width + sum(self.col_widths[:self.selected_col]), y=self.origin_cell_height + (self.selected_row - self.start_row) * self.cell_height, width=self.col_widths[self.selected_col], height=self.cell_height) # 위치 및 크기 조정
            self.entry.focus()

            self.entry.bind("<Return>", lambda e: self.save_cell())
            self.entry.bind("<FocusOut>", lambda e: self.save_cell(False))

            self.is_editing = True
        else:
            self.toggle_check(self.selected_row)
            self.draw_table()

    # 수정된 셀 저장
    def save_cell(self, focus=True):
        self.set_data_from_cell(self.selected_row, self.selected_col, self.entry.get())

        self.entry.destroy()
        self.entry = None
        self.draw_table()

        self.is_editing = False
        edited_row = self.get_key(self.selected_row)
        if edited_row not in self.changed["added"] and edited_row not in self.changed["updated"]:
            self.changed["updated"][edited_row] = self.get_data_from_cell(self.selected_row)

        self.focus = focus
        if self.focus:
            self.focus_set()

        if self.selected_row == len(self.data) - 1:
            if any(i for i in self.data[self.last_index]["data"]): # 마지막 행 하나라도 채워지면
                self.add_row()
                if self.row_count < self.rows:
                    self.start_row += 1
            self.draw_table()

    # 체크된 행 삭제
    def delete_row(self):
        check = msgbox.askokcancel("행 삭제", "선택된 행을 삭제하시겠습니까?")
        if not check:
            return
        tmp = []
        for i, key in enumerate(self.data.keys()):
            if key == self.last_index: # 마지막 행 제외
                break
            if self.data[key]["checked"]:
                if key in self.changed["added"]:
                    del self.changed["added"][key]
                if key in self.changed["updated"]:
                    del self.changed["updated"][key]
                self.changed["deleted"][key] = self.get_data_from_key(key)
                tmp.append(key)
        for i, key in enumerate(tmp[::-1]):
            del self.data[key]
            if i < self.selected_row:
                self.selected_row -= 1
            if i < self.start_row:
                self.start_row -= 1

        self.rows = len(self.data)
        self.draw_table()

if __name__ == "__main__":
    # 사용 예시
    root = tk.Tk() # 부모 창
    root.config(bg="black")
    test_data = [[f"Data {r + 1}{chr(65 + c)}" for c in range(4)] for r in range(15)] # 임의의 데이터

    app1 = TableWidget(root, 
                       data=test_data,
                       col_name=["A", "B", "C", "D"], # 열 이름(순서대로, 데이터 열 개수와 맞게)
                       col_width=[120, 80, 100, 150], # 열 너비(순서대로, 데이터 열 개수와 맞게)
                       width=600, # 테이블 그려질 너비
                       height=400) # 테이블 그려질 높이
    # col_width 생략 시 크기에 맞게 분배
    # col_name 생략 시 Col1, Col2, ... 지정

    app1.grid(row=0, column=0)
    
    # 디버그용
    root.bind("<F5>", lambda e: test())

    def test():
        print(f"data: {app1.data}") # 저장된 데이터
        print(f"rows cols: {app1.rows} {app1.cols}") # 행 열 개수
        print(f"selected: {app1.selected_row} {app1.selected_col}") # 선택된 행 열 index
        print(f"changed {app1.changed}") # 원본 대비 변경된 데이터

    root.mainloop()
