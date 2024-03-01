import time
from tkinter.filedialog import askopenfilenames
import ttkbootstrap as ttk
from threading import Thread
from scapy.all import wrpcap,rdpcap

class Merge_ui:
    def __init__(self,root):
        # self.window = ttk.Window()  # 实例化
        # self.window.call('tk', 'scaling', 1.333)  # 设置程序缩放为1.333
        #
        self.window=ttk.Toplevel(
        master=root,
        title='合并pcap',
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        )
        self.window.grab_set()

        self.window.title('合并pcap')
        self.files=[]
        self.result=''
        self.layout_1()

    def start_merge(self,file_list):
        li = []
        self.l4.insert('end', '正在处理..' + '\n')
        for i in file_list:
            a = rdpcap(i)
            li.extend(a)
        name=f'{time.time()}.pcap'
        wrpcap(f"./{name}", li)
        self.l4.insert('end', '完成！' + '\n')
        self.l4.insert('end', f'合并文件保存至当前目录下{name}' + '\n')

    def select_file(self):
        self.l4.delete('1.0','end')
        self.l4.insert('end','请一次选择多个pcap或者pcapng文件'+'\n')
        self.filepath = askopenfilenames(title= "Select pcap file", filetypes= [("pcap files", "*.pcap"),("pcap files", "*.pcapng")])
        self.l4.insert('end',f'将合并以下{len(self.filepath)}个文件：'+'\n')
        for i in self.filepath:
            self.l4.insert('end',i+'\n')
        self.l3.configure(state='')

    def to_2(self):
        self.l3.configure(state='disable')
        Thread(target=self.start_merge,args=(self.filepath,)).start()


    def layout_1(self):
        self.frame1=ttk.Frame(self.window)
        self.frame1.pack(pady=5)

        self.l1=ttk.Button(self.frame1,text='选择多文件', bootstyle="info",command=self.select_file)
        self.l1.pack(side='left',pady=5)
        self.l3=ttk.Button(self.frame1,text='确定', state='disable',bootstyle="info",command=self.to_2)
        self.l3.pack(side='left',padx=10,pady=5)


        self.l4=ttk.ScrolledText(self.window,width=40,height=10)
        self.l4.insert('end','请一次选择多个pcap或者pcapng文件'+'\n')
        self.l4.pack()
        self.window.mainloop()


if __name__ == '__main__':
    aa=Merge_ui(1)