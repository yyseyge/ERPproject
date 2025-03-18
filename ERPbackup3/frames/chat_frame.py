import tkinter as tk
import traceback
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from color import Color  # GRAY, WHITE, BLACK, BUTTON, FOCUS 등
import socket
import threading
import json
import datetime

# 전역 데이터
employees_data = []   # 직원 목록 (dict 리스트)
chatrooms_data = []   # 채팅방 목록 (dict 리스트)

current_user_info = {
    "employee_code": "",
    "name": "",
    "department": "",
    "job_grade": ""
}

test_socket = None
current_frame = None

class LoginFrame(tk.Frame):
    def __init__(self, root, on_login):
        super().__init__(root, bg=Color.WHITE)
        self.root = root
        self.on_login = on_login
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="ERP 로그인", font=('맑은 고딕', 18, 'bold'),
                         bg=Color.WHITE, fg=Color.BLACK)
        title.pack(pady=20)
        label = tk.Label(self, text="사원코드 입력", font=('맑은 고딕', 14),
                         bg=Color.WHITE, fg=Color.BLACK)
        label.pack(pady=10)
        self.entry_employee_code = tk.Entry(self, font=('맑은 고딕', 14), width=20)
        self.entry_employee_code.pack(pady=10)
        login_btn = tk.Button(self, text="로그인", font=('맑은 고딕', 14, 'bold'),
                              bg=Color.BUTTON, fg=Color.WHITE, command=self.login)
        login_btn.pack(pady=20)

    def login(self):
        emp_code = self.entry_employee_code.get().strip()
        if not emp_code:
            messagebox.showerror("오류", "사원코드를 입력하세요.")
            return
        req = {
            "code": 70001,
            "args": {
                "employee_code": emp_code,
                "password": "dummy"
            }
        }
        try:
            encoded = json.dumps(req, ensure_ascii=False).encode()
            test_socket.send(str(len(encoded)).ljust(16).encode())
            test_socket.send(encoded)
        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror("오류", str(e))

    def recv(self, **kwargs):
        code = kwargs.get("code")
        sign = kwargs.get("sign")
        data = kwargs.get("data")
        if code == 70001:
            if sign == 1 and data:
                current_user_info.update(data)
                self.on_login()
            else:
                messagebox.showerror("로그인 실패", str(data))
        else:
            print("로그인 창 기타 응답:", kwargs)

class ChattingFrame(tk.Frame):
    def __init__(self, root, sock):
        super().__init__(root, width=350, height=730, bg=Color.WHITE)
        self.root = root
        self.sock = sock
        self.current_chat_target = None
        self.current_room_id = None

        self.fr_top = tk.Frame(self, width=350, height=130, bg=Color.GRAY)
        self.fr_top.grid(row=0, column=0, sticky="nsew")
        self.fr_top.grid_propagate(False)
        self.create_top_frame()

        self.fr_middle = tk.Frame(self, width=350, height=560, bg=Color.WHITE, bd=1, relief=tk.SOLID)
        self.fr_middle.grid(row=1, column=0, sticky="nsew")
        self.fr_middle.grid_propagate(False)
        self.fr_main = tk.Frame(self.fr_middle, bg=Color.WHITE)
        self.fr_chatList = tk.Frame(self.fr_middle, bg=Color.WHITE)
        self.fr_group = tk.Frame(self.fr_middle, bg=Color.WHITE)
        self.fr_chat = tk.Frame(self.fr_middle, bg=Color.WHITE)
        for frame in (self.fr_main, self.fr_chatList, self.fr_group, self.fr_chat):
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.fr_bottom = tk.Frame(self, width=350, height=60, bg=Color.WHITE)
        self.fr_bottom.grid(row=2, column=0, sticky="nsew")
        self.fr_bottom.grid_propagate(False)
        self.create_bottom_buttons()

        self.show_main()

    def create_top_frame(self):
        self.fr_top_user = tk.Frame(self.fr_top, bg=Color.GRAY, height=60)
        self.fr_top_user.pack(fill=tk.X, side=tk.TOP)
        info_text = (
            f"사원코드: {current_user_info['employee_code']}    "
            f"이름: {current_user_info['name']}    "
            f"직급: {current_user_info['job_grade']}    "
            f"부서: {current_user_info['department']}"
        )
        lbl_user = tk.Label(self.fr_top_user, text=info_text, font=('맑은 고딕', 12, 'bold'),
                            fg=Color.BLACK, bg=Color.GRAY)
        lbl_user.pack(pady=10, padx=10)
        self.fr_top_search = tk.Frame(self.fr_top, bg=Color.GRAY, height=70)
        self.fr_top_search.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.search_entry = tk.Entry(self.fr_top_search, font=('맑은 고딕', 12), relief=tk.GROOVE, bd=2)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        self.search_btn = tk.Button(self.fr_top_search, text="🔍", font=('맑은 고딕', 12),
                                    bg=Color.BUTTON, fg=Color.WHITE, relief="flat",
                                    activebackground=Color.FOCUS, command=self.search_employees)
        self.search_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    def create_bottom_buttons(self):
        for widget in self.fr_bottom.winfo_children():
            widget.destroy()
        btn_main = tk.Button(self.fr_bottom, text="메인", font=('맑은 고딕', 12, 'bold'),
                             bg="#333333", fg=Color.WHITE, relief="flat", activebackground="#2a2a2a",
                             command=self.show_main)
        btn_chatList = tk.Button(self.fr_bottom, text="채팅방목록", font=('맑은 고딕', 12, 'bold'),
                                 bg="#444444", fg=Color.WHITE, relief="flat", activebackground="#3b3b3b",
                                 command=self.show_chatlist)
        btn_group = tk.Button(self.fr_bottom, text="채팅방 만들기", font=('맑은 고딕', 12, 'bold'),
                              bg="#555555", fg=Color.WHITE, relief="flat", activebackground="#4a4a4a",
                              command=self.show_group)
        btn_main.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        btn_chatList.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        btn_group.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        for i in range(3):
            self.fr_bottom.columnconfigure(i, weight=1)
        self.fr_bottom.rowconfigure(0, weight=1)

    def show_main(self):
        self.fr_main.lift()
        req = {"code": 10201, "args": {"사원이름": self.search_entry.get()}}
        self.send_(json.dumps(req, ensure_ascii=False))

    def show_chatlist(self):
        self.fr_chatList.lift()
        req = {"code": 70012, "args": {}}
        self.send_(json.dumps(req, ensure_ascii=False))

    def show_group(self):
        self.fr_group.lift()
        self.update_group()

    def show_chat(self, room_id, chat_target):
        self.current_room_id = int(room_id)
        self.current_chat_target = chat_target
        self.fr_chat.lift()
        self.update_chat()

    def update_main(self, employees=None):
        for widget in self.fr_main.winfo_children():
            widget.destroy()
        tree = ttk.Treeview(self.fr_main, columns=("사원코드", "이름", "부서", "직급"), show="headings")
        tree.heading("사원코드", text="사원코드")
        tree.heading("이름", text="이름")
        tree.heading("부서", text="부서")
        tree.heading("직급", text="직급")
        tree.column("사원코드", width=80, anchor="center")
        tree.column("이름", width=80, anchor="center")
        tree.column("부서", width=80, anchor="center")
        tree.column("직급", width=80, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)
        data = employees if employees is not None else employees_data
        for emp in data:
            tree.insert("", tk.END, values=(
                emp.get("사원코드"), emp.get("사원명"), emp.get("소속부서"), emp.get("직급")))
        tree.bind("<Double-1>", lambda e: self.open_one_to_one_chat(tree))

    def search_employees(self):
        self.show_main()

    def open_one_to_one_chat(self, tree):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            target_emp_code = values[0]
            personal_room_name = f"개인톡: {values[1]}"
            existing = [room for room in chatrooms_data if room.get("room_name") == personal_room_name]
            if existing:
                room_id = existing[0].get("room_id")
                self.show_chat(room_id, personal_room_name)
            else:
                req = {
                    "code": 70010,
                    "args": {
                        "room_name": personal_room_name,
                        "members": [target_emp_code, current_user_info["employee_code"]]
                    }
                }
                self.send_(json.dumps(req, ensure_ascii=False))

    def update_group(self):
        for widget in self.fr_group.winfo_children():
            widget.destroy()
        lbl = tk.Label(self.fr_group, text="단체 채팅방 만들기 - 초대할 사람 선택",
                       font=('맑은 고딕', 12, 'bold'), bg=Color.WHITE, fg=Color.BLACK)
        lbl.pack(pady=5)
        self.group_vars = {}
        for emp in employees_data:
            var = tk.IntVar()
            self.group_vars[emp["사원코드"]] = var
            chk = tk.Checkbutton(self.fr_group, text=f"{emp['사원명']} ({emp['소속부서']})",
                                 variable=var, bg=Color.WHITE, fg=Color.BLACK)
            chk.pack(anchor="w", padx=10)
        btn_create = tk.Button(self.fr_group, text="채팅방 만들기", font=('맑은 고딕', 12, 'bold'),
                               bg=Color.BUTTON, fg=Color.WHITE, relief="flat",
                               activebackground=Color.FOCUS, command=self.create_group_chat)
        btn_create.pack(pady=10)

    def create_group_chat(self):
        selected_members = [emp["사원코드"] for emp in employees_data if self.group_vars[emp["사원코드"]].get() == 1]
        if not selected_members:
            messagebox.showwarning("경고", "초대할 사람을 선택하세요.")
            return
        room_name = "단체방: " + ", ".join(selected_members)
        req = {
            "code": 70010,
            "args": {
                "room_name": room_name,
                "members": selected_members
            }
        }
        self.send_(json.dumps(req, ensure_ascii=False))

    def update_chatlist(self):
        for widget in self.fr_chatList.winfo_children():
            widget.destroy()
        tree = ttk.Treeview(self.fr_chatList, columns=("room_id", "채팅방", "마지막 메시지"), show="headings")
        tree.heading("채팅방", text="채팅방")
        tree.heading("마지막 메시지", text="마지막 메시지")
        tree.column("room_id", width=0, stretch=False)
        tree.column("채팅방", width=150, anchor="center")
        tree.column("마지막 메시지", width=200, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)
        data = chatrooms_data if chatrooms_data else []
        for room in data:
            tree.insert("", tk.END, values=(room.get("room_id"), room.get("room_name"), room.get("last_message")))
        tree.bind("<Double-1>", lambda e: self.open_group_chat(tree))

    def open_group_chat(self, tree):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0], "values")
            room_id = item[0]
            room_name = item[1]
            req_join = {
                "code": 70013,
                "args": {
                    "room_id": int(room_id),
                    "employee_code": current_user_info["employee_code"]
                }
            }
            self.send_(json.dumps(req_join, ensure_ascii=False))
            self.show_chat(room_id, room_name)

    def update_chat(self):
        for widget in self.fr_chat.winfo_children():
            widget.destroy()
        self.fr_chat.grid_rowconfigure(0, weight=0)
        self.fr_chat.grid_rowconfigure(1, weight=1)
        self.fr_chat.grid_rowconfigure(2, weight=0)
        self.fr_chat.grid_columnconfigure(0, weight=1)
        lbl = tk.Label(self.fr_chat, text=f"채팅: {self.current_chat_target}",
                       font=('맑은 고딕', 14, 'bold'), bg=Color.WHITE, fg=Color.BLACK)
        lbl.grid(row=0, column=0, sticky="nsew", pady=5)
        text_frame = tk.Frame(self.fr_chat, bg=Color.WHITE)
        text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        self.chat_history = tk.Text(text_frame, font=('맑은 고딕', 12),
                                     state="disabled", bg=Color.WHITE, fg=Color.BLACK, wrap="word")
        self.chat_history.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(text_frame, command=self.chat_history.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_history['yscrollcommand'] = scrollbar.set
        chat_input_frame = tk.Frame(self.fr_chat, bg=Color.WHITE, height=40)
        chat_input_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        chat_input_frame.grid_propagate(False)
        self.chat_input = tk.Entry(chat_input_frame, font=('맑은 고딕', 12), relief=tk.GROOVE, bd=2,
                                   bg=Color.WHITE, fg=Color.BLACK)
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.chat_input.bind("<Return>", self.sendMessage)
        send_btn = tk.Button(chat_input_frame, text="전송", font=('맑은 고딕', 12, 'bold'),
                             bg=Color.BUTTON, fg=Color.WHITE, relief="flat", activebackground=Color.FOCUS,
                             command=self.sendMessage)
        send_btn.pack(side=tk.RIGHT, padx=5)

    def sendMessage(self, event=None):
        message = self.chat_input.get().strip()
        if message:
            self.chat_input.delete(0, tk.END)
            self.append_message("나", message)
            req = {
                "code": 70011,
                "args": {
                    "room_id": self.current_room_id,
                    "sender_id": current_user_info["employee_code"],
                    "sender_name": current_user_info["name"],
                    "message": message
                }
            }
            self.send_(json.dumps(req, ensure_ascii=False))
        else:
            return

    def append_message(self, sender, message):
        self.chat_history.config(state="normal")
        self.chat_history.insert(tk.END, f"{sender}: {message}\n")
        self.chat_history.see("end")
        self.chat_history.config(state="disabled")

    def send_(self, msg):
        try:
            encoded = msg.encode()
            # test_socket.send(str(len(encoded)).ljust(16).encode())
            # test_socket.send(encoded)
            self.root.send_(msg)
        except Exception as e:
            print(traceback.format_exc())
            print(e)

    def recv(self, **kwargs):
        code = kwargs.get("code")
        sign = kwargs.get("sign")
        data = kwargs.get("data")
        if code == 70010:
            if sign == 1:
                messagebox.showinfo("채팅방 생성", str(data))
                req = {"code": 70012, "args": {}}
                self.send_(json.dumps(req, ensure_ascii=False))
            else:
                messagebox.showerror("채팅방 생성 실패", str(data))
        elif code == 70011:
            if sign == 1:
                if data.get("room_id") == self.current_room_id:
                    self.append_message(data.get("sender_name"), data.get("message"))
            else:
                messagebox.showerror("채팅 전송 실패", str(data))
        elif code == 70012:
            if sign == 1 and data:
                global chatrooms_data
                chatrooms_data = data
                self.update_chatlist()
            else:
                messagebox.showinfo("알림", "채팅방 목록 조회 실패")
        elif code == 10201:
            if sign == 1 and data:
                global employees_data
                employees_data = data
                self.update_main(employees=data)
            else:
                messagebox.showinfo("알림", "직원 목록 조회 실패")
        else:
            print("기타 응답:", kwargs)

def recv_thread_func(sock):
    def recv_all(count):
        buf = b""
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    while True:
        try:
            length_data = recv_all(16)
            if not length_data:
                break
            try:
                length = int(length_data.decode().strip())
            except Exception as e:
                print("길이 파싱 오류:", e)
                continue
            msg_data = recv_all(length)
            if not msg_data:
                continue
            decoded = msg_data.decode().strip()
            if decoded == "":
                continue
            try:
                msg_json = json.loads(decoded)
            except Exception as e:
                print(traceback.format_exc())
                continue
            if current_frame:
                current_frame.recv(**msg_json)
        except Exception as e:
            print("수신 스레드 오류:", e)
            break
#
# if __name__ == "__main__":
#     HOST = "192.168.0.12"   # 고정된 서버 IP
#     PORT = 12345            # 고정된 서버 포트
#     test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     test_socket.connect((HOST, PORT))
#
#     root = tk.Tk()
#     root.geometry("350x730")
#     root.config(bg=Color.WHITE)
#
#     def on_login():
#         global current_frame
#         global login_frame
#         login_frame.destroy()
#         current_frame = ChattingFrame(root, test_socket)
#         current_frame.pack(fill=tk.BOTH, expand=True)
#
#     login_frame = LoginFrame(root, on_login)
#     login_frame.pack(fill=tk.BOTH, expand=True)
#     current_frame = login_frame
#
#     threading.Thread(target=recv_thread_func, args=(test_socket,), daemon=True).start()
#
#     root.mainloop()