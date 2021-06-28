#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by RD/EE:Wiki Wang
first release version:Ver:2020/02/29
"""
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
import os
import subprocess
import tempfile
import threading


class Debug_tool():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('A09 project Test script -Ver:20200229')
        self.root.geometry()  # '800x500'
        self.GUI()

    def GUI(self):
        # create fram1
        fram1 = tk.Frame(self.root)
        fram1.pack(side='left', fill='both', expand='yes')  # 实例化1个Frame
        ft = tkFont.Font(weight=tkFont.BOLD)  # set the bold font
        # set the bold font and underline
        ft1 = tkFont.Font(weight=tkFont.BOLD, underline=1)

        # create fram2
        fram2 = tk.Frame(self.root)
        fram2.pack(side='left', padx=10, expand='yes')
        fram2.pack(side='left', padx=10, fill='both', expand='yes')

        # add text
        self.text1 = tk.Text(fram2, width=80, height=25, bg='SpringGreen', relief='groove', bd=3)  # text bd setting, must set relief firstly
        # 设置 tag for self.text1, 配合tex1.insert('end',string,
        # 'tag_xx')使用设置插入字符的显示，字体，颜色，背景颜色等
        self.text1.tag_config("tag_item", font=ft)
        self.text1.tag_config("tag_data", foreground="blue")
        self.text1.tag_config("tag_wled", foreground="white", font=ft)
        self.text1.tag_config("tag_rled", foreground="red", font=ft)
        self.text1.tag_config("tag_dis", foreground="purple", font=ft)
        self.text1.pack(side='top', pady=20, fill='both', expand='yes')
        label1 = tk.Label(
            fram2,
            text='Manual test command input in below area: ',
            width=20,
            font=ft1)
        label1.pack(side='top', fill='x', expand='yes')

        self.ManualCmd = tk.Entry(
            fram2,
            width=45,
            foreground='black',
            bd=3,
            bg='DeepSkyBlue')
        self.ManualCmd.pack(side='top', pady=5, fill='both', expand='yes')

        # add fram3
        fram3 = tk.Frame(self.root)
        fram3.pack(side='left', padx=10, expand='yes')
        fram3.pack(side='left', padx=10, fill='both', expand='yes')

        label2 = tk.Label(
            fram3,
            text='Basic information: ',
            width=10,
            font=ft1)
        label2.pack(side='top', fill='x')  # ,expand='yes'

        self.text2 = tk.Text(fram3, width=30, height=20, bg='Wheat', relief='sunken', bd=3)
        self.text2.pack(side='top', pady=3, fill='both', expand='yes')

        # 设置 tag for self.text2
        self.text2.tag_config("tag_item", font=ft)
        self.text2.tag_config("tag_data", foreground="blue")
        self.text2.tag_config("tag_err", backgroun="yellow", foreground="red", font=ft)
        # Add buttons to fram1
        button1 = tk.Button(
            fram1,
            width=10,
            text='Battery',
            fg='blue', command=lambda: self.thread_it(self.Batt)).pack(
            side='top',
            pady=3,
            padx=5,
            fill='y',
            expand='yes')  # 生成button1
        button2 = tk.Button(
            fram1,
            width=10,
            text='Lsensor',
            fg='blue',
            command=lambda: self.thread_it(self.Lsensor)).pack(
            side='top',
            pady=3,
            padx=5,
            fill='y',
            expand='yes')
        button3 = tk.Button(
            fram1,
            width=10,
            text='SensorSelf',
            fg='blue',
            command=lambda: self.thread_it(self.SensorSelfTest)).pack(
            side='top',
            pady=3,
            padx=5,
            fill='y',
            expand='yes')
        button5 = tk.Button(
            fram1,
            width=10,
            text='MIC',
            fg='blue',
            command=lambda: self.thread_it(self.MIC)).pack(
            side='top',
            pady=3,
            padx=5,
            fill='y',
            expand='yes')
        button6 = tk.Button(
            fram1,
            width=10,
            text='Speaker',
            fg='blue',
            command=lambda: self.thread_it(self.Speaker)).pack(
            side='top',
            pady=3,
            padx=5,
            fill='y',
            expand='yes')

        # button4 = tk.Button(
        #     fram1,
        #     width=12,
        #     text='ScreenCapture',
        #     fg='blue',
        #     command=lambda: self.thread_it(self.ScreenCapture)).pack(
        #     side='top',
        #     pady=3,
        #     padx=5,
        #     fill='y',
        #     expand='yes')

        button8 = tk.Button(
            fram2,
            width=10,
            text='SendCommand',
            fg='blue',
            command=lambda: self.thread_it(self.ManulCmd)).pack(
            side='right',
            padx=5,
            pady=5,
            fill='both',
            expand='yes')
        button9 = tk.Button(
            fram1,
            width=10,
            text='Clear',
            fg='red',
            font=ft1,
            command=lambda: self.thread_it(self.Clear)).pack(
            side='bottom',
            pady=30,
            padx=5,
            fill='y',
            expand='yes')
        button10 = tk.Button(
            fram3,
            width=10,
            text='Connect Device',
            fg='black',
            font=ft,
            command=lambda: self.thread_it(self.Recon)).pack(
            side='top',
            pady=5,
            padx=5,
            fill='both',
            expand='yes')
        self.root.mainloop()

    def OutputMore(self, command):              # 当输出的内容过多时，用此函数,PIPE本身可容纳的量比较小，所以程序会卡死
        out_temp = tempfile.SpooledTemporaryFile(buffering=10 * 1000)   # 方法是不用subprocess提供的PIPE，而是使用自己创建的流。如此，可以控制流的大小。
        fileno = out_temp.fileno()
        obj = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=True)
        obj.wait()
        out_temp.seek(0)   # 从0位置开始读取零时文件
        lines = out_temp.readlines()
        output = ''
        for line in lines:
            output += line.decode('utf-8')
        return output

    def Batt(self):
        try:
            self.text1.delete(1.0, "end")
            self.text1.update()
            self.text1.insert(
                'end', 'Battery Status:', 'tag_item')
            self.text1.update()
            command = ['adb shell "echo 0 > /sys/class/power_supply/battery/input_suspend"',
                       'adb shell cat /sys/class/power_supply/battery/current_now',
                       'adb shell cat /sys/class/power_supply/battery/charge_type',
                       'adb shell cat /sys/class/power_supply/battery/status',
                       'adb shell "echo 1 > /sys/class/power_supply/battery/input_suspend"',
                       'adb shell cat /sys/class/power_supply/battery/voltage_now',
                       'adb shell cat /sys/class/power_supply/battery/capacity',
                       'adb shell cat /sys/class/power_supply/battery/temp'
                       ]
            description = ['', 'Current_now\n', 'Charge_type\n', 'Status\n', '', 'Voltage_now\n', 'Capacity\n', 'Temp\n']
            for i in range(len(command)):
                b = os.popen(command[i])
                result4 = b.read()
                b.close()
                self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行
                self.text1.update()
                self.text1.insert('end', description[i], 'tag_dis')
                self.text1.update()
                self.text1.insert('end', result4, 'tag_data')
                self.text1.update()
        except Exception as e:
            tkinter.messagebox.showwarning(
                '警告', "Smart Watch can't be connected! Please check your connection!")

    def Speaker(self):
        try:
            self.text1.delete(1.0, "end")
            self.text1.update()
            command = ['adb shell "tinymix \'PRI_TDM_RX_1 Audio Mixer MultiMedia1\' 1"',
                       'adb shell tinyplay /data/pa_audio_test.wav'
                       ]
            self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行
            self.text1.insert('end', 'Start Speaker Test......\n', 'tag_dis')
            self.text1.update()
            os.system(command[0])
            b = os.popen(command[1])
            result4 = b.read()
            b.close()
            self.text1.insert('end', result4, 'tag_data')
            self.text1.insert('end', '\n\n')  # END索引号表示在最后插入, '\n'换行
            self.text1.update()

        except BaseException:
            tkinter.messagebox.showwarning(
                '警告', "W2 can't be connected! Please check your connection!")

    def MIC(self):
        try:
            self.text1.delete(1.0, "end")
            self.text1.update()
            self.text1.insert(
                'end', 'Start MIC Test.....\n', 'tag_dis')
            self.text1.insert(
                'end', 'Start Record, please play music from outside. It needs 6 seconds.\n', 'tag_data')
            self.text1.update()
            command2 = ['adb shell "tinymix \'MultiMedia1 Mixer PRI_TDM_TX_3\' 1"',
                        'adb shell "tinycap /data/test.wav -c 1 -r 48000 -T 6"',
                        'adb shell "tinymix \'PRI_TDM_RX_1 Audio Mixer MultiMedia1\' 1"',
                        'adb shell "tinyplay /data/test.wav"'
                        ]
            description2 = ['Start Record:\n', '', 'Start play the Recorded sound:\n', 'MIC Test accomplished!\n']
            for i in range(len(command2)):
                b = os.popen(command2[i])
                result4 = b.read()
                b.close()
                self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行
                self.text1.insert('end', description2[i], 'tag_dis')
                self.text1.insert('end', result4, 'tag_data')
                self.text1.update()
        except BaseException:
            tkinter.messagebox.showwarning(
                '警告', "W2 can't be connected! Please check your connection!")

    def Lsensor(self):
        try:
            self.text1.delete(1.0, "end")
            self.text1.update()
            self.text1.insert(
                'end', 'Start L-sensor Test:\n', 'tag_item')
            command = ['adb shell "sh /system/Factory/script/setBrightness.sh 0"',
                       'adb shell "sns_client_example_cpp ambient_light 20 1"',
                       'adb shell "sh /system/Factory/script/setBrightness.sh 102"',
                       ]
            self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行
            self.text1.insert('end', 'Close LCD back-light\n', 'tag_dis')
            self.text1.update()
            os.system(command[0])
            self.text1.insert('end', 'Open a light source besides the LCD\n', 'tag_dis')
            self.text1.update()
            output = self.OutputMore(command[1])
            self.text1.insert('end', '\n' + output + '\n', 'tag_data')
            # for line in lines:
            #     self.text1.insert('end', '\n' + line.decode('utf-8') + '\n', 'tag_data')
            #     self.text1.update()
            os.system(command[2])
            self.text1.insert('end', 'Test finished! Open LCD back-light\n', 'tag_dis')
            self.text1.update()
        except BaseException:
            tkinter.messagebox.showwarning(
                '警告', "Smart Watch can't be connected! Please check your connection!")

    def SensorSelfTest(self):
        # try:
        command = ['adb shell "see_selftest -sensor=accel -testtype=3"',
                   'adb shell "see_workhorse -ping=1 -sensor=accel"',
                   'adb shell "see_selftest -sensor=gyro -testtype=3"',
                   'adb shell "see_workhorse -ping=1 -sensor=gyro"',
                   'adb shell "see_selftest -sensor=mag -testtype=3"',
                   'adb shell "see_workhorse -ping=1 -sensor=mag"',
                   'adb shell "see_selftest -sensor=pressure -testtype=3"',
                   'adb shell "see_workhorse -ping=1 -sensor=pressure"',
                   ]
        test_item = ['G sensor', 'Gryo sensor', 'E-compass sensor', 'Pressure sensor']

        self.Text_SensorSelf()  # text界面清空
        # 注意：tag所在的那一行要没有\n，如果有\n就代表tag所标记的是下面一行，所以下面的文本不带\n
        self.text1.insert('end', 'G sensor : [self_test] or [Ping_Test]')  # G sensor
        self.Tag_SensorSelf(test_item[0], command[0], "link1", "insert linestart+11c", "insert linestart+22c")  # self_test
        self.Tag_SensorSelf(test_item[0], command[1], "link2", "insert linestart+26c", "insert linestart+37c")  # Ping_Test
        self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行，代表tag所标记的为下面这个将要插入的文本

        self.text1.insert('end', 'Gryo sensor : [self_test] or [Ping_Test]') # Gryo sensor
        self.Tag_SensorSelf(test_item[1], command[2], "link3", "insert linestart+14c", "insert linestart+24c")  # self_test
        self.Tag_SensorSelf(test_item[1], command[3], "link4", "insert linestart+29c", "insert linestart+40c")  # ping_test
        self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行，代表tag所标记的为下面这个将要插入的文本

        self.text1.insert('end', 'E-compass sensor : [self_test] or [Ping_Test]')  # E-compass sensor
        self.Tag_SensorSelf(test_item[2], command[4], "link5", "insert linestart+19c", "insert linestart+30c")  # self_test
        self.Tag_SensorSelf(test_item[2], command[5], "link6", "insert linestart+35c", "insert linestart+45c")  # ping_test
        self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行，代表tag所标记的为下面这个将要插入的文本

        self.text1.insert('end', 'Pressure sensor : [self_test] or [Ping_Test]')  # Pressure sensor
        self.Tag_SensorSelf(test_item[3], command[6], "link7", "insert linestart+18c", "insert linestart+30c")  # self_test
        self.Tag_SensorSelf(test_item[3], command[7], "link8", "insert linestart+33c", "insert linestart+45c")  # ping_test
        self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行，代表tag所标记的为下面这个将要插入的文本

    # 配置text里的文本显示, 各个测试item显示，供SensorSelfTest调用
    def Text_SensorSelf(self):
        self.text1.delete(1.0, "end")
        self.text1.update()
        self.text1.insert(
            'end',
            'Please click the related link base on your test item: \n',
            'tag_item')
        self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行
        self.text1.update()
        self.text1.see(tk.END)
        # self.text1.insert('end', 'G sensor : [self_test] or [Ping_Test]')  # 这里的空格为了下一个插入的能显示在text控件下一行
        # self.text1.insert('end', 'Gryo sensor : [self_test] or [Ping_Test]')  # 空格为了占满text控件一行
        # self.text1.insert('end', 'E-compass sensor : [self_test] or [Ping_Test]                                   ')
        # self.text1.insert('end', 'Pressure sensor : [self_test] or [Ping_Test]')  # Pressure-sensor

    # 配置text控件里的tag标签，并设置鼠标click事件，供SensorSelfTest调用
    def Tag_SensorSelf(self, test_item, command, link, line_start, line_end):
        # insert linestart means the start index of current line, 11c means add 11 columns
        self.text1.tag_add(link, line_start, line_end)
        self.text1.tag_config(link, foreground="blue", underline=True)

        def show_arrow_cursor(event):
            self.text1.config(cursor="arrow")

        def show_xterm_cursor(event):
            self.text1.config(cursor="xterm")

        def click(event):
            self.text1.insert('end', '\n' + test_item + ' test is on going, please wait 5 seconds... \n', 'tag_data')
            self.text1.update()
            output = self.OutputMore(command)
            tkinter.messagebox.showinfo('测试完成！', output)

        self.text1.tag_bind(link, "<Enter>", show_arrow_cursor)
        self.text1.tag_bind(link, "<Leave>", show_xterm_cursor)
        self.text1.tag_bind(link, "<Button-1>", click)
        self.text1.update()  # display the information timely
        self.text1.see(tk.END)

    # def ScreenCapture(self):
    #     # try:
    #     self.text1.delete(1.0, "end")
    #     self.text1.update()
    #     self.text1.insert(
    #         'end', 'Start ScreenCapture, maybe need 5 seconds...\n', 'tag_dis')
    #     self.text1.update()
    #     # command = ['adb shell /system/bin/screencap -p /sdcard/screenshot.png',
    #     #            'adb pull /sdcard/screenshot.png screenshot.png',
    #     #            ]
    #     # os.system(command[0])
    #     # os.system(command[1])
    #     # time.sleep(5)
    #     my_photo = tk.PhotoImage(file="./screenshot.png")
    #     self.text1.image_create('end', image=my_photo)
    #     self.text1.pack()
    #     print('success')
    #
    #     # except BaseException:
    #     #     tkinter.messagebox.showwarning(
    #     #         '警告', "W2 can't be connected! Please check your connection!")

    def ManulCmd(self):
        try:
            var = self.ManualCmd.get()  # 从entry获得变量值
            b = os.popen(var)
            result = b.read()
            b.close()
            self.text1.insert('end', '\n')  # END索引号表示在最后插入, '\n'换行
            self.text1.insert('end', result)
            self.text1.update()
            self.text1.see(tk.END)
        except BaseException:
            tkinter.messagebox.showwarning(
                '警告', "Smart Watch can't be connected! Please check your connection!")

    def Clear(self):
        self.text1.delete(1.0, "end")
        self.text1.update()  # display the information timely

    def Recon(self):
        # Clear self.text2 before reconnect the system
        self.text2.delete(1.0, "end")
        self.text2.update()      # display the information timely
        self.FirstLoad()

    def FirstLoad(self):
        # Basic information
        try:
            command = ['adb shell cat /persist/sku',  'adb shell cat /persist/sn', 'adb shell getprop  ro.build.version.software' ]
            b = os.popen(command[0])
            sku = b.read()
            b = os.popen(command[1])
            sn = b.read()
            b = os.popen(command[2])
            ver = b.read()
            b.close()
            self.text2.insert('end', 'SKU :  \n', 'tag_item')  # '\n'表示换行, item bold
            self.text2.insert('end', sku + '\n', 'tag_data')
            self.text2.insert('end', 'SN :  \n', 'tag_item')  # '\n'表示换行, item bold
            self.text2.insert('end', sn + '\n\n', 'tag_data')
            self.text2.insert('end', 'SW version :  \n', 'tag_item')  # '\n'表示换行, item bold
            self.text2.insert('end', ver + '\n', 'tag_data')
            self.text1.update()
        except:
            # print ("[ ST port can't be connected! ]")
            self.text2.insert('end', 'Smart Watch can not be connected!\n', 'tag_err')  # '\n'表示换行
            self.text2.insert('end', 'Check the adb.exe if in the running script folder\n', 'tag_err')

    def thread_it(self, func):  # 多線程函數，供GUI裡的command調用。
        '''将函数打包进线程'''
        # 创建
        t = threading.Thread(target=func)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()


if __name__ == '__main__':
    Debug_tool()
    # obj = Debug_tool()
    # t1 = threading.Thread(target=obj.GUI())
    # t1.start()
    # t2 = threading.Thread(target=obj.FirstLoad())
    # t2.start()
    # t3 = threading.Thread(target=obj.Batt())
    # t3.start()
