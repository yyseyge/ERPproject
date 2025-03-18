
import json
import socket
import threading
import tkinter as tk
import traceback

from color import Color
from frames import *
from frames import notification


# icon
# https://www.flaticon.com/icon-fonts-most-downloaded?weight=bold&type=uicon

class Tab:
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third
        self.button = None

    def __hash__(self):
        return hash((self.first, self.second, self.third))

    def __eq__(self, other):
        if isinstance(other, Tab):
            return (self.first, self.second, self.third) == (other.first, other.second, other.third)
        return False


class Category:
    def __init__(self, btn: tk.Button = None):
        self.button = btn
        self.categories = {}

    def add(self, id_, category):
        self.categories[id_] = category

    def get(self, id_):
        return self.categories[id_]


class AppFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root

    def send_(self, msg):
        self.root.send_(msg)

    def prev_page(self):
        self.root.prev_page()

    def next_page(self):
        self.root.next_page()


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.socket = None

        self.category = {
            "인사": {
                "직원관리": {
                    "테스트": [sample.SampleFrame, sample2.SampleFrame2],
                    "사원관리": [employee_management.EmployeeManagement],
                },
                "출퇴기록": {
                    "근태현황": [attendance_status.AttendanceStatus],
                },
                "연차휴가관리": {
                    "초과근무관리": [overtime_management.OvertimeManagement],
                    "연차관리": [Time_off_management.Timeoffmanagement],
                },
                "급여관리": {
                    "급여관리명세서": [pay_stub.PayStub],
                    "퇴직금명세서": [serverance_pay.SeverancePay],
                },
                "회사정보": {
                    "회사정보": [company_information.CompanyInformation],
                },
            },
            "기술": {
                "생산관리": {
                    "작업표준서": [SOP.SOP],
                    "BOM": [BOM.BOM],
                    "생산지시서": [MO.Manufacturing_Order],
                    "출고": [shipping.Shipping],
                    "입고": [receiving.Receiving],
                },
                "자재관리": {
                    "자재조회/수정/삭제": [materialFrame.materialFrame],
                    "구매요청서 조회/등록/수정/삭제": [PO.PurchasingOrder]
                },
                "물류관리": {
                    "창고등록마스터": [Plant.Plant],
                    "창고별자재조회": [plantFrame.plantFrame],
                }
            },
            "영업": {
                "거래처등록": {
                    "등록": [add_business_partner.add_business_partner_Frame],
                },
                "발주서": {
                    "생성/조회/수정/삭제": [order_form.order],
                },
                "판매 실적": {
                    "판매 실적 조회": [Sales_Performance.Sales_Performance],
                }
            },
            "회계": {
                "재무회계": {
                    "전표": [ac_accountbook.AccountBookFrame],
                    "세금계산서": [ac_taxinvoice.TaxInvoiceFrame],
                    "계정관리": [ac_accountsubject.AccountSubjectFrame],
                    "재무상태표": [Financial_statement.Financial_statement],
                    "손익계산서": [income_statement.income_statement],
                },
                "관리회계": {
                    "생산비용 분석": [Production_cost_analysis_1.Production_cost_analysis_1,
                                Production_cost_analysis_2.Production_cost_analysis_2]
                },
            },
        }

        self.logged_in = False
        self.id_ = None
        self.name = None

        self.current_category = [None, None, None]
        self.opened_category = []
        self.tabs = []
        self.etc_buttons = []

        # 상단 좌측
        self.fr_logo = tk.Frame(self, width=300, height=130, bg=Color.GRAY)
        self.fr_logo.grid(row=0, column=0)

        self.im_logo = tk.PhotoImage(file="logo.png")
        self.lb_logo = tk.Label(self.fr_logo, image=self.im_logo, width=300, height=130, borderwidth=0,
                                highlightthickness=0, bg=Color.WHITE)
        self.lb_logo.bind("<Button-1>", lambda e: self.screen_main())
        self.lb_logo.place(x=0, y=0)

        # 상단 우측
        self.fr_nav = tk.Frame(self, width=1300, height=130, bg=Color.WHITE)
        self.fr_nav.grid(row=0, column=1)

        self.fr_notification = tk.Frame(self.fr_nav, width=1300, height=100, bg=Color.WHITE)
        self.fr_tabs = tk.Frame(self.fr_nav, width=1300, height=30, bg=Color.WHITE)

        self.en_id = tk.Entry(self.fr_notification)

        self.im_login = tk.PhotoImage(file="sign-in-alt.png")
        self.bt_login = tk.Button(self.fr_notification, image=self.im_login, relief="flat", bg=Color.WHITE,
                                  command=self.login)

        self.im_logout = tk.PhotoImage(file="sign-out-alt.png")
        self.bt_logout = tk.Button(self.fr_notification, image=self.im_logout, relief="flat", bg=Color.WHITE,
                                   command=self.logout)

        self.im_alarm = tk.PhotoImage(file="bell.png")
        # self.bt_alarm = tk.Button(self.fr_notification, padx=10, pady=10, text=0, command=self.draw_nt)
        self.bt_alarm = tk.Button(self.fr_notification, image=self.im_alarm, relief="flat", bg=Color.WHITE,
                                  command=self.draw_nt)

        self.im_chat = tk.PhotoImage(file="comment-alt-middle.png")
        self.bt_chat = tk.Button(self.fr_notification, image=self.im_chat, relief="flat", bg=Color.WHITE,
                                 command=self.toggle_chat)

        self.en_id.place(x=900, y=45)
        self.bt_login.place(x=1050, y=35)
        self.bt_alarm.place(x=1150, y=35)
        self.bt_chat.place(x=1200, y=35)

        self.fr_notification.grid(row=0, column=0)
        self.fr_tabs.grid(row=1, column=0)
        self.fr_tabs.pack_propagate(False)

        # 중앙 좌측
        self.fr_menu = tk.Frame(self, width=300, height=700, bg=Color.WHITE)
        self.fr_menu.grid(row=1, column=0)

        # 중앙 우측
        self.fr_app = AppFrame(self, width=1300, height=700)
        self.fr_app.grid(row=1, column=1)

        self.apps = {}
        self.app = None

        # 하단 좌측
        self.fr_etc = tk.Frame(self, width=300, height=70, bg=Color.WHITE)
        self.fr_etc.grid(row=2, column=0, sticky="n")
        self.fr_etc.pack_propagate(False)

        self.fr_etc_inner = tk.Frame(self.fr_etc, bg=Color.WHITE)
        self.fr_etc_inner.pack(expand=True)

        self.etc_buttons.append(
            tk.Button(self.fr_etc_inner, text="e001>e002 메시지", bg=Color.FOCUS, relief="flat", padx=30, pady=5,
                      command=self.start_work))
        # self.etc_buttons.append(tk.Button(self.fr_etc_inner, text="퇴근", bg=Color.FOCUS, relief="flat", padx=30, pady=5, command=self.add_nt))
        self.etc_buttons.append(
            tk.Button(self.fr_etc_inner, text="e001>e006 결재", bg=Color.FOCUS, relief="flat", padx=30, pady=5,
                      command=self.appr))

        # 하단 우측
        self.fr_footer = tk.Frame(self, width=1300, height=70, bg=Color.WHITE)
        self.fr_footer.grid(row=2, column=1)

        self.current_page = 0
        self.pages = 1
        self.footer_buttons = []

        self.geometry("1600x900")
        self.resizable(width=False, height=False)
        self.title("ERP")
        self.configure(background=Color.WHITE)

        self.category_tree = Category()
        for first in self.category:
            first_tree = Category(tk.Button(self.fr_menu, text=first, anchor="w", bg=Color.FOCUS, relief="flat",
                                            command=lambda x=first: self.select_category(0, x)))
            # first_tree = Category(tk.Button(self.fr_menu, text=first, anchor="w", bg=Color.BUTTON, relief="flat", borderwidth=0, command=lambda x=first: self.select_category(0, x)))
            self.category_tree.add(first, first_tree)

            for second in self.category[first]:
                second_tree = Category(
                    tk.Button(self.fr_menu, text=f"　　{second}", anchor="w", bg=Color.GRAY, relief="flat",
                              command=lambda x=second: self.select_category(1, x)))
                first_tree.add(second, second_tree)

                for third in self.category[first][second]:
                    third_tree = Category(
                        tk.Button(self.fr_menu, text=f"　　　　{third}", anchor="w", bg=Color.WHITE, relief="flat",
                                  command=lambda x=third: self.select_category(2, x)))
                    second_tree.add(third, third_tree)

        # 알림
        self.nt_frame = notification.NotificationFrame(self, self.test)
        self.bt_alarm.config(text=self.nt_frame.get_nt_len())
        self.nt_flag = True

        # 채팅
        self.chat_frame = chat_frame.ChattingFrame(self, self.socket)
        self.chat_frame.place(x=1250, y=-850)
        self.chat_visible = False

        # 결재
        self.fr_appr = None

        # self.nt_button = tk.Button(self.fr_notification, text=self.nt_frame.get_nt_len(), command=self.draw_nt)
        # self.nt_button.pack()
        # self.nt_button2 = tk.Button(self.fr_notification, command=self.add_nt)
        # self.nt_button2.pack()

        self.draw_etc()

        self.en_id.insert(0, "e001")

    def draw_nt(self):
        if self.nt_flag:
            self.bt_alarm.config(text=self.nt_frame.get_nt_len())
            self.nt_frame.place(x=900, y=80)
            self.nt_frame.deployment()
            self.nt_flag = False
        else:
            self.bt_alarm.config(text=self.nt_frame.get_nt_len())
            self.nt_frame.place_forget()
            self.nt_flag = True

    def add_nt(self):
        test = {"code": 00000, "sign": 1, "data": {"message": "안녕하세요", "sender_id": "id2", "sender_name": "성진하이"}}
        self.nt_frame.recv(test)
        self.bt_alarm.config(text=self.nt_frame.get_nt_len())

    def test(self):
        self.bt_alarm.config(text=self.nt_frame.get_nt_len())

    # 메인화면(첫화면) 띄우기
    def screen_main(self):
        print("main")
        self.current_category = [None, None, None]

        self.draw_category()
        self.draw_tabs()
        if self.opened_category is None:
            return
        if self.app is not None:
            self.app.destroy()
        self.app = dashboard.DashboardFrame(self.fr_app)
        self.app.place(x=0, y=0)

        if callable(getattr(self.app, "after_init", None)):
            self.app.after_init()
        self.opened_category = None

        for b in self.footer_buttons:
            b.destroy()
        self.footer_buttons.clear()

    # 카테고리 선택
    def select_category(self, depth, key):
        # 이미 선택된 카테고리
        if self.current_category[depth] == key:
            if depth < 2:
                self.current_category[depth] = None
            else:
                return
        else:
            self.current_category[depth] = key
        for i in range(depth + 1, 3):
            self.current_category[i] = None

        if depth == 2:
            print(key)
            # 로그아웃 상태
            if not self.logged_in:
                return
            category = self.category[self.current_category[0]][self.current_category[1]][self.current_category[2]]
            # button = self.category_tree.get(self.current_category[0]).get(self.current_category[1]).get(self.current_category[2]).button
            # print(button)
            self.opened_category = category
            self.pages = len(category)

            for key in self.apps:
                if self.apps[key] is not None:
                    self.apps[key].destroy()
                    self.apps[key] = None
            self.app = None

            self.apps = {
                i: None for i in range(self.pages)
            }

            frame = category[0]
            self.current_page = 0

            # 프레임 아직 안만들었을 경우
            if frame is None:
                return

            self.apps[self.current_page] = frame(self.fr_app)
            self.app = self.apps[self.current_page]
            self.append_tab(*self.current_category)

            if self.app is None:
                print("App is None")
                return

            if callable(getattr(self.app, "after_init", None)):
                self.app.after_init()
            else:
                # print("Frame doesnt have after_init()")
                pass
            self.app.place(x=0, y=0)
            self.draw_pages()
            self.draw_tabs()
        self.draw_category()

    # 카테고리 그리기(좌측)
    def draw_category(self):
        y = 0
        for first in self.category:
            first_tree = self.category_tree.get(first)
            first_tree.button.place(y=y, width=300, height=30)
            y += 30

            for second in self.category[first]:
                second_tree = first_tree.get(second)
                if self.current_category[0] == first:
                    second_tree.button.place(y=y, width=300, height=30)
                    y += 30
                else:
                    second_tree.button.place_forget()

                for third in self.category[first][second]:
                    third_tree = second_tree.get(third)
                    if self.current_category[1] == second:
                        third_tree.button.place(y=y, width=300, height=30)
                        y += 30
                    else:
                        third_tree.button.place_forget()

    # 페이지 버튼 그리기
    def draw_pages(self):
        for b in self.footer_buttons:
            b.destroy()
        self.footer_buttons.clear()
        self.footer_buttons.append(tk.Button(self.fr_footer, text="<", bg=Color.WHITE, padx=10, pady=10, relief="flat",
                                             command=self.prev_page))
        for i in range(self.pages):
            self.footer_buttons.append(
                tk.Button(self.fr_footer, text=str(i + 1), bg=Color.WHITE, padx=10, pady=10, relief="flat",
                          command=lambda x=i: self.select_page(x)))
            if self.current_page == i:
                self.footer_buttons[-1].config(bg=Color.GRAY)
            else:
                self.footer_buttons[-1].config(bg=Color.WHITE)
        self.footer_buttons.append(tk.Button(self.fr_footer, text=">", bg=Color.WHITE, padx=10, pady=10, relief="flat",
                                             command=self.next_page))

        for b in self.footer_buttons:
            b.pack(side="left")

    # 이전 페이지
    def prev_page(self):
        if self.current_page <= 0:
            return

        self.select_page(self.current_page - 1)

    # 다음 페이지
    def next_page(self):
        if self.current_page >= self.pages - 1:
            return

        self.select_page(self.current_page + 1)

    # 페이지 선택
    def select_page(self, page):
        print(page + 1, "page")
        first_load = False
        if (self.current_page == page) or (page not in self.apps):
            return

        self.current_page = page
        if self.apps[page] is None:
            self.apps[page] = self.opened_category[page](self.fr_app)
            first_load = True

        self.app.place_forget()
        self.app = self.apps[page]

        if first_load and callable(getattr(self.app, "after_init", None)):
            self.app.after_init()

        self.app.place(x=0, y=0)
        self.draw_pages()

    # 탭 버튼 선택
    def select_tab(self, tab):
        self.current_category[0] = tab.first
        self.current_category[1] = tab.second
        self.select_category(2, tab.third)

    # 탭 추가
    def append_tab(self, first, second, third):
        # print(first, second, third)
        tab = Tab(first, second, third)
        if tab in self.tabs:
            idx = self.tabs.index(tab)
            self.tabs.append(self.tabs.pop(idx))
            return

        tab.button = tk.Button(self.fr_tabs, text=tab.third, height=30, padx=10, relief="flat",
                               command=lambda: self.select_tab(tab))
        self.tabs.append(tab)

        if len(self.tabs) > 10:
            self.tabs.pop(0).button.destroy()

    # 탭 그리기
    def draw_tabs(self):
        for tab in self.tabs:
            tab.button.pack_forget()

        for tab in self.tabs[:-1]:
            tab.button.config(bg=Color.WHITE)
        if self.tabs:
            if self.opened_category is None:
                self.tabs[-1].button.config(bg=Color.WHITE)
            else:
                self.tabs[-1].button.config(bg=Color.GRAY)

        for tab in self.tabs[::-1]:
            tab.button.pack(side="left", anchor="w")

    def draw_etc(self):
        for button in self.etc_buttons:
            button.pack_forget()
        if self.logged_in:
            for button in self.etc_buttons:
                button.pack(side="left", padx=5)

    def login(self):
        msg = {
            "code": 81001,
            "args": {
                "id": self.en_id.get()
            }
        }
        self.send_(json.dumps(msg, ensure_ascii=False))

    def logout(self):
        msg = {
            "code": 81002,
            "args": {
                "id": self.en_id.get()
            }
        }
        self.send_(json.dumps(msg, ensure_ascii=False))

    def start_work(self):
        if not self.logged_in:
            return
        msg = {
            "code": 71003,
            "args": {
                "from_id": self.en_id.get(),
                "type": "user",
                "to_id": "e002",
                "msg": "hello"
            }
        }
        self.send_(json.dumps(msg, ensure_ascii=False))
        print("start_work")

    def finish_work(self):
        if not self.logged_in:
            return
        print("finish_work")

    def appr(self):
        self.fr_appr = test_apprreq.ApprovalReqFrame(self)
        self.fr_appr.reqAppr()
        self.fr_appr.user_name_entry.delete(0, tk.END)
        self.fr_appr.user_name_entry.insert(0, self.name)
        self.fr_appr.user_name_entry.config(state="disabled")

    def get_user_id(self):
        return self.id_

    def get_user_name(self):
        return self.name

    def toggle_chat(self):
        if self.chat_visible:
            self.hide_chat()
        else:
            self.show_chat()

    def show_chat(self):
        self.chat_visible = True
        self.animate_chat(visible=True)

    def hide_chat(self):
        self.chat_visible = False
        self.animate_chat(visible=False)

    def animate_chat(self, visible):
        target_y = 50 if visible else -850
        current_y = self.chat_frame.winfo_y()
        step = 20 if visible else -20

        if (visible and current_y < target_y) or (not visible and current_y > target_y):
            self.chat_frame.place(y=current_y + step)
            self.after(10, lambda: self.animate_chat(visible))
        else:
            self.chat_frame.place(y=target_y)

    # 메세지 보내기
    def send_(self, msg):
        try:
            if not msg or self.socket is None:
                return
            encoded = msg.encode()
            self.socket.send(str(len(encoded)).ljust(16).encode())
            self.socket.send(encoded)
            print("send:", msg)
        except Exception as e:
            print(f"Error in send_(): {e}")

    # 메세지 받기
    def recv(self):
        def recv_all(count):
            buf = b""
            while count:
                new_buf = self.socket.recv(count)
                if not new_buf:
                    return None
                buf += new_buf
                count -= len(new_buf)
            return buf

        while True:
            try:
                if self.socket is None:
                    return
                length = recv_all(16)
                data = recv_all(int(length)).decode()

                if not data:
                    break
                print("recv:", json.loads(data))
                d = json.loads(data)
                if type(d) is str:
                    d = json.loads(d)

                code = d.get("code")
                sign = d.get("sign")
                data = d.get("data")

                if code == 81001:  # login
                    if sign == 1:
                        self.logged_in = True
                        self.id_ = data.get("id")
                        self.name = data.get("name")
                        self.en_id.config(state="disabled")
                        self.bt_login.place_forget()
                        self.bt_logout.place(x=1050, y=35)
                        self.screen_main()
                        self.draw_etc()
                    else:
                        print("login failed")
                        pass
                elif code == 81002:  # logout
                    if sign == 1:
                        self.logged_in = False
                        self.id_ = None
                        self.name = None
                        self.en_id.config(state="normal")
                        self.bt_logout.place_forget()
                        self.bt_login.place(x=1050, y=35)
                        for tab in self.tabs:
                            tab.button.destroy()
                        self.tabs.clear()
                        self.draw_tabs()
                        self.screen_main()
                        self.draw_etc()
                    else:
                        print("logout failed")
                        pass
                elif code == 71003:  # um > msg
                    print("msg:", data)
                elif code in [81004, 71005]:  # appr
                    self.fr_appr.recv(**d)

                # d = json.loads(json.loads(data)) # str로 남아있을 수도 있어서 2번 load
                if callable(getattr(self.app, "recv", None)):
                    self.app.recv(**d)
                else:
                    print("★ 프레임에 recv()가 없음")

            except ConnectionResetError:
                print("recv(): Connection failed")
                break
            except Exception as e:
                print(traceback.format_exc())
                continue

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                self.socket = sock
                self.socket.connect(("localhost", 12345))
                # self.socket.connect(("192.168.0.29", 12345))
                self.screen_main()

                t = threading.Thread(target=self.recv, args=())
                t.daemon = True
                t.start()
                print(self.socket)
                self.mainloop()

        except Exception as e:
            print(traceback.format_exc())


if __name__ == "__main__":
    main = Main()
    main.run()