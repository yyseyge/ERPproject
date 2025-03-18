
import tkinter as tk
import pymysql
import tablewidget
# import DB
import datetime
from dateutil.relativedelta import relativedelta
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json


class Plant(tk.Frame):
    # DataBase = DB.ConnectDB

    def __init__(self,root):
        super().__init__(root, width=1300, height=700)
        self.root = root
        #--> 날짜
        self.before_one_month = datetime.date.today() - relativedelta(month=2)
        #--->top_left
        self.fr_left=tk.LabelFrame(self, width=948, height=350, relief="solid", bg="lightgrey", text='New')
        self.fr_left.grid(row=0, column=0)
        self.fr_left.grid_propagate(False)
        self.fr_left.pack_propagate(False)
            ##창고코드
        self.plant_label=tk.Label(self.fr_left, text="창고코드")
        self.plant_label.place(x=50, y=40)
        self.plant_entry=tk.Entry(self.fr_left, width=10, state='disabled', disabledbackground='lightgrey')
        self.plant_entry.place(x=150, y=40)
            ##창고명
        self.name_label=tk.Label(self.fr_left, text="창고명")
        self.name_label.place(x=50, y=80)
        self.name_entry=tk.Entry(self.fr_left, width=20, state='disabled', disabledbackground='lightgrey')
        self.name_entry.place(x=150, y=80)
            ##창고위치
        self.loc_label=tk.Label(self.fr_left, text="창고위치")
        self.loc_label.place(x=50, y=120)
        self.loc_entry=tk.Entry(self.fr_left, width=50, state='disabled', disabledbackground='lightgrey')
        self.loc_entry.place(x=150, y=120)
            ##전화번호
        self.phone_label=tk.Label(self.fr_left, text="전화번호")
        self.phone_label.place(x=50, y=160)
        self.phone_entry1=tk.Entry(self.fr_left, width=6, state='disabled', disabledbackground='lightgrey')
        self.phone_entry1.place(x=150, y=160)
        self.phone_entry2=tk.Entry(self.fr_left, width=6, state='disabled', disabledbackground='lightgrey')
        self.phone_entry2.place(x=200, y=160)
        self.phone_entry3=tk.Entry(self.fr_left, width=6, state='disabled', disabledbackground='lightgrey')
        self.phone_entry3.place(x=250, y=160)
            ##FAX
        self.fax_label=tk.Label(self.fr_left, text="FAX")
        self.fax_label.place(x=50, y=200)
        self.fax_entry=tk.Entry(self.fr_left, width=20, state='disabled', disabledbackground='lightgrey')
        self.fax_entry.place(x=150, y=200)

            ##E-Mail
        self.mail_label=tk.Label(self.fr_left, text="E-Mail")
        self.mail_label.place(x=50, y=240)
        self.mail_entry=tk.Entry(self.fr_left, width=15, state='disabled', disabledbackground='lightgrey')
        self.mail_entry.place(x=150, y=240)
        self.text2=tk.Label(self.fr_left, text="@", bg='lightgrey')
        self.text2.place(x=258, y=240)
        self.mail_entry2=tk.Entry(self.fr_left, width=15, state='disabled', disabledbackground='lightgrey')
        self.mail_entry2.place(x=275, y=240)
        self.mail_combo=ttk.Combobox(self.fr_left, width=15, state='disabled', values=['gmail.com','naver.com','daum.net','hanmail.net','직접 작성'])
        self.mail_combo.place(x=395, y=240)
        self.mail_combo.set("선택하세요")
        self.mail_combo.bind("<<ComboboxSelected>>", self.open_mail_add)
        self.l1 = [self.plant_entry, self.name_entry, self.loc_entry, self.phone_entry1, self.phone_entry2,
                   self.phone_entry3, self.fax_entry, self.mail_entry, self.mail_entry2, self.mail_combo]
        #--->top_right
        self.fr_right=tk.LabelFrame(self, width=350, height=350, relief="solid", bg="lightgrey", text='Control Box')
        self.fr_right.grid(row=0, column=1)
        self.fr_right.grid_propagate(False)
        self.fr_right.pack_propagate(False)
            ##창고코드
        self.plant_label2=tk.Label(self.fr_right, text="창고코드")
        self.plant_label2.place(x=30, y=40)
        self.plant_combo2=ttk.Combobox(self.fr_right, state="readonly", width=19)
        self.plant_combo2.place(x=90, y=40)
            ##창고명
        self.name_label2=tk.Label(self.fr_right, text="창고명")
        self.name_label2.place(x=30, y=80)
        self.name_entry2=tk.Entry(self.fr_right, width=21)
        self.name_entry2.place(x=90, y=80)
            ##생성날짜
        self.created_on=tk.Label(self.fr_right, text="생성날짜")
        self.created_on.place(x=30, y=120)
        self.cal1 = DateEntry(self.fr_right, width=7, background="darkblue", foreground="white", borderwidth=2, year=self.before_one_month.year, month=self.before_one_month.month, day=self.before_one_month.day)
        self.cal1.place(x=90, y=120)
        self.text=tk.Label(self.fr_right, text="~", bg='lightgrey')
        self.text.place(x=160, y=120)
        self.cal2 = DateEntry(self.fr_right, width=7, background="darkblue", foreground="white", borderwidth=2)
        self.cal2.place(x=174, y=120)
            ##생성자
        self.created_by=tk.Label(self.fr_right, text="생성자")
        self.created_by.place(x=30, y=160)
        self.created_by_entry=tk.Entry(self.fr_right, width=21)
        self.created_by_entry.place(x=90, y=160)
            ##버튼
        self.make_button('조회', self.read, 280, 40)
        self.make_button('생성', self.create, 280, 70)
        self.make_button('수정', self.update, 280, 100)
        self.make_button('저장', self.save, 280, 130)
        self.make_button('사용불가', self.delete, 280, 160)
            ##설명
        self.exlabel1=tk.Label(self.fr_right, text='*창고생성: [생성] -> [저장]', font=("맑은 고딕",8), fg="red", background="lightgrey")
        self.exlabel1.place(x=23, y=230)
        self.exlabel2=tk.Label(self.fr_right, text='*창고수정: [조회] -> [수정] -> [저장]', font=("맑은 고딕",8), fg="red", background="lightgrey")
        self.exlabel2.place(x=23, y=250)
        self.exlabel5=tk.Label(self.fr_right, text='*수정 가능 필드: 창고명, 위치, 전화번호, Fax, E-Mail', font=("맑은 고딕",8), fg="red", background="lightgrey")
        self.exlabel5.place(x=23, y=270)
        self.exlabel3=tk.Label(self.fr_right, text='*조회조건 입력 시, "%"문자를 이용하여 다량 데이터 조회 가능', font=("맑은 고딕",8), fg="red", background="lightgrey")
        self.exlabel3.place(x=23, y=290)
        self.exlabel4=tk.Label(self.fr_right, text='ex.창고명="%창고"', font=("맑은 고딕",8), fg="red", background="lightgrey")
        self.exlabel4.place(x=235, y=310)



        #--->bottom
        self.fr_bottom=tk.LabelFrame(self, width=1300, height=350, relief="solid", bg="lightgrey", text='Display Box')
        self.fr_bottom.grid(row=1, column=0, columnspan=2)
        self.fr_bottom.grid_propagate(False)
        self.fr_bottom.pack_propagate(False)

        self.bool_chk=False
        self.condition=''
        self.selected_data=[]
        self.dict={}

        self.load_plantcode()

    def make_button(self, t, c, x, y):
        self.button_d=tk.Button(self.fr_right, text=t, command=c)
        self.button_d.place(x=x, y=y)

    def load_plantcode(self):
        test_dict = {
            "code": 20656,
            "args": {}
        }
        self.root.send_(json.dumps(test_dict, ensure_ascii=False))

        # self.DataBase.connection_DB(self.DataBase)
        # tables=self.DataBase.query('SELECT plant_code FROM erp_test.plant WHERE del_flag is NULL;')
        # tb = ['전체']
        # for i in tables:
        #     tb.append(i[0])
        #
        # self.plant_combo2["values"]=tb
        # DB.ConnectDB.close(self.DataBase)

    def open_mail_add(self,e=None):
        if self.mail_combo.get() == '직접 작성':
            self.mail_entry2.configure(state='normal', background='white')
        else:
            self.mail_entry2.configure(state='disabled', disabledbackground='lightgrey')


    def make_condition(self):
        condict={}
        #1.창고코드
        if self.plant_combo2.get() != '전체':
            condict['plant_code']=self.plant_combo2.get()

        #2.생성날짜
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
        condict['created_on']=f"{self.dayfrom}~{self.dayto}"

        #3.창고명
        if self.name_entry2.get() != '':
            condict['plant_name']=self.name_entry2.get()

        #4.생성자
        if self.created_by_entry.get() != '':
            condict['created_by']=self.created_by_entry.get()

        condict['del_flag']=''

        print('조건dictionary: ',condict)
        return condict

    def make_tabw(self,edit_list):
        col = ['창고코드', '창고명', '위치', '전화번호', 'Fax', 'E-mail', '생성자', '생성날짜', '수정인', '수정날짜', '삭제여부']
        self.tab1 = tablewidget.TableWidget(self.fr_bottom,
                                            data=self.dict,
                                            cols=11,
                                            col_name=col,
                                            col_width=[120, 120, 200, 150, 150, 160, 120, 130, 120, 130, 60],
                                            new_row=False,
                                            editable=edit_list,
                                            width=1280,
                                            height=300,
                                            )
        self.tab1.grid(row=0, column=0)


    # @staticmethod
    # def f20651(**kwargs):
    #     DataBase = DB.ConnectDB
    #     condition=''
    #     def select_data(condition):
    #         DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(DataBase,f"SELECT * FROM erp_test.plant WHERE {condition};")
    #         DataBase.close(DataBase)
    #         return selected_data
    #
    #     for key,value in kwargs['args'].items():
    #         if key=='plant_code':
    #             condition += f"plant_code='{value}' and "
    #
    #         elif key=='created_on':
    #             condition += f"DATE(created_on)>='{value.split('~')[0]}' and DATE(created_on)<='{value.split('~')[1]}'"
    #
    #         elif key=='plant_name':
    #             if '%' in value:
    #                 condition += f" and plant_name like '{value}'"
    #             else:
    #                 condition += f" and plant_name='{value}'"
    #
    #         elif key=='created_by':
    #             if '%' in value:
    #                 condition += f" and created_by like '{value}'"
    #             else:
    #                 condition += f" and created_by='{value}'"
    #
    #         # elif key=='del_flag':
    #         #     condition += f" and del_flag IS NULL"
    #
    #     print('condition:',condition)
    #     test_data=select_data(condition)
    #     # 실패:0, 성공:1
    #     if test_data != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # def f20652(**kwargs):
    #     DataBase = DB.ConnectDB
    #     condition = ''
    #     def select_data():
    #         DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(DataBase,f"SELECT * FROM erp_test.plant WHERE del_flag IS NULL;")
    #         DataBase.close(DataBase)
    #         return selected_data
    #
    #     def insert_data(condition):
    #         DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(DataBase,f"INSERT INTO `erp_test`.`plant` VALUES ({condition});")
    #         DataBase.close(DataBase)
    #         return selected_data
    #
    #     for key, value in kwargs['args'].items():
    #         if value != None:
    #             condition+=f"'{value}'"
    #         else:
    #             condition += "NULL"
    #
    #         if key != 'del_flag':
    #             condition+=','
    #
    #     result=insert_data(condition)
    #     test_data=select_data()
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # def f20653(**kwargs):
    #     DataBase = DB.ConnectDB
    #     condition = ''
    #     def update_data(condition,key):
    #         DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(DataBase,f"""
    #                             UPDATE `erp_test`.`plant`
    #                             SET {condition}
    #                             WHERE plant_code = '{key}';""")
    #         DataBase.close(DataBase)
    #         return selected_data
    #
    #     def select_data():
    #         DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(DataBase,f"SELECT * FROM erp_test.plant WHERE del_flag IS NULL;")
    #         DataBase.close(DataBase)
    #         return selected_data
    #
    #     for key, value in kwargs['args'].items():
    #         if key != 'changed_on':
    #             if value==None:
    #                 condition += (f"{key}=null,")
    #             else:
    #                 condition += (f"{key}='{value}',")
    #         else :
    #             condition += (f"{key}='{value}'")
    #         print('condition',condition)
    #     result=update_data(condition,kwargs['args']['plant_code'])
    #     test_data=select_data()
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    #
    #
    # @staticmethod
    # def f20654(**kwargs):
    #     DataBase = DB.ConnectDB
    #     condition=''
    #     def delete_data(condition):
    #         DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(DataBase,f"UPDATE `erp_test`.`plant` SET `del_flag`='X' WHERE ({condition});")
    #         DataBase.close(DataBase)
    #         return selected_data
    #
    #     def select_data():
    #         DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(DataBase,f"SELECT * FROM erp_test.plant")
    #         # selected_data = DataBase.query(DataBase,f"SELECT * FROM erp_test.plant WHERE del_flag IS NULL;")
    #         DataBase.close(DataBase)
    #         return selected_data
    #
    #     for key, value in kwargs['args'].items():
    #         if type(kwargs['args']['plant_code']) is str:
    #             condition=f"plant_code='{value}'"
    #         else:
    #             condition=f"plant_code IN {value}"
    #
    #     result = delete_data(condition)
    #     test_data = select_data()
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}

    def read(self):
        if self.plant_combo2.get() == '':
            messagebox.showerror('창고조회', '창고 코드를 선택해주세요.')
        else:
            test_dict = {
                "code": 20651,
                "args": self.make_condition()
            }
            print(test_dict)
            self.root.send_(json.dumps(test_dict, ensure_ascii=False))


            # self.dict=Plant.f20651(code=20651,args=self.make_condition())
            # self.make_tabw([False, False, False, False, False, False, False, False, False, False, False])

    def create(self):
        if self.bool_chk==False:
            for i in range(len(self.l1)):
                if i== 8:
                    continue
                if i== 9:
                    print(self.l1[i])
                    self.l1[i].configure(state='readonly', background='white')
                else:
                    self.l1[i].configure(state='normal', background='white')

                # 생성 시, 창고번호 자동채번
                if i == 0:
                    test_dict = {
                        "code": 20655,
                        "args": {}
                    }
                    self.root.send_(json.dumps(test_dict, ensure_ascii=False))

            self.bool_chk=True

        else:
            for i in range(len(self.l1)):
                self.l1[i].configure(state='normal', background='white')
                self.l1[i].delete(0,'end')
                self.l1[i].configure(state='disabled', background='lightgrey')
            self.bool_chk=False


    def update(self):
        self.make_tabw([False, True, True, True, True, True, False, False, False, False, False])



    def save(self):
        #[생성]일 경우
        if self.bool_chk==True:
            if self.plant_entry.get() == '' or self.name_entry.get() == '':
                messagebox.showerror('창고신규','창고 코드와, 창고 이름을 작성 후 "저장"버튼을 눌러주세요.')
            else:
                r=messagebox.askquestion("창고","등록하시겠습니까?")
                if r=='yes':
                    condict = {}
                    condict['plant_code'] = self.plant_entry.get()
                    condict['plant_name'] = self.name_entry.get()

                    if self.loc_entry.get() != '':
                        condict['location'] = self.loc_entry.get()
                    else:
                        condict['location'] = None

                    if self.phone_entry1.get() != '':
                        condict['phone'] = (self.phone_entry1.get()+self.phone_entry2.get()+self.phone_entry3.get())
                    else:
                        condict['phone'] = None

                    if self.fax_entry.get() != '':
                        condict['fax'] = self.fax_entry.get()
                    else:
                        condict['fax'] = None

                    if self.mail_entry.get() != '':
                        #직접입력일 경우,
                        if self.mail_entry2.get() != '':
                            address=self.mail_entry2.get()
                        else:
                            address=self.mail_combo.get()
                        condict['email'] = f"{self.mail_entry.get()}@{address}"
                        print(condict['email'])
                    else:
                        condict['email'] = None

                    condict['created_by'] = 'USER01'  # 임의로 넣어줌, 추후 수정
                    condict['created_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    condict['changed_by'] = None
                    condict['changed_on'] = None
                    condict['del_flag'] = None

                    test_dict = {
                        "code": 20652,
                        "args": condict
                    }
                    self.root.send_(json.dumps(test_dict, ensure_ascii=False))

        #[수정]일 경우
        else:
            condict = {}
            #한 줄씩 update
            for i in self.tab1.changed['updated'].values():
                condict['plant_code'] = i[0]
                condict['plant_name'] = i[1]
                condict['location'] = i[2]
                condict['phone'] = i[3]
                condict['fax'] = i[4]
                condict['email'] = i[5]
                condict['changed_by'] = 'USER01'
                condict['changed_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print('condict',condict)
                test_dict = {
                    "code": 20653,
                    "args": condict
                }
                self.root.send_(json.dumps(test_dict, ensure_ascii=False))

    def delete(self):
        condict = {}
        tup=()
        chk=''
        for i in self.tab1.checked_data():
            #이미 삭제된 데이터가 포함된 경우 (i[10]->del_flag필드)
            if i[10]!='':
                messagebox.showerror("창고사용불가","현재 사용중인 창고만 사용불가 처리 가능합니다. [삭제여부]필드를 확인하세요.")
                chk='F'
                break
            if len(self.tab1.checked_data())>1:
                tup+=(i[0],)
            else:
                tup=(i[0])
        if chk=='':
            condict['plant_code']=tup
            print('tup',tup)
            test_dict = {
                "code": 20654,
                "args": condict
            }
            self.root.send_(json.dumps(test_dict, ensure_ascii=False))
            # self.dict = Plant.f20654(code=20654, args=condict)

    def after_init(self):
        pass

    def data_info(self):
        print(f"data: {self.tab1.data}")  # 저장된 데이터
        print(f"rows cols: {self.tab1.rows} {self.tab1.cols}")  # 행 열 개수
        print(f"selected: {self.tab1.selected_row} {self.tab1.selected_col}")  # 선택된 행 열 index
        print(f"changed {self.tab1.changed}")  # 원본 대비 변경된 데이터

    def recv(self, **kwargs):
        print("code:", kwargs.get("code"))
        print("sign:", kwargs.get("sign"))
        print("data:", kwargs.get("data"))
        code = kwargs.get("code")
        sign = kwargs.get("sign")
        data = kwargs.get("data")
        if code == 20651:
            self.dict=data
            self.make_tabw([False, False, False, False, False, False, False, False, False, False, False])
        elif code == 20652 and sign==1:
            self.dict = data
            print('dict:', self.dict)
            # 성공일 경우 entry 잠궈주고, 재조회
            self.load_plantcode()
            for i in self.l1:
                if i == self.mail_combo:
                    i.configure(state='normal')
                    i.delete(0, 'end')
                    i.configure(state='disabled')
                else:
                    i.configure(state='normal')
                    i.delete(0, 'end')
                    i.configure(state='disabled', disabledbackground='lightgrey')
            self.make_tabw([False, False, False, False, False, False, False, False, False, False, False])
            self.bool_chk = False
        elif code == 20653 and sign==1:
            self.load_plantcode()
            self.dict=data
            messagebox.showinfo('수정','정상적으로 수정되었습니다.')
            self.make_tabw([False, False, False, False, False, False, False, False, False, False])
        elif code == 20654 and sign==1:
            self.load_plantcode()
            self.dict = data
            messagebox.showinfo('창고삭제', '정상적으로 삭제되었습니다.')
            self.make_tabw([False, False, False, False, False, False, False, False, False, False])
        elif code == 20655:
            max_code=data
            if max_code < 10:
                self.l1[0].insert(0, f'P00{max_code}')
            elif max_code < 100:
                self.l1[0].insert(0, f'P0{max_code}')
            elif max_code < 1000:
                self.l1[0].insert(0, f'P{max_code}')
            self.l1[0].configure(state='disabled', background='lightgrey')

        elif code==20656:
            tb = ['전체']
            for i in data:
                tb.append(i[0])

            self.plant_combo2["values"]=tb



# 테스트용 코드
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1600x900")
    r.config(bg="white")
    fr = Plant(r)
    fr.place(x=300, y=130)
    fr.load_plantcode()
    r.mainloop()



######창고등록마스터#######################################################
    #
    # @staticmethod
    # @MsgProcessor
    # def f20651(**kwargs):
    #     # DataBase = DB.ConnectDB
    #     DataBase = dbm
    #     condition = ''
    #
    #     def select_data(condition):
    #         # DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(f"SELECT * FROM erp_db.plant WHERE {condition};")
    #         selected_data = [list(i) for i in selected_data]
    #         for i, v in enumerate(selected_data):
    #             for j, w in enumerate(v):
    #                 if type(w) is datetime.datetime:
    #                     selected_data[i][j] = w.strftime("%Y-%m-%d %H:%M:%S")
    #
    #         # DataBase.close(DataBase)
    #         return selected_data
    #
    #     # for key, value in kwargs['args'].items():
    #     for key, value in kwargs.items():
    #         if key == 'plant_code':
    #             condition += f"plant_code='{value}' and "
    #
    #         elif key == 'created_on':
    #             condition += f"DATE(created_on)>='{value.split('~')[0]}' and DATE(created_on)<='{value.split('~')[1]}'"
    #
    #         elif key == 'plant_name':
    #             if '%' in value:
    #                 condition += f" and plant_name like '{value}'"
    #             else:
    #                 condition += f" and plant_name='{value}'"
    #
    #         elif key == 'created_by':
    #             if '%' in value:
    #                 condition += f" and created_by like '{value}'"
    #             else:
    #                 condition += f" and created_by='{value}'"
    #
    #         # elif key=='del_flag':
    #         #     condition += f" and del_flag IS NULL"
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
    # def f20652(**kwargs):
    #     # DataBase = DB.ConnectDB
    #     DataBase = dbm
    #     condition = ''
    #
    #     def select_data():
    #         # DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(f"SELECT * FROM erp_db.plant WHERE del_flag IS NULL;")
    #         # DataBase.close(DataBase)
    #         selected_data = [list(i) for i in selected_data]
    #         for i, v in enumerate(selected_data):
    #             for j, w in enumerate(v):
    #                 if type(w) is datetime.datetime:
    #                     selected_data[i][j] = w.strftime("%Y-%m-%d %H:%M:%S")
    #
    #
    #         return selected_data
    #
    #     def insert_data(condition):
    #         # DataBase.connection_DB(DataBase)
    #         selected_data = DataBase.query(f"INSERT INTO `erp_db`.`plant` VALUES ({condition});")
    #         # DataBase.close(DataBase)
    #         return selected_data
    #
    #     for key, value in kwargs.items():
    #         if value != None:
    #             condition += f"'{value}'"
    #         else:
    #             condition += "NULL"
    #
    #         if key != 'del_flag':
    #             condition += ','
    #
    #     result = insert_data(condition)
    #     test_data = select_data()
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20653(**kwargs):
    #     # DataBase = DB.ConnectDB
    #     DataBase = dbm
    #     condition = ''
    #
    #     def update_data(condition, key):
    #         selected_data = DataBase.query(f"""
    #                                UPDATE `erp_db`.`plant`
    #                                SET {condition}
    #                                WHERE plant_code = '{key}';""")
    #         return selected_data
    #
    #     def select_data():
    #         selected_data = DataBase.query(f"SELECT * FROM erp_db.plant WHERE del_flag IS NULL;")
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
    #         if key != 'changed_on':
    #             if value == None:
    #                 condition += (f"{key}=null,")
    #             else:
    #                 condition += (f"{key}='{value}',")
    #         else:
    #             condition += (f"{key}='{value}'")
    #
    #     result = update_data(condition, kwargs['plant_code'])
    #     test_data = select_data()
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20654(**kwargs):
    #     DataBase = dbm
    #     condition = ''
    #
    #     def delete_data(condition):
    #         selected_data = DataBase.query(f"UPDATE `erp_db`.`plant` SET `del_flag`='X' WHERE ({condition});")
    #         return selected_data
    #
    #     def select_data():
    #         selected_data = DataBase.query(f"SELECT * FROM erp_db.plant")
    #         selected_data = [list(i) for i in selected_data]
    #         for i, v in enumerate(selected_data):
    #             for j, w in enumerate(v):
    #                 if type(w) is datetime.datetime:
    #                     selected_data[i][j] = w.strftime("%Y-%m-%d %H:%M:%S")
    #         return selected_data
    #
    #     for key, value in kwargs.items():
    #         if type(kwargs['plant_code']) is str:
    #             condition = f"plant_code='{value}'"
    #         else:
    #             condition = f"plant_code IN {value}"
    #
    #     result = delete_data(condition)
    #     test_data = select_data()
    #     # 실패:0, 성공:1
    #     if result != None:
    #         return {"sign": 1, "data": test_data}
    #     else:
    #         return {"sign": 0, "data": None}
    #
    # @staticmethod
    # @MsgProcessor
    # def f20655(**kwargs):
    #     DataBase = dbm
    #     condition = ''
    #
    #     max_code = int((DataBase.query('select max(plant_code) from erp_db.plant;'))[0][0][1:4]) + 1
    #
    #     # 실패:0, 성공:1
    #     if max_code != None:
    #         return {"sign": 1, "data": max_code}
    #     else:
    #         return {"sign": 0, "data": None}
#############################################################