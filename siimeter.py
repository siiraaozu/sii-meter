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

import json

import os
#os.chdir(os.path.dirname(os.path.abspath(__file__))) #pyで実行時
os.chdir(os.path.dirname(os.path.abspath("__file__"))) #exe化時

#桁と色，寸法の定義
color = ["b", "y", "p", "br", "g", "w"]
x_img = 84
y_img = 128
interval = 7

#数字パネルの座標
def point_img(digit, window_x):
    return [window_x-(164+(x_img+interval)*digit), 20]


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
        self.wrap = int(self.data["wrap"])
    
    #メンバ変数の数字->桁数,画像ファイル
    def load_num(self):
        self.digits = int(math.log10(self.num))+1
        img = []
        num = self.num
        for i in range(self.digits):
            d = num % 10
            img += [str(d) + color[i] + ".png"]
            num = num // 10
        self.img_names = img
        

    # メーターメイン画面作成
    def create_canvas(self):
        if self.digits <= 5:
            window_x = 933
        else:
            window_x = 933 + x_img + interval
        window_y = 153

        #ガベージコレクション対策
        global img, img_siira

        # 画像を表示するための準備
        ## メーター背景の用意
        if self.digits <= 5:
            img = Image.open(r'panel\sii-meter_resized.png')
        else:
            img = Image.open(r'panel\sii-meter_resized6.png')
        img = ImageTk.PhotoImage(img)

        ## しいらイラストの用意
        if self.wrap == 0:
            img_siira = Image.open(r'panel\siira.png')
        elif self.wrap == 1:
            img_siira = Image.open(r'panel\transparent.png')
        elif self.wrap == 2:
            img_siira = Image.open(r'panel\maid.png')
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
        self.canvas.create_image(2, 0, image=img_siira, anchor=tk.NW)

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

        self.config.geometry("420x200")
        self.config.title("設定")

        #お仕事回数
        ##文字
        font2 = font.Font(family='Meiryo', size=14)
        font3 = font.Font(family='Meiryo', size=11)
        label = tk.Label(self.config, text="お仕事回数:", font=font2)
        label.place(x=10, y=10)

        ##ボックス
        ##num_tmp:config内で動く
        num_tmp = self.num
        self.entry = tk.Entry(self.config, font=font2)
        self.entry.place(x=120, y=10, width=100)
        self.entry.insert(tk.END, num_tmp)

        #ボタン
        self.btn_p1 = tk.Button(self.config, font=font2 ,text='+1') 
        self.btn_p1.place(x=240, y=10, width=80, height=40)
        self.btn_p1.configure(command = lambda: self.add_num(1)) 
        #ボタン
        self.btn_p10 = tk.Button(self.config, font=font2 ,text='+10') 
        self.btn_p10.place(x=330, y=10, width=80, height=40) 
        self.btn_p10.configure(command = lambda: self.add_num(10))

        #ボタン
        self.btn_m1 = tk.Button(self.config, font=font2 ,text='-1') 
        self.btn_m1.place(x=240, y=50, width=80, height=40)
        self.btn_m1.configure(command = lambda: self.add_num(-1))

        #ボタン
        self.btn_m10 = tk.Button(self.config, font=font2 ,text='-10') 
        self.btn_m10.place(x=330, y=50, width=80, height=40) 
        self.btn_m10.configure(command = lambda: self.add_num(-10))


        #文字
        label = tk.Label(self.config, text="ラッピング:", font=font2)
        label.place(x=10, y=50)


        #ラッピング変更
        self.wraplist = ["デフォルト" , "バレンタイン", "メイド"]

        self.cb = ttk.Combobox(self.config, values=self.wraplist, state='readonly', width=10, font=font3)
        self.cb.place(x=50, y=200) 
        self.cb.grid(column=0, row=0, padx=120, pady=55)
        self.cb.current(self.wrap)

        #更新ボタン
        self.btn_reload = tk.Button(self.config, font=font2 ,text='更新') 
        self.btn_reload.place(x=150, y=150, width=80, height=40) 
        self.btn_reload.configure(command = self.reload) 

        
        self.chk = tk.Checkbutton(self.config, variable=self.bln, font=font3, text='ショートカットキー(Shift + Alt + ↑↓)\nを使ってメーター画面上で回数を操作する')
        self.chk.place(x=20, y=90)
    
    def reload(self):
        try:
            flag_canvas = 0 #画面を更新するか？

            #ラッピング準備
            wrap_p = self.wrap
            self.wrap = self.wraplist.index(self.cb.get())
            #ラッピングの変更
            if self.wrap != wrap_p:
                flag_canvas = 1

            #推しごと回数
            num_tmp = int(self.entry.get())
            self.num = num_tmp
            digits_p = self.digits
            self.load_num()
            #お仕事回数更新時print
            print(self.num)
            #桁数の変更チェック
            if self.digits != digits_p:
                flag_canvas = 1

            #リロード
            #flag_canvasならば背景も変える
            if num_tmp > 0:   
                self.config.destroy()
                if flag_canvas == 1:
                    self.create_canvas()
                self.create_panel()
            else:
                messagebox.showerror('エラー', '1以上を入力してください',parent=self.config)
        except ValueError:
            messagebox.showerror('エラー', '正の整数を入力してください！',parent=self.config)
        except IndexError:
            messagebox.showerror('エラー', '7桁以上は対応しておりません…',parent=self.config)
    
    #お仕事回数(entrybox)を操作
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

    def closing(self):
        self.data["shortcut"] = self.bln.get()
        self.data["wrap"] = self.wrap
        if messagebox.askyesno("Quit", "本日のお仕事回数をdata_oshigoto.txtに保存しますか？"):
            self.data["oshigoto"] = self.num

            with open('data_oshigoto.txt',mode='r',encoding='utf-8') as f:
                l = f.readlines()
                print(l)
            
            if l:
                latest_num = l[-1].split()
                if latest_num[0] == str(date.today()):
                    l[-1] = str(date.today()) + " " + str(self.num) + "\n"
                else:
                    l += [str(date.today()) + " " + str(self.num) + "\n"]

            else: #ファイルが空
                l += [str(date.today()) + " " + str(self.num) + "\n"]

            print(l)
            with open('data_oshigoto.txt',mode='w',encoding='utf-8') as f:
                f.write("".join(l))

        with open('data.json',mode='w',encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        #破壊
        self.master.destroy()


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

    sii_meter.master.protocol("WM_DELETE_WINDOW", sii_meter.closing)

    sii_meter.mainloop()



if __name__ == "__main__":
    main()







