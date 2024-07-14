from tkinter.filedialog import askopenfilename
import ttkbootstrap as ttk
from threading import Thread
from splitFlow import SplitFlow

class Split_ui:
    def __init__(self,root):
        # self.window = ttk.Window()  # 实例化
        # self.window.call('tk', 'scaling', 1.333)  # 设置程序缩放为1.333
        #
        self.window=ttk.Toplevel(
        master=root,
        title='拆分pcap为多条流',
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        )
        self.window.grab_set()

        self.window.title('拆分pcap为多条流')
        self.files=[]
        self.result=''
        self.layout_1()


    def select_file(self):
        self.filepath = askopenfilename(title= "Select pcap file", filetypes= (("pcap files", "*.pcap"),("pcap files", "*.pcapng")))
        self.l4.insert('end',self.filepath+'\n')
        self.l3.configure(state='')

    def to_2(self):
        self.l3.configure(state='disable')
        ss=SplitFlow(self.filepath)
        Thread(target=ss.to_split,args=(self.l4,)).start()




    def layout_1(self):
        self.frame1=ttk.Frame(self.window)
        self.frame1.pack(pady=5)

        self.l1=ttk.Button(self.frame1,text='选择文件', bootstyle="success",command=self.select_file)
        self.l1.pack(side='left',pady=5)
        self.l3=ttk.Button(self.frame1,text='确定', state='disable',bootstyle="success",command=self.to_2)
        self.l3.pack(side='left',padx=10,pady=5)

        self.l4=ttk.ScrolledText(self.window,width=40,height=10)
        self.l4.insert('end','请选择pcap或者pcapng文件'+'\n')
        self.l4.insert('end','以四元组作为拆分依据'+'\n')
        self.l4.insert('end','拆分文件以四元组进行命名'+'\n')
        self.l4.pack()
        self.window.mainloop()


if __name__ == '__main__':
    aa=Split_ui(1)