import time
from tkinter.filedialog import askopenfilename
import ttkbootstrap as ttk
from threading import Thread
from scapy.all import wrpcap,rdpcap

class ChangeTime_ui:
    def __init__(self,root):
        # self.window = ttk.Window()  # 实例化
        # self.window.call('tk', 'scaling', 1.333)  # 设置程序缩放为1.333
        #
        self.window = root
        # self.window=ttk.Toplevel(
        # master=root,
        # title='修改时间戳',
        # resizable=None,         #设置窗口是否可以更改大小
        # alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        # )
        # self.window.grab_set()
        # self.ddd = [0,0]
        # self.window.title('修改时间戳')
        self.check_time=self.window.register(self.check_time2)#注册验证函数

        # self.run()

    def check_time2(self,x):
        try:
            float(x)
            self.ddd[0]=1
            self.interval = x
            if self.ddd[0]==1 and self.ddd[1]==1:
                self.l3.configure(state="")
            return True
        except:
            self.ddd[0]=0
            self.interval = None
            self.l3.configure(state="disable")
            return False

    def start_merge(self,fileName,interval):
        self.l4.insert('end', '读取文件..' + '\n')
        pkts = rdpcap(fileName)
        cooked=[]
        timestamp = time.time()
        self.l4.insert('end', '正在处理..' + '\n')
        for p in pkts:
            p.time = timestamp
            timestamp += float(interval)
            pmod=p
            cooked.append(pmod)
        name=f'{time.time()}.pcap'
        wrpcap(f"./{name}", cooked)
        self.l4.insert('end', '完成！' + '\n')
        self.l4.insert('end', f'文件保存至当前目录下{name}' + '\n')

    def select_file(self):
        self.l4.delete('1.0','end')
        self.l4.insert('end','请选择pcap或者pcapng文件'+'\n')
        self.filepath = askopenfilename(title= "Select pcap file", filetypes= (("pcap files", "*.pcap"),("pcap files", "*.pcapng")))
        self.ddd[1]=1
        self.l4.insert('end',self.filepath+'\n')
        if self.ddd[0]==1 and self.ddd[1]==1:
            self.l3.configure(state="")

    def to_2(self):
        self.l3.configure(state='disable')
        Thread(target=self.start_merge,args=(self.filepath,self.interval,)).start()


    def run(self):
        self.frame1=ttk.Frame(self.window)
        self.frame1.pack(pady=5)

        self.l1=ttk.Button(self.frame1,text='选择文件', bootstyle="secondary",command=self.select_file)
        self.l1.pack(side='left',pady=5)
        ttk.Label(self.frame1,text='时间间隔/s:').pack(side=ttk.LEFT)
        self.l4=ttk.Entry(self.frame1,width=5,validate="focus", validatecommand=(self.check_time, '%P'))
        self.l4.insert('0','0.1')
        self.l4.pack(side=ttk.LEFT, padx=10)
        self.l3=ttk.Button(self.frame1,text='确定', state='disable',bootstyle="secondary",command=self.to_2)
        self.l3.pack(side='left',padx=10,pady=5)


        self.l4=ttk.ScrolledText(self.window,width=40,height=50)
        self.l4.pack(fill='both')
        self.window.mainloop()


if __name__ == '__main__':
    aa=ChangeTime_ui(1)