import tkinter as tk
import tkinter.messagebox as msgbox

from color import Color


# 최종 수정일 250307 15:28
class TableWidget(tk.Frame):
    def __init__(self, master, padding=0, data=None, cols=0, new_row=True, has_checkbox=True, col_name=None,
                 col_width=None, col_align=None, editable=None, padx=None, pady=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.padding = padding
        self.has_checkbox = True  # 체크박스 표시 여부
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.font = ("Arial", 10)

        self.col_name = None  # 열 이름
        self.col_widths = None  # 셀 너비
        self.col_align = None  # 열 정렬
        self.editable = None  # 수정 가능 여부
        self.data = None  # 데이터
        self.new_row = True  # 맨 아래 빈 행 추가 여부

        self.last_index = 0  # 데이터 마지막 행 번호
        self.rows = 0  # 행 개수
        self.cols = 0  # 열 개수
        self.selected_row = 0  # 선택된 행
        self.selected_col = 0  # 선택된 열

        self.origin_cell_width = 40  # 기준 셀 너비
        self.origin_cell_height = 30  # 기준 셀 높이
        self.checkbox_cell_width = 30 if has_checkbox else 0  # 체크박스 셀 너비
        self.scrollbar_width = 16  # 스크롤바 크기
        self.cell_height = 30  # 셀 높이

        self.width = kwargs.get("width", self.origin_cell_width + self.checkbox_cell_width)  # 프레임 너비
        self.height = kwargs.get("height", self.origin_cell_height + self.cell_height)  # 프레임 높이

        self.start_row = 0  # canvas에 보여질 첫 행 번호
        self.row_count = (
                                     self.height - self.origin_cell_height - self.scrollbar_width) // self.cell_height  # canvas에 보여질 행 개수

        self.entry = None  # 수정할 때 나타날 entry
        self.is_editing = False  # Entry 위젯이 활성화 여부
        self.focus = True  # 현재 포커스 여부
        self.changed = {  # 원본 데이터 대비 바뀐 행들
            "updated": {},
            "added": {},
            "deleted": {}
        }

        self.scroll_h = tk.Scrollbar(self, orient=tk.HORIZONTAL, width=self.scrollbar_width)
        self.canvas = tk.Canvas(self, width=self.width - 2 * padding,
                                height=self.height - self.scrollbar_width - 2 * padding, highlightthickness=0)  # canvas
        self.scroll_h.place(x=padding, y=self.height - padding - self.scrollbar_width, width=self.width - 2 * padding)

        self.scroll_h.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.scroll_h.set)
        self.canvas.place(x=padding, y=padding)

        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<Up>", lambda e: self.move_up())
        self.bind("<Down>", lambda e: self.move_down())
        self.bind("<Left>", lambda e: self.move_left())
        self.bind("<Right>", lambda e: self.move_right())
        self.bind("<Return>", lambda e: self.edit_cell())
        self.canvas.bind("<MouseWheel>", lambda e: self.on_scroll(e))
        self.bind("<F7>", lambda e: self.delete_row())

        self.from_data(data=data, cols=cols, new_row=new_row, has_checkbox=has_checkbox, col_name=col_name,
                       col_width=col_width, col_align=col_align, editable=editable, **kwargs)

    # 특정 list로 테이블 만들기
    def from_data(self, data: list[list], cols: int = 0, new_row: bool = True, has_checkbox: bool = True,
                  col_name: list[str] = None, col_width: list[int] = None, col_align: list[str] = None,
                  editable: list[bool] = None, **kwargs):
        # 초기화
        self.new_row = new_row
        self.has_checkbox = has_checkbox
        self.col_name = None
        self.col_widths = None
        self.col_align = None
        self.editable = None

        self.selected_row = 0
        self.selected_col = 0
        self.checkbox_cell_width = 30 if has_checkbox else 0

        if data is None:
            self.data = {}
            self.rows = 0
            self.last_index = None
        else:
            self.data = {
                i: {
                    "checked": False,
                    "data": [j for j in d]
                } for i, d in enumerate(data)  # 원본 데이터 유지
            }
            self.rows = len(data)
            self.last_index = len(data) - 1

        if cols == 0:
            self.cols = len(data[0])
        else:
            self.cols = cols

        if col_name is None:
            self.col_name = ColName()
            for i in range(self.cols):
                self.col_name.add(f"Col{i + 1}", 0, i)
        elif type(col_name) == list:
            self.col_name = ColName()
            for i, value in enumerate(col_name):
                self.col_name.add(value, 0, i)
        else:
            self.col_name = col_name
        if col_width is None:
            self.col_widths = [
                (self.width - self.origin_cell_width - self.checkbox_cell_width - 2 * self.padding - 1) / self.cols for
                _ in range(self.cols)]
        else:
            self.col_widths = col_width + ([(
                                                        self.width - self.origin_cell_width - self.checkbox_cell_width - 2 * self.padding - 1 - sum(
                                                    col_width)) / (self.cols - len(col_width)) for _ in
                                            range(self.cols - len(col_width))] if len(col_width) < self.cols else [])
        if col_align is None:
            self.col_align = ["left" for _ in range(self.cols)]
        else:
            self.col_align = col_align + (
                ["left" for _ in range(self.cols - len(col_align))] if len(col_align) < self.cols else [])
        if editable is None:
            self.editable = [True for _ in range(self.cols)]
        else:
            self.editable = editable + (
                [True for _ in range(self.cols - len(editable))] if len(editable) < self.cols else [])

        self.row_count = (
                                     self.height - self.origin_cell_height * self.col_name.rows - self.scrollbar_width) // self.cell_height  # canvas에 보여질 행 개수

        self.changed = {
            "updated": {},
            "added": {},
            "deleted": {}
        }
        self.canvas.config(scrollregion=(0, 0, self.origin_cell_width + self.checkbox_cell_width + sum(self.col_widths),
                                         self.origin_cell_height + self.rows * self.cell_height))

        if new_row:
            self.add_row()
        else:
            self.draw_table()

    # 선택된 셀의 값 가져오기
    def get(self):
        if self.rows == 0:
            return None
        if self.selected_col < 0:
            return self.is_checked(self.selected_row)
        return self.get_data_from_cell(self.selected_row, self.selected_col)

    # 선택된 셀이 있는 행 전체 정보
    def get_row(self):
        if self.rows == 0:
            return None
        return self.data[self.get_key(self.selected_row)]

    # 체크된 데이터 개수
    def checked_count(self):
        return sum(1 for i in self.data.values() if i["checked"])

    # 체크박스 정보를 제외한 data
    def get_data(self):
        return [i["data"] for i in self.data.values()]

    # 체크된 데이터만
    def checked_data(self):
        return [i["data"] for i in self.data.values() if i["checked"]]

    # index로부터 key 찾기 
    def get_key(self, index):
        return list(self.data.keys())[index]

    # 셀의 row col index로 데이터 값 찾기
    def get_data_from_cell(self, row, col=None):
        if col is None:
            return self.data[self.get_key(row)]["data"]
        return self.data[self.get_key(row)]["data"][col]

    # 셀의 row col index로 데이터 값 설정
    def set_data_from_cell(self, row, col, value):
        self.data[self.get_key(row)]["data"][col] = value

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
        if self.last_index is None:
            self.last_index = 0
        else:
            self.last_index += 1
        self.data[self.last_index] = {
            "checked": False,
            "data": ["" for _ in range(self.cols)]
        }
        self.changed["added"][self.last_index] = self.data[self.last_index]["data"]
        self.rows += 1
        self.draw_table()

    # 테이블 그리기
    def draw_table(self):
        self.canvas.delete("all")  # 이전 그려진 내용을 지움

        # 좌상단 셀
        self.canvas.create_rectangle(0, 0, self.origin_cell_width, self.origin_cell_height * self.col_name.rows,
                                     outline=Color.BLACK, fill=Color.FOCUS, tags="header")

        # 체크박스 열
        if self.has_checkbox:
            self.canvas.create_rectangle(self.origin_cell_width, 0, self.origin_cell_width + self.checkbox_cell_width,
                                         self.origin_cell_height * self.col_name.rows, outline=Color.BLACK,
                                         fill=Color.FOCUS, tags="header")

        # 열 이름
        current_x = self.origin_cell_width + self.checkbox_cell_width
        for title in self.col_name.names:
            x1 = current_x + sum(self.col_widths[:title["col"]])
            x2 = x1 + sum(self.col_widths[title["col"]:title["col"] + title["colspan"]])
            y1 = self.origin_cell_height * title["row"]
            y2 = y1 + self.origin_cell_height * title["rowspan"]
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=Color.BLACK, fill=Color.FOCUS, tags="header")
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=title["value"], font=self.font, tags="header")

        # canvas에 보이는 각 행
        for row in range(self.row_count):
            current_row = self.start_row + row
            if current_row >= len(self.data):
                break

            # 행 번호
            y1 = self.origin_cell_height * self.col_name.rows + row * self.cell_height
            y2 = y1 + self.cell_height

            self.canvas.create_rectangle(0, y1, self.origin_cell_width, y2, outline=Color.BLACK, fill=Color.FOCUS,
                                         tags="header")
            self.canvas.create_text(0 + self.origin_cell_width / 2, y1 + self.origin_cell_height / 2,
                                    text=str(self.start_row + row + 1), font=self.font, tags="header")

            # 체크박스 셀
            if self.has_checkbox and current_row < self.rows:
                self.canvas.create_rectangle(self.origin_cell_width, y1,
                                             self.origin_cell_width + self.checkbox_cell_width, y2, outline=Color.BLACK,
                                             fill=Color.GRAY if current_row == self.selected_row else Color.WHITE,
                                             tags="cell")
                self.draw_checkbox(self.origin_cell_width + 10, y1 + 10, self.is_checked(current_row))

            # 데이터 셀
            current_x = self.origin_cell_width + self.checkbox_cell_width
            for col in range(self.cols):
                x1 = current_x
                x2 = x1 + self.col_widths[col]

                self.canvas.create_rectangle(x1, y1, x2, y2, outline=Color.BLACK,
                                             fill=Color.GRAY if current_row == self.selected_row else Color.WHITE,
                                             tags="cell")
                if self.col_align[col] == "center":
                    self.canvas.create_text(x1 + self.col_widths[col] / 2, y1 + self.cell_height / 2,
                                            text=self.get_data_from_cell(current_row, col), font=self.font, tags="text",
                                            anchor="center")
                elif self.col_align[col] == "right":
                    self.canvas.create_text(x1 + self.col_widths[col] - 5, y1 + self.cell_height / 2,
                                            text=self.get_data_from_cell(current_row, col), font=self.font, tags="text",
                                            anchor="e")
                else:  # left
                    self.canvas.create_text(x1 + 5, y1 + self.cell_height / 2,
                                            text=self.get_data_from_cell(current_row, col), font=self.font, tags="text",
                                            anchor="w")
                current_x = x2

        # 선택된 셀 강조
        if self.rows > 0 and self.start_row <= self.selected_row < self.start_row + self.row_count:
            if self.selected_col >= 0:
                x1 = self.origin_cell_width + self.checkbox_cell_width + sum(self.col_widths[:self.selected_col])
                x2 = x1 + self.col_widths[self.selected_col]
            else:
                x1 = self.origin_cell_width
                x2 = x1 + self.checkbox_cell_width
            y1 = (self.selected_row - self.start_row) * self.cell_height + self.origin_cell_height * self.col_name.rows
            y2 = y1 + self.cell_height
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=Color.BUTTON, width=2, tags="highlight")

    # 체크박스 그리기
    def draw_checkbox(self, x, y, checked=False):
        self.canvas.create_rectangle(x, y, x + 10, y + 10, outline=Color.BLACK,
                                     fill=Color.BLACK if checked else Color.WHITE, width=2)

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
        if self.selected_col > (-1 if self.has_checkbox else 0):
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
        if self.origin_cell_width <= event.x < self.origin_cell_width + self.checkbox_cell_width and 0 <= event.y < self.origin_cell_height * self.col_name.rows:
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
        if event.x <= self.origin_cell_width or event.y <= self.origin_cell_height * self.col_name.rows:  # 열 이름과 행 번호 부분을 클릭한 경우
            self.focus_set()
            return
        # 영역 밖
        if event.x < 0 or event.x > self.origin_cell_width + sum(
                self.col_widths) or event.y < 0 or event.y > self.origin_cell_height * self.col_name.rows + min(
                self.rows, self.row_count) * self.cell_height:
            self.focus = False
            return

        if self.is_editing:
            self.save_cell()

        self.selected_row = self.start_row + (
                    event.y - self.origin_cell_height * self.col_name.rows - 1) // self.cell_height

        if self.origin_cell_width <= event.x < self.origin_cell_width + self.checkbox_cell_width:  # checkbox
            self.toggle_check(self.selected_row)
            self.selected_col = -1
        else:  # data
            self.selected_col = 0
            current_x = self.origin_cell_width + self.checkbox_cell_width
            for i, width in enumerate(self.col_widths):
                if event.x <= current_x + width:
                    self.selected_col = i
                    break
                current_x += width

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

        if not self.editable[self.selected_col]:
            return

        if self.has_checkbox and self.selected_col < 0:
            self.toggle_check(self.selected_row)
            self.draw_table()
        else:
            self.entry = tk.Entry(self)
            self.entry.insert(0, self.get_data_from_cell(self.selected_row, self.selected_col))
            self.entry.config(font=self.font)
            self.entry.place(x=self.padding + self.origin_cell_width + self.checkbox_cell_width + sum(
                self.col_widths[:self.selected_col]), y=self.padding + self.origin_cell_height * self.col_name.rows + (
                        self.selected_row - self.start_row) * self.cell_height,
                             width=self.col_widths[self.selected_col], height=self.cell_height)  # 위치 및 크기 조정
            self.entry.focus()

            self.entry.bind("<Return>", lambda e: self.save_cell())
            self.entry.bind("<FocusOut>", lambda e: self.save_cell(False))

            self.is_editing = True

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
            if any(i for i in self.data[self.last_index]["data"]):  # 마지막 행 하나라도 채워지면
                if self.new_row:
                    self.add_row()
                    if self.row_count < self.rows:
                        self.start_row += 1
            else:
                self.draw_table()

    # 체크된 행 삭제
    def delete_row(self):
        if not self.has_checkbox:
            return
        check = msgbox.askokcancel("행 삭제", "선택된 행을 삭제하시겠습니까?")
        if not check:
            return
        tmp = []
        for i, key in enumerate(self.data.keys()):
            if self.new_row and key == self.last_index:  # 마지막 행 제외
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


class ColName:
    def __init__(self, from_list: list = None):
        self.names = []
        self.rows = 0
        self.cols = 0
        if from_list is None:
            return

        for i, value in enumerate(from_list):
            self.add(value, 0, i)

    def add(self, value, row, col, rowspan=1, colspan=1):
        self.names.append({
            "value": value,
            "row": row,
            "col": col,
            "rowspan": rowspan,
            "colspan": colspan
        })
        self.rows = max(self.rows, row + rowspan)
        self.cols = max(self.cols, col + colspan)


if __name__ == "__main__":
    # 사용 예시
    root = tk.Tk()  # 부모 창
    root.geometry("600x400")

    test_data = [[f"Data {r + 1}{chr(65 + c)}" for c in range(5)] for r in range(15)]  # 임의의 데이터
    test_frame = tk.Frame(root, width=600, height=400)

    cn = ColName()
    cn.add("과목", 0, 0, rowspan=2)
    cn.add("당기", 0, 1, colspan=2)
    cn.add("전기", 0, 3, colspan=2)
    cn.add("금액", 1, 1, colspan=2)
    cn.add("금액", 1, 3, colspan=2)
    # print(t.rows, t.cols)

    table_widget = TableWidget(test_frame,
                               data=test_data,
                               # data=None,
                               cols=5,
                               # new_row=False,
                               # has_checkbox=False, # 체크박스 존재 여부
                               # col_name=["A", "B", "C", "D"], # 열 이름(순서대로)
                               col_name=cn,  # 열 이름(순서대로, 데이터 열 개수와 맞게)
                               # col_width=[120, 80, 100, 150], # 열 너비(순서대로)
                               col_align=["left", "center", "right"],
                               editable=[True, True, False],
                               width=600,  # 테이블 그려질 너비
                               height=400,
                               padding=10
                               )
    test_frame.place(x=0, y=0)
    table_widget.grid(row=0, column=0)

    # 디버그용
    root.bind("<F5>", lambda e: test())
    root.bind("<F4>", lambda e: table_widget.add_row())
    root.bind("<F3>", lambda e: print(table_widget.get_row()))
    root.bind("<F2>", lambda e: print(table_widget.get()))
    root.bind("<F1>", lambda e: print(table_widget.get_data()))


    def test():
        print(f"data: {table_widget.data}")  # 저장된 데이터
        print(f"rows cols: {table_widget.rows} {table_widget.cols}")  # 행 열 개수
        print(f"selected: {table_widget.selected_row} {table_widget.selected_col}")  # 선택된 행 열 index
        print(f"changed {table_widget.changed}")  # 원본 대비 변경된 데이터


    def test2():
        table_widget.from_data(
            data=[
                ["1", "2", "3"],
                ["4", "5", "6"],
                ["7", "8", "9"],
            ],
            cols=3,
            new_row=False,
            has_checkbox=False,
            col_name=["A", "B", "C"],
            col_width=None,
            col_align=["left", "center", "right"],
            editable=[False, True, True],
            width=1300,
            height=350,
        )


    root.mainloop()