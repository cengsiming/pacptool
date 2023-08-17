import time
from tkinter.filedialog import askopenfilename
import ttkbootstrap as ttk
from compare_pcap import start_run,wirte_result2
from threading import Thread


class Compare_ui:
    def __init__(self,root):
        # self.window = ttk.Window()  # 实例化
        # self.window.call('tk', 'scaling', 1.333)  # 设置程序缩放为1.333
        #
        self.window=ttk.Toplevel(
        master=root,
        title='对比pcap',
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        )
        self.window.grab_set()

        self.window.title('对比pcap')
        self.files=[]
        self.result=''
        self.layout_1()


    def select_file(self,l):
        self.filepath = askopenfilename(title= "Select pcap file", filetypes= (("pcap files", "*.pcap"),("pcap files", "*.pcapng")))
        l.config(text=self.filepath)
        if '.pcap' in self.l11.cget('text') and '.pcap'  in self.l12.cget('text'):
            self.l3.configure(state='')
        else:
            self.l3.configure(state='disable')

    def to_eqqqq2(self):
        self.files.append(self.l11.cget('text'))
        self.files.append(self.l12.cget('text'))
        try:
            self.l5.start(200)
            self.thr()
        except:
            self.l4.insert('end', '未知错误，请关闭程序释放内存' + '\n')
            self.l5.stop()
            # print('未知错误，请关闭程序释放内存')
        self.l3.configure(state="disable")
        self.l1.config(state="disable")
        self.l2.config(state="disable")

    def wirte_result(self):
        wirte_result2()
        self.l4.insert('end','运行结果已导出至当前目录'+'\n')

    def thr(self):
        p=Thread(target=start_run,args=(*self.files,self.l4,self.l5,self.l6))
        p.start()


    def layout_1(self):
        self.frame1=ttk.Frame(self.window)
        self.frame1.pack(pady=5)
        self.frame2=ttk.Frame(self.window)
        self.frame2.pack(pady=5)
        self.frame3=ttk.Frame(self.window)
        self.frame3.pack(pady=5)
        self.l1=ttk.Button(self.frame1,text='选择文件1', bootstyle="warning",command=lambda :self.select_file(self.l11))
        self.l1.pack(side='left',pady=5)
        self.l11=ttk.Label(self.frame1)
        self.l11.pack(side='left',pady=5)
        self.l2=ttk.Button(self.frame2,text='选择文件2', bootstyle="warning",command=lambda :self.select_file(self.l12))
        self.l2.pack(side='left',pady=5)
        self.l12=ttk.Label(self.frame2)
        self.l12.pack(side='left',pady=5)
        self.l3=ttk.Button(self.frame3,text='确定', state='disable',bootstyle="warning",command=self.to_eqqqq2)
        self.l3.pack(side='left',pady=5)
        self.l6=ttk.Button(self.frame3,text='导出', state='disable',bootstyle="warning",command=self.wirte_result)
        self.l6.pack(side='left',padx=10)
        self.l5 = ttk.Progressbar(self.frame3, bootstyle="warning-striped",mode=ttk.INDETERMINATE)
        self.l5.pack(side='left',padx=10)


        self.l4=ttk.ScrolledText(self.window,width=40,height=10)
        self.l4.insert('end','对比维度包括五元组+应用层协议+payload'+'\n')
        self.l4.insert('end','运行结果将会输出两个pcap文件中不同的包的序号'+'\n')
        self.l4.pack()
        self.window.mainloop()


if __name__ == '__main__':
    aa=Compare_ui()