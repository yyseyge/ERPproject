import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from dateutil.relativedelta import relativedelta
import pymysql
from color import Color
import tablewidget
import json


class PurchasingOrder(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        # --> 날짜
        self.before_one_month = datetime.date.today() - relativedelta(month=2)
        # --->top_left
        self.make_leftframe(948, 350, "solid", "lightgrey", 'New', 0, 0)
        # --->top_right
        self.make_rightframe(350, 350, "solid", "lightgrey", 'Control Box', 0, 1)

        ##top_right의 왼쪽 프레임
        self.fr_rl = tk.Frame(self.fr_right, width=235, height=300, bg="lightgrey")
        self.fr_rl.grid(row=0, column=0)
        self.fr_rl.grid_propagate(False)
        self.fr_rl.pack_propagate(False)

        ##구매오더번호
        self.po_label = tk.Label(self.fr_rl, text="구매오더번호")
        self.po_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)
        self.po_entry = tk.Entry(self.fr_rl, width=20)
        self.po_entry.place(x=95, y=10)

        self.vendor_label = tk.Label(self.fr_rl, text="거래처 코드")
        self.vendor_label.grid(row=1, column=0, sticky='w', pady=10, padx=10)
        self.vendor_entry = tk.Entry(self.fr_rl, width=20)
        self.vendor_entry.place(x=95, y=51)

        self.created_on = tk.Label(self.fr_rl, text="생성 날짜")
        self.created_on.grid(row=2, column=0, sticky='w', pady=10, padx=10)
        self.cal1 = DateEntry(self.fr_rl, width=6, background="darkblue", foreground="white", borderwidth=2,
                              year=self.before_one_month.year, month=self.before_one_month.month,
                              day=self.before_one_month.day)
        self.cal1.place(x=95, y=92)
        self.text = tk.Label(self.fr_rl, text="~", bg='lightgrey')
        self.text.place(x=160, y=92)
        self.cal2 = DateEntry(self.fr_rl, width=6, background="darkblue", foreground="white", borderwidth=2)
        self.cal2.place(x=177, y=92)

        self.dpt_label = tk.Label(self.fr_rl, text="담당 부서")
        self.dpt_label.grid(row=3, column=0, sticky='w', pady=10, padx=10)
        self.dpt_entry = tk.Entry(self.fr_rl, width=20)
        self.dpt_entry.place(x=95, y=133)

        self.name_label = tk.Label(self.fr_rl, text="담당자")
        self.name_label.grid(row=4, column=0, sticky='w', pady=10, padx=10)
        self.name_entry = tk.Entry(self.fr_rl, width=20)
        self.name_entry.place(x=95, y=174)

        ##top_right의 오른쪽 프레임
        self.fr_rr = tk.Frame(self.fr_right, width=102, height=300, bg="lightgrey")
        self.fr_rr.grid(row=0, column=1)
        self.fr_rr.grid_propagate(False)
        self.fr_rr.pack_propagate(False)

        ##버튼
        self.button_r = tk.Button(self.fr_rr, text='조회', command=self.read)
        self.button_r.grid(row=0, column=0, padx=40, pady=5, sticky='ew')
        self.button_c = tk.Button(self.fr_rr, text='생성', command=self.create)
        self.button_c.grid(row=1, column=0, padx=40, pady=5, sticky='ew')
        # self.button_u = tk.Button(self.fr_rr, text='수정')
        # self.button_u.grid(row=2, column=0, padx=40, pady=5, sticky='ew')
        self.button_s = tk.Button(self.fr_rr, text='저장', command=self.save)
        self.button_s.grid(row=2, column=0, padx=40, pady=5, sticky='ew')
        self.button_d = tk.Button(self.fr_rr, text='삭제', command=self.delete)
        self.button_d.grid(row=3, column=0, padx=40, pady=5, sticky='ew')
        self.button_r2 = tk.Button(self.fr_rr, text='상세정보', width=7, height=3, command=self.show_details)
        self.button_r2.grid(row=4, column=0, padx=40, pady=5, sticky='nsew')

        # --->bottom
        self.make_bottom(1300, 350, "solid", "lightgrey", 'Display Box', 1, 0, 2)

        self.bom=''
        self.sign=''
        self.bool_chk=False
        self.bottom_dict = []
        self.dict={}
        self.saved_num=''

    def make_leftframe(self, w, h, r, bg, t, row, col):
        self.fr_left = tk.LabelFrame(self, width=w, height=h, relief=r, bg=bg, text=t)
        self.fr_left.grid(row=row, column=col)
        self.fr_left.grid_propagate(False)
        self.fr_left.pack_propagate(False)

    def make_rightframe(self, w, h, r, bg, t, row, col):
        self.fr_right = tk.LabelFrame(self, width=w, height=h, relief=r, bg=bg, text=t)
        self.fr_right.grid(row=row, column=col)
        self.fr_right.grid_propagate(False)
        self.fr_right.pack_propagate(False)

    def make_bottom(self, w, h, r, bg, t, row, col, cols):
        self.fr_bottom = tk.LabelFrame(self, width=w, height=h, relief=r, bg=bg, text=t)
        self.fr_bottom.grid(row=row, column=col, columnspan=cols)
        self.fr_bottom.grid_propagate(False)
        self.fr_bottom.pack_propagate(False)

    def make_tabw(self, tabname, window, col, col_width, edit_list, data):
        tabname = tablewidget.TableWidget(window,
                                            data=data,
                                            cols=12,
                                            col_name=col,
                                            col_width=col_width,
                                            new_row=False,
                                            editable=edit_list,
                                            width=940,
                                            height=325,
                                            )
        tabname.grid(row=0, column=0)


    def make_condition(self):
        condict = {}
        # 1.구매오더번호
        condict['po_num'] = self.po_entry.get()
        # 2.생성날짜
        if int(self.cal1.get().split('/')[0]) < 10:
            self.mon1 = f"0{self.cal1.get().split('/')[0]}"
        else:
            self.mon1 = self.cal1.get().split('/')[0]
        if int(self.cal1.get().split('/')[1]) < 10:
            self.day1 = f"0{self.cal1.get().split('/')[1]}"
        else:
            self.day1 = self.cal1.get().split('/')[1]

        if int(self.cal2.get().split('/')[0]) < 10:
            self.mon2 = f"0{self.cal2.get().split('/')[0]}"
        else:
            self.mon2 = self.cal2.get().split('/')[0]
        if int(self.cal2.get().split('/')[1]) < 10:
            self.day2 = f"0{self.cal2.get().split('/')[1]}"
        else:
            self.day2 = self.cal2.get().split('/')[1]

        self.dayfrom = f"20{self.cal1.get().split('/')[2]}-{self.mon1}-{self.day1}"
        self.dayto = f"20{self.cal2.get().split('/')[2]}-{self.mon2}-{self.day2}"
        condict['created_on'] = f"{self.dayfrom}~{self.dayto}"

        # 3.거래처코드
        if self.vendor_entry.get() != '':
            condict['vendor'] = self.vendor_entry.get()

        # 4.담당부서
        if self.dpt_entry.get() != '':
            condict['department'] = self.dpt_entry.get()

        # 5.담당자
        if self.name_entry.get() != '':
            condict['manager'] = self.name_entry.get()

        condict['del_flag'] = ''

        print('조건dictionary: ', condict)
        return condict

    def make_top_tab(self):
        self.tab1 = tablewidget.TableWidget(self.fr_left,
                                            data=self.read_dict["data"],
                                            cols=10,
                                            col_name=["구매오더번호", "생산지시서 코드", "담당자", "담당자명", "담당부서", "생성자", "생성일자", "수정인",
                                                      "수정일자", "삭제여부"],
                                            col_width=[80, 100, 80, 80, 100, 80, 140, 80, 140, 60],
                                            new_row=False,
                                            editable=[False, False, False, False, False, False, False, False, False,
                                                      False, ],
                                            width=940,
                                            height=325,
                                            )
        self.tab1.grid(row=0, column=0)


    def read(self):
        if (self.po_entry.get() != '' or self.vendor_entry.get() != '' or
                self.dpt_entry.get() != '' or self.dpt_entry.get() != ''):
            # 프레임 새로생성
            self.make_leftframe(948, 350, "solid", "lightgrey", 'New', 0, 0)
            self.make_bottom(1300, 350, "solid", "lightgrey", 'Display Box', 1, 0, 2)

            # 데이터 조회
            test_dict = {
                "code": 20501,
                "args": self.make_condition()
            }
            self.root.send_(json.dumps(test_dict, ensure_ascii=False))
            # self.read_dict = PurchasingOrder.f20501(code=20501, args=self.make_condition())
            # print('dict1', self.read_dict)
            # self.tab1 = tablewidget.TableWidget(self.fr_left,
            #                                   data=self.read_dict["data"],
            #                                   cols=10,
            #                                   col_name=["구매오더번호", "생산지시서 코드", "담당자", "담당자명", "담당부서", "생성자", "생성일자", "수정인", "수정일자", "삭제여부"],
            #                                   col_width=[80, 100, 80, 80, 100, 80, 140, 80, 140, 60],
            #                                   new_row=False,
            #                                   editable=[False, False, False, False, False, False, False, False, False, False,],
            #                                   width=940,
            #                                   height=325,
            #                                   )
            # self.tab1.grid(row=0, column=0)

        else:
            messagebox.showerror('구매오더', '조회 조건을 입력해주세요.')

    def show_details(self):
        ##condition
        print('details',self.tab1.checked_data())
        condict={'po_num':[]}
        for i in self.tab1.checked_data():
            condict['po_num'].append(i[0])

        test_dict = {
            "code": 20511,
            "args": condict
        }
        self.root.send_(json.dumps(test_dict, ensure_ascii=False))
        # self.detail_dict = PurchasingOrder.f20511(code=20511, args=condict)
        # print('detail',self.detail_dict)

        # self.tab2 = tablewidget.TableWidget(self.fr_bottom,
        #                                     data=self.detail_dict["data"],
        #                                     cols=18,
        #                                     col_name=["구매오더번호", "자재유형", "자재코드", "자재명","거래처코드", "거래처명",
        #                                               "수량", "단위", "총액", "단위","창고", "창고명", "생산지시서 코드",
        #                                               "생성자", "생성일자", "수정인", "수정일자", "삭제여부"],
        #                                     col_width=[80, 60, 100, 120, 80, 140, 80, 60, 100, 60, 80, 100, 120, 80, 140, 80, 140, 60],
        #                                     has_checkbox=False,
        #                                     new_row=False,
        #                                     editable=[False, False, False, False, False, False, False, False, False, False,
        #                                               False, False, False, False, False, False, False, False],
        #                                     width=1290,
        #                                     height=325,
        #                                     )
        # self.tab2.grid(row=0, column=0)

    def create(self):
        self.bool_chk = True
        def open_new_window():
            mo_num=''
            new_window=tk.Toplevel(self.root)
            new_window.title("구매오더 생성")
            new_window.geometry("%dx%d+%d+%d" % (400, 100, 500, 200))
            label_in_new_window=tk.Label(new_window, text="생산지시서 코드를 입력하세요")
            label_in_new_window.grid(row=0, column=0, sticky='w', pady=10, padx=100)
            entry_in_new_window=tk.Entry(new_window, width=18)
            entry_in_new_window.grid(row=1, column=0, sticky='w', padx=100)

            def exit_window():
                nonlocal mo_num
                mo_num=entry_in_new_window.get()
                print('생산지시서번호:',mo_num)
                new_window.destroy()

            button_in_new_window=tk.Button(new_window, text="확인", command=exit_window)
            button_in_new_window.grid(row=1, column=0, padx=250)
            new_window.wait_window()
            return mo_num


        # 프레임 새로생성
        self.make_leftframe(948, 350, "solid", "lightgrey", 'New', 0, 0)
        self.make_bottom(1300, 350, "solid", "lightgrey", 'Display Box', 1, 0, 2)
        # 생산지시서 번호 가져오기
        self.mo_num=open_new_window()
        print('monum살아있는지확인',self.mo_num)

        # 생산지시서코드로 DATA 넣어주기
        #1. 생산지시서 테이블을 통해 BOM코드 가져오기
        condict={}
        print(self.mo_num)
        condict["mo_code"] = self.mo_num
        print(condict)
        test_dict = {
            "code":20521,
            "args":condict
        }
        self.root.send_(json.dumps(test_dict, ensure_ascii=False))

        #2. 생성 시, 구매오더 자동채번
        test_dict = {
            "code":20531,
            "args":{}
        }
        self.root.send_(json.dumps(test_dict, ensure_ascii=False))


    def save(self):
        #생성일 경우
        if self.bool_chk==True:
            chk=''
            condict = {}
            for i in self.tab3.changed['updated'].values():
                for j in range(len(i)):
                    if (j==2 and i[j]=='') or (j==3 and i[j]==''):
                        messagebox.showerror('구매오더 생성', '담당자와 담당부서를 입력해주세요.')
                        chk='F'
                        break
                    if j==0:
                        self.saved_num=i[j]
                    elif j==1:
                        man=i[j]
                    elif j==2:
                        m=i[j]
                    elif j==3:
                        d = i[j]
            if chk=='':
                r = messagebox.askquestion("구매오더 생성", "등록하시겠습니까?")
                if r=='yes':
                    condict={}
                    for i in range(len(self.bottom_dict)):
                        #하나씩 INSERT
                        condict['num']=None
                        condict['po_num']=self.saved_num
                        condict['vendor']=self.bottom_dict[i][4]
                        condict['mat_code']=self.bottom_dict[i][2]
                        condict['quantity']=self.bottom_dict[i][6]
                        condict['measure']=self.bottom_dict[i][7]
                        condict['amount']=self.bottom_dict[i][8]
                        condict['measure2']=None
                        condict['plant']=None
                        condict['manufactoring_code']=man
                        condict['manager']=m
                        condict['department']=d
                        condict['created_by']='USER01'
                        condict['created_on']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        condict['changed_by']=None
                        condict['changed_on']=None
                        condict['del_flag']=None
                        if i==0:
                            condict['stat']='H'
                        else:
                            condict['stat'] = 'B'

                        test_dict = {
                            "code": 20502,
                            "args": condict
                        }
                        self.root.send_(json.dumps(test_dict, ensure_ascii=False))
                    messagebox.showinfo('구매오더 생성', f"오더번호 {self.saved_num}: 등록되었습니다.")
        #생성이 아닐 경우
        else:
            messagebox.showerror("구매오더 생성","[생성]일 경우에만 저장 가능합니다.")

    def delete(self):
        condict={}
        tup=()
        chk=''
        r = messagebox.askquestion("구매오더 삭제", "선택한 오더를 삭제하시겠습니까?")
        if r=='yes':
            for i in self.tab1.checked_data():
                #이미 삭제된 데이터가 포함된 경우(i[9] -> del_flag 필드
                if i[9]!='':
                    messagebox.showerror("구매오더삭제","선택된 오더 중 이미 삭제된 데이터가 있습니다. [삭제여부]필드를 확인하세요.")
                    chk='F'
                    break
                if len(self.tab1.checked_data()) > 1:
                    tup += (i[0],)
                else:
                    tup = (i[0])

            if chk=='':
                condict['po_num'] = tup
                print('tup', tup)

                test_dict = {
                    "code": 20503,
                    "args": condict
                }
                self.root.send_(json.dumps(test_dict, ensure_ascii=False))



    def after_init(self):
        pass

    def data_info(self):
        print(f"data: {self.tab4.data}")  # 저장된 데이터
        print(f"rows cols: {self.tab4.rows} {self.tab1.cols}")  # 행 열 개수
        print(f"selected: {self.tab4.selected_row} {self.tab1.selected_col}")  # 선택된 행 열 index
        print(f"changed {self.tab4.changed}")  # 원본 대비 변경된 데이터


    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))
        code = kwargs.get("code")
        sign = kwargs.get("sign")
        data = kwargs.get("data")
        if code == 20501 and sign==1:
            self.tab1 = tablewidget.TableWidget(self.fr_left,
                                                data=data,
                                                cols=10,
                                                col_name=["구매오더번호", "생산지시서 코드", "담당자", "담당자명", "담당부서", "생성자", "생성일자",
                                                          "수정인", "수정일자", "삭제여부"],
                                                col_width=[80, 100, 80, 80, 100, 80, 140, 80, 140, 60],
                                                new_row=False,
                                                editable=[False, False, False, False, False, False, False, False, False,
                                                          False, ],
                                                width=940,
                                                height=325,
                                                )
            self.tab1.grid(row=0, column=0)
        elif code == 20511 and sign==1:
            self.tab2 = tablewidget.TableWidget(self.fr_bottom,
                                                data=data,
                                                cols=18,
                                                col_name=["구매오더번호", "자재유형", "자재코드", "자재명", "거래처코드", "거래처명",
                                                          "수량", "단위", "총액", "단위", "창고", "창고명", "생산지시서 코드",
                                                          "생성자", "생성일자", "수정인", "수정일자", "삭제여부"],
                                                col_width=[80, 60, 100, 120, 80, 140, 80, 60, 100, 60, 80, 100, 120, 80,
                                                           140, 80, 140, 60],
                                                has_checkbox=False,
                                                new_row=False,
                                                editable=[False, False, False, False, False, False, False, False, False,
                                                          False,
                                                          False, False, False, False, False, False, False, False],
                                                width=1290,
                                                height=325,
                                                )
            self.tab2.grid(row=0, column=0)
        elif code == 20521 and sign==1:
            self.sign=''
            if data!=[]:
                self.dict=data
            else:
                self.sign='F'
                messagebox.showerror('구매오더', '생산지시서 코드가 유효하지 않습니다.')


        elif code == 20531 and sign==1:
            if self.sign == '':
                max_code=data
                if max_code < 10:
                    max_code = f'po000{max_code}'
                elif max_code < 100:
                    max_code = f'po00{max_code}'
                elif max_code < 1000:
                    max_code = f'po000{max_code}'

                # TOP에 보여줄 dict만들기
                top_dict = [max_code, self.mo_num, '', '']

                # 2. BOM코드로 해당하는 상세정보 가져오기
                condict = {}
                dd = []
                self.bottom_dict = []
                for i in self.dict:
                    dd = []
                    dd.append(max_code)
                    for j in range(len(i)):
                        if j == 5:  # 갯수저장
                            q = int(i[j])
                            dd.append(q)
                        elif j == 7:  # 가격계산
                            if i[j]==None:
                                p=0
                            else:
                                p = (q * int(i[j])) * 1.1
                            dd.append(round(p))
                        else:
                            dd.append(i[j])
                    dd.append('')  # 창고
                    dd.append('')  # 창고명
                    dd.append(self.mo_num)  # 생산지시서코드
                    self.bottom_dict.append(dd)
                print("bottom", self.bottom_dict)

                # 생성날짜
                self.today = tk.Label(self.fr_left, text='생성 날짜:', background="lightgrey")
                self.today.grid(row=0, column=0, sticky='w', padx=5, pady=5)
                self.today_entry = tk.Entry(self.fr_left, width=12, state='normal')
                self.today_entry.insert(0, str(datetime.date.today()))
                self.today_entry.grid(row=0, column=0, sticky='w', padx=70, pady=5)

                # 생성자ID
                self.creatId = tk.Label(self.fr_left, text='생성자ID:', background="lightgrey")
                self.creatId.grid(row=0, column=0, sticky='w', padx=170, pady=5)
                self.creatId_entry = tk.Entry(self.fr_left, width=12, state='normal')
                self.creatId_entry.insert(0, 'USER01')
                self.creatId_entry.grid(row=0, column=0, sticky='w', padx=228, pady=5)
                self.exlabel1 = tk.Label(self.fr_left, text='*구매오더 번호는 자동 채번됩니다.', font=("맑은 고딕", 8), fg="red",
                                         background="lightgrey")
                self.exlabel1.grid(row=1, column=0, sticky='w', padx=5)
                self.exlabel2 = tk.Label(self.fr_left, text='*구매오더 정보는 입력하신 생산지시서 코드의 항목대로 저장됩니다.', font=("맑은 고딕", 8),
                                         fg="red", background="lightgrey")
                self.exlabel2.grid(row=2, column=0, sticky='w', padx=5)
                self.exlabel3 = tk.Label(self.fr_left, text='*담당자, 담당부서 칸에 해당되는 [코드]로 정보를 기입해주세요.', font=("맑은 고딕", 8),
                                         fg="red", background="lightgrey")
                self.exlabel3.grid(row=3, column=0, sticky='w', padx=5)
                self.exlabel4 = tk.Label(self.fr_left, text='*하단의 창고정보는 입고 처리 후 자동기입 됩니다.', font=("맑은 고딕", 8), fg="red",
                                         background="lightgrey")
                self.exlabel4.grid(row=4, column=0, sticky='w', padx=5)

                self.tab3 = tablewidget.TableWidget(self.fr_left,
                                                    data=[top_dict],
                                                    cols=4,
                                                    col_name=["구매오더번호", "생산지시서 코드", "담당자", "담당부서"],
                                                    col_width=[80, 100, 80, 100],
                                                    new_row=False,
                                                    editable=[False, False, True, True],
                                                    width=940,
                                                    height=180,
                                                    )
                self.tab3.grid(row=5, column=0, pady=5)
                self.tab4 = tablewidget.TableWidget(self.fr_bottom,
                                                    data=self.bottom_dict,
                                                    cols=12,
                                                    col_name=[
                                                        "구매오더번호", "자재유형", "자재코드", "자재명", "거래처코드", "거래처명",
                                                        "수량", "단위", "총액", "창고", "창고명", "생산지시서코드"],
                                                    col_width=[100, 80, 80, 80, 80, 120, 50, 50, 80, 80, 100, 100],
                                                    new_row=False,
                                                    editable=[False, False, False, False, False, False, False, False, False,
                                                              False, False, False],
                                                    width=1290,
                                                    height=325,
                                                    has_checkbox=False
                                                    )
                self.tab4.grid(row=0, column=0)

        elif code == 20502 and sign==1:
            pass
        elif code == 20503 and sign==1:
            messagebox.showinfo('삭제', '정상적으로 삭제되었습니다. 삭제 여부 필드를 확인하세요.')
            self.read()

if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = PurchasingOrder(r)
    fr.place(x=300, y=130)
    r.mainloop()


###############################구매요청서############################
    # @staticmethod
    # @MsgProcessor
    # def f20501(**kwargs):
    #     DataBase = dbm
    #     condition = ''
    #
    #     def select_data(condition):
    #         selected_data = DataBase.query(f"""
    #         SELECT p.po_num, p.manufactoring_code,
    #                p.manager, e.name, p.department,
    #                p.created_by, p.created_on, p.changed_by, p.changed_on,
    #                p.del_flag
    #           FROM erp_db.purchasing_order as p LEFT OUTER JOIN erp_db.employee as e
    #             ON p.manager = e.employee_code
    #          WHERE {condition}
    #            AND p.stat = 'H';
    #         """)  # HEADER인 데이터만 가져오기
    #
    #         #날짜필드 변환
    #         selected_data = [list(i) for i in selected_data]
    #         for i, v in enumerate(selected_data):
    #             for j, w in enumerate(v):
    #                 if type(w) is datetime.datetime:
    #                     selected_data[i][j] = w.strftime("%Y-%m-%d %H:%M:%S")
    #
    #         return selected_data
    #
    #     for key, value in kwargs.items():
    #         if key == 'po_num':
    #             if '%' in value:
    #                 condition += f"po_num like '{value}' and "
    #             else:
    #                 condition += f"po_num='{value}' and "
    #
    #         elif key == 'created_on':
    #             condition += f"DATE(created_on)>='{value.split('~')[0]}' and DATE(created_on)<='{value.split('~')[1]}'"
    #
    #         elif key == 'vendor':
    #             if '%' in value:
    #                 condition += f" and vendor like '{value}'"
    #             else:
    #                 condition += f" and vendor='{value}'"
    #
    #         elif key == 'department':
    #             if '%' in value:
    #                 condition += f" and department like '{value}'"
    #             else:
    #                 condition += f" and department='{value}'"
    #
    #         elif key == 'manager':
    #             if '%' in value:
    #                 condition += f" and manager like '{value}'"
    #             else:
    #                 condition += f" and manager='{value}'"
    #
    #     print('condition:', condition)
    #     test_data = select_data(condition)
    #     # 실패:0, 성공:1
    #     if test_data != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20511(**kwargs):
    #     DataBase = dbm
    #     condition = ''
    #
    #     def select_data(condition):
    #         selected_data = DataBase.query(f"""
    #                 SELECT po.po_num, m.materialType, po.mat_code, m.materialName,
    #                        po.vendor, v.Customer_name,
    #                        po.quantity, po.measure, po.amount, po.measure, po.plant,
    #                        p.plant_name, po.manufactoring_code,
    #                        po.created_by, po.created_on, po.changed_by, po.changed_on, po.del_flag
    #                   FROM erp_db.purchasing_order AS po LEFT OUTER JOIN erp_db.mtable4 AS m
    #                     ON po.mat_code = m.materialCode LEFT OUTER JOIN erp_db.plant AS p
    #                     ON po.plant = p.plant_code      LEFT OUTER JOIN erp_db.Customer_management as v
    #                     ON po.vendor = v.ID
    #                  WHERE {condition}
    #                  ORDER BY po.po_num;
    #                 """)
    #
    #         selected_data = [list(i) for i in selected_data]
    #         for i, v in enumerate(selected_data):
    #             for j, w in enumerate(v):
    #                 if type(w) is datetime.datetime:
    #                     selected_data[i][j] = w.strftime("%Y-%m-%d %H:%M:%S")
    #
    #         return selected_data
    #
    #     for key, value in kwargs.items():
    #         cond = str(value).replace('[', '(')
    #         cond = cond.replace(']', ')')
    #         condition += f"po_num IN {cond}"
    #
    #     test_data = select_data(condition)
    #     # 실패:0, 성공:1
    #     if test_data != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20521(**kwargs):
    #     DataBase = dbm
    #     condition = ''
    #
    #     # 생산지시서코드로 BOM코드 가져오기
    #     for key, value in kwargs.items():
    #         selected_data = DataBase.query(f"""select m.materialType, b.material_code, m.materialName, m.correspondentCode,
    #                                             c.Customer_name, b.quantity, m.unit, m.price
    #                                       from erp_db.bom_f as b left outer join erp_db.mtable4 as m
    #                                         on b.material_code=m.materialCode
    #                                                              left outer join erp_db.customer_management as c
    #                                         on m.correspondentCode = c.ID
    #                                     where b.bom_code=(select bom_code from erp_db.mo where mo_code='{value}');""")
    #     print(selected_data)
    #
    #     if selected_data != None:
    #         return {"sign": 1, "data": selected_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20531(**kwargs):
    #     DataBase = dbm
    #     max_code = int(DataBase.query(f"SELECT max(po_num) FROM erp_db.purchasing_order;")[0][0][2:6]) + 1
    #
    #     if max_code != None:
    #         return {"sign": 1, "data": max_code}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20502(**kwargs):
    #     DataBase = dbm
    #     condition = ''
    #
    #     def insert_data(condition):
    #         selected_data = DataBase.query(f"INSERT INTO `erp_db`.`purchasing_order` VALUES ({condition});")
    #         return selected_data
    #
    #     for key, value in kwargs.items():
    #         if value != None:
    #             condition += f"'{value}'"
    #         else:
    #             condition += "NULL"
    #
    #         if key != 'stat':
    #             condition += ','
    #
    #     print('condition', condition)
    #     result = insert_data(condition)
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": result}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20503(**kwargs):
    #     DataBase = dbm
    #     condition = ''
    #
    #     def delete_data(condition):
    #         selected_data = DataBase.query(f"UPDATE `erp_db`.`purchasing_order` SET `del_flag`='X' WHERE ({condition});")
    #         return selected_data
    #
    #     def select_data():
    #         selected_data = DataBase.query(f"SELECT * FROM erp_db.purchasing_order")
    #         selected_data = [list(i) for i in selected_data]
    #         for i, v in enumerate(selected_data):
    #             for j, w in enumerate(v):
    #                 if type(w) is datetime.datetime:
    #                     selected_data[i][j] = w.strftime("%Y-%m-%d %H:%M:%S")
    #         return selected_data
    #
    #     for key, value in kwargs.items():
    #         if type(kwargs['po_num']) is str:
    #             condition = f"po_num='{value}'"
    #         else:
    #             condition = f"po_num IN {value}"
    #
    #     result = delete_data(condition)
    #     test_data = select_data()
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    ###########################################################