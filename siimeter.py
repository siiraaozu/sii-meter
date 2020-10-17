#coding:utf-8

#GUI
import tkinter as tk
#コンボボックスで使用
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox

from PIL import Image, ImageTk

import math
import datetime
from datetime import date
import time

import json

import os
#os.chdir(os.path.dirname(os.path.abspath(__file__))) #pyで実行時
os.chdir(os.path.dirname(os.path.abspath("__file__"))) #exe化時

#桁と色，寸法の定義
color = ["b", "y", "p", "br", "g", "w"]
x_img = 122
y_img = 186
interval = 11

#数字パネルの座標
#↓一桁目の数字の座標(x1rは右端から)
x1r = 242
y1 = 31
def point_img(digit, window_x):
    return [(window_x-x1r)-(x_img+interval)*(digit), y1]


#シイメーターオブジェクト
class Meter(tk.Frame):
    def __init__(self, master):
        #masterGUIオブジェクトを使いまわす
        super().__init__(master)

        self.pack()
        self.master.title("SII-METER ver3.0")

        self.import_data()
        self.load_num()
        self.create_canvas()
        self.create_panel()

    #データをdata.jsonから読み込みメンバ変数に代入
    def import_data(self):
        with open('data.json',mode='r',encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.num = int(self.data["oshigoto"])
        self.bln = tk.BooleanVar()
        self.bln.set(bool(int(self.data["shortcut"])))
        self.bln2 = tk.BooleanVar()
        self.bln2.set(bool(int(self.data["shortcut2"])))
        self.wrap = int(self.data["wrap"])
    
    #メンバ変数の数字->桁数,画像ファイル
    #使用:①開始時　②更新時　③ショートカット回数操作時
    def load_num(self):
        self.digits = int(math.log10(self.num))+1
        img = []
        num = self.num
        for i in range(self.digits):
            d = num % 10
            img += [str(d) + color[i] + ".png"]
            num = num // 10
        self.img_names = img
        #お仕事回数更新時print
        print(self.num)
        

    # メーターメイン画面作成
    def create_canvas(self):
        if self.digits <= 5:
            window_x = 1358
        else:
            window_x = 1358 + x_img + interval
        window_y = 224

        #ガベージコレクション対策
        global img, img_siira

        # 画像を表示するための準備
        ## メーター背景の用意
        if self.digits <= 5:
            img = Image.open(r'panel\sii-meter3.1.png')
        else:
            img = Image.open(r'panel\sii-meter3.1_6.png')
        img = ImageTk.PhotoImage(img)

        ## しいらイラストの用意(170*224)
        if self.wrap == 0:
            img_siira = Image.open(r'panel\defalt3.1.png')
        elif self.wrap == 1:
            img_siira = Image.open(r'panel\transparent.png')
        elif self.wrap == 2:
            img_siira = Image.open(r'panel\maid3.1.png')
        img_siira = ImageTk.PhotoImage(img_siira)

        # ウィンドウサイズ変更の許可　(x,y)・・・0：禁止　1：許可
        self.master.resizable(1,1)
        self.master.geometry(str(window_x+4)+"x"+str(window_y+4))
        self.master.resizable(0,0)

        # 画像を張る
        ## 画像を表示するためのキャンバスの作成（黒で表示）
        self.canvas = tk.Canvas(self.master,bg = "black", width=window_x, height=window_y)
        self.canvas.place(x=0, y=0) # 左上の座標を指定
        ## キャンバスに画像を表示する。第一引数と第二引数は、x, yの座標
        self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
        self.canvas.create_image(0, 0, image=img_siira, anchor=tk.NW)

        self.window_x = window_x
        
    
    def create_panel(self):
        #ガベージコレクション対策
        global imgs
        imgs = []
        for digit, img_name in enumerate(self.img_names):
            # 画像を表示するための準備
            imgs += [Image.open('img_num/' + img_name)]
            imgs[digit] = ImageTk.PhotoImage(imgs[digit])
            # キャンバスに画像を表示する。第一引数と第二引数は、x, yの座標
            p = point_img(digit, self.window_x)
            self.canvas.create_image(p[0], p[1], image=imgs[digit], anchor=tk.NW)

    def create_config(self,event):
        self.config = tk.Toplevel(self)
        self.config.focus_set()
        self.config.grab_set()

        self.config.geometry("540x260")
        self.config.title("設定")

        #お仕事回数
        ##文字
        font2 = font.Font(family='Meiryo', size=13)
        font3 = font.Font(family='Meiryo', size=10)
        font4 = font.Font(family='Meiryo', size=9)
        label = tk.Label(self.config, text="お仕事回数:", font=font2)
        label.place(x=10, y=10)

        ##entryボックス
        ##num_tmp:config内で動く
        num_tmp = self.num
        self.entry = tk.Entry(self.config, font=font2)
        self.entry.place(x=170, y=8, width=130)
        self.entry.insert(tk.END, num_tmp)

        #ボタン
        self.btn_p1 = tk.Button(self.config, font=font2 ,text='+1') 
        self.btn_p1.place(x=340, y=10, width=80, height=40)
        self.btn_p1.configure(command = lambda: self.add_num(1)) 
        #ボタン
        self.btn_p10 = tk.Button(self.config, font=font2 ,text='+10') 
        self.btn_p10.place(x=420, y=10, width=80, height=40) 
        self.btn_p10.configure(command = lambda: self.add_num(10))

        #ボタン
        self.btn_m1 = tk.Button(self.config, font=font2 ,text='-1') 
        self.btn_m1.place(x=340, y=50, width=80, height=40)
        self.btn_m1.configure(command = lambda: self.add_num(-1))

        #ボタン
        self.btn_m10 = tk.Button(self.config, font=font2 ,text='-10') 
        self.btn_m10.place(x=420, y=50, width=80, height=40) 
        self.btn_m10.configure(command = lambda: self.add_num(-10))


        #文字
        label = tk.Label(self.config, text="ラッピング:", font=font2)
        label.place(x=10, y=50)


        #ラッピング変更
        self.wraplist = ["デフォルト" , "バレンタイン", "メイド"]

        self.cb = ttk.Combobox(self.config, values=self.wraplist, state='readonly', width=10, font=font3)
        #self.cb.place(x=200, y=200) 
        self.cb.grid(column=0, row=0, padx=170, pady=56)
        self.cb.current(self.wrap)
      
        self.chk = tk.Checkbutton(self.config, variable=self.bln, font=font4, text='ショートカットキー(Shift + Alt + ↑↓)\nを使ってメーター画面上で回数を操作する')
        self.chk.place(x=20, y=100)

        self.chk2 = tk.Checkbutton(self.config, variable=self.bln2, font=font4, text='ショートカットキー(Ctrl + S)でお仕事回数を保存する')
        self.chk2.place(x=20, y=160)

        #更新ボタン
        self.btn_reload = tk.Button(self.config, font=font2 ,text='更新') 
        self.btn_reload.place(x=150, y=210, width=160, height=40) 
        self.btn_reload.configure(command = self.reload) 
    
    def reload(self):
        try:
            flag_canvas = 0 #画面を更新するか？

            #ラッピング準備
            wrap_p = self.wrap
            self.wrap = self.wraplist.index(self.cb.get())

            #推しごと回数
            num_tmp = int(self.entry.get())
            self.num = num_tmp
            digits_p = self.digits
            self.load_num()

            #リロード
            #flag_canvasならば背景も変える
            if num_tmp > 0:   
                self.config.destroy()
                #桁数orラッピングの変更チェック
                if self.digits != digits_p or self.wrap != wrap_p:
                    self.create_canvas()
                self.create_panel()
            else:
                messagebox.showerror('エラー', '1以上を入力してください',parent=self.config)
        except ValueError:
            messagebox.showerror('エラー', '正の整数を入力してください！',parent=self.config)
        except IndexError:
            messagebox.showerror('エラー', '7桁以上は対応しておりません…',parent=self.config)
    
    #ボタンによるお仕事回数(entrybox)を操作
    def add_num(self, add):
        try:
            num_tmp = int(self.entry.get()) + add

            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END ,num_tmp)
        except ValueError:
            messagebox.showerror('エラー', '正の整数を入力してください！',parent=self.config)

    #ショートカットによるお仕事回数操作
    def add_num_main(self,num):
        if self.bln.get():
            digits_p = self.digits
            self.num += num
            self.load_num()
            if self.digits != digits_p:
                self.create_canvas()
            self.create_panel()


    #はじめは空欄
    #保存時には一つ改行されている
    #ex
    #--------------
    #2020-08-15 13375改行
    #2020-08-16 13376改行
    #
    #--------------
    #この場合、'2020-08-15 13375\n', '2020-08-16 13376\n'となる(最終行は空、ではない)


    def closing2(self):
        self.close = tk.Toplevel(self)
        self.close.focus_set()
        self.close.grab_set()

        self.close.geometry("540x180")
        self.close.title("Quit")

        self.canvas = tk.Canvas(self.close,bg = "white", width=540, height=100)
        self.canvas.place(x=0, y=0)

        font3 = font.Font(family='Meiryo', size=9)
        label = tk.Label(self.close, text="本日のお仕事回数をdata_oshigoto.txtに保存しますか？", font=font3 ,bg = "white")
        label.place(x=20, y=50)
        
        self.btn_yes = tk.Button(self.close, font=font3 ,text='保存') 
        self.btn_yes.place(x=140, y=120, width=120, height=36)
        self.btn_yes.configure(command = lambda: self.close_save(True)) 

        self.btn_no = tk.Button(self.close, font=font3 ,text='保存しない') 
        self.btn_no.place(x=270, y=120, width=120, height=36)
        self.btn_no.configure(command = lambda: self.close_save(False)) 

        self.btn_cancel = tk.Button(self.close, font=font3 ,text='キャンセル') 
        self.btn_cancel.place(x=400, y=120, width=120, height=36)
        self.btn_cancel.configure(command = self.close_cancel) 

    def save_txt(self):
        with open('data_oshigoto.txt',mode='r',encoding='utf-8') as f:
            l = f.readlines()
        
        if l:
            latest_num = l[-1].split()
            if latest_num[0] == str(date.today()):
                print("update today's number")
                l[-1] = str(date.today()) + " " + str(self.num) + "\n"
            else:
                print("add today's number")
                l += [str(date.today()) + " " + str(self.num) + "\n"]

        else: #ファイルが空
            print("add today's number(create)")
            l += [str(date.today()) + " " + str(self.num) + "\n"]

        print(l)
        with open('data_oshigoto.txt',mode='w',encoding='utf-8') as f:
            f.write("".join(l))

    def close_save(self,save):
        if save:
            self.save_txt()
            
            self.data["oshigoto"] = self.num
        
        self.data["shortcut"] = self.bln.get()
        self.data["shortcut2"] = self.bln2.get()
        self.data["wrap"] = self.wrap

        with open('data.json',mode='w',encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        #破壊
        print("See you!")
        self.master.destroy()
        
    def close_cancel(self):
        self.close.destroy()

    #ctrl+sのセーブ
    #data_shigotoに保存(jsonには保存しない！！)
    def event_save(self, event):
        if self.bln2.get():
            self.save_txt()


# 回数の読み込み
# digits=len(names)桁数
# digitは何のくらいか


def main():
    root = tk.Tk()
    sii_meter = Meter(master=root)#Inheritクラスの継承！

    #イベント
    #root == siimeter.master
    sii_meter.master.bind(
        "<ButtonPress>", # 受付けるイベント
        sii_meter.create_config # そのイベント時に実行する関数
    )

    sii_meter.master.bind(
        "<Shift-Alt-Up>", # 受付けるイベント
        lambda event: sii_meter.add_num_main(1) # そのイベント時に実行する関数
    )

    sii_meter.master.bind(
        "<Shift-Alt-Down>", # 受付けるイベント
        lambda event: sii_meter.add_num_main(-1) # そのイベント時に実行する関数
    )

    sii_meter.master.bind(
        "<Control-s>", # 受付けるイベント
        sii_meter.event_save # そのイベント時に実行する関数
    )

    sii_meter.master.protocol("WM_DELETE_WINDOW", sii_meter.closing2)

    sii_meter.mainloop()


if __name__ == "__main__":
    main()







