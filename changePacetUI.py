import time,re

from changePacket import ChangePacket,ipaddress
import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename
from threading import Thread


class ChangePacetUI:
    def __init__(self,root):
        # self.window=ttk.Window(
        # title='修改IP和端口',
        # resizable=None,         #设置窗口是否可以更改大小
        # alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        # )

        self.window=ttk.Toplevel(
        master=root,
        title='修改IP和端口',
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        )
        self.window.grab_set()


    # # self.window.place_window_center()    #让显现出的窗口居中
    # # self.window.resizable(False,False)   #让窗口不可更改大小
    # # self.window.call('tk','scaling',1.333)

        self.srcip = ttk.StringVar()
        self.dstip = ttk.StringVar()
        self.srcport = ttk.StringVar()
        self.dstport = ttk.StringVar()
        self.srcmac = ttk.StringVar()
        self.dstmac = ttk.StringVar()
        self.srcip.set("1")
        self.dstip.set("1")
        self.srcport.set("1")
        self.dstport.set("1")
        self.srcmac.set("1")
        self.dstmac.set("1")
        self.variable_content = [
            [self.srcip, "源IP"],
            [self.dstip, "目的IP"],
            [self.srcport, "源端口"],
            [self.dstport, "目的端口"],
            [self.srcmac, "源mac"],
            [self.dstmac, "目的mac"]
        ]
        self.filepath=''
        self.check_srcip2=self.window.register(self.check_srcip)#注册验证函数
        self.check_srcport2=self.window.register(self.check_srcport)
        self.check_srcmac2=self.window.register(self.check_srcmac)
        self.check_dstip2=self.window.register(self.check_dstip)#注册验证函数
        self.check_dstport2=self.window.register(self.check_dstport)
        self.check_dstmac2=self.window.register(self.check_dstmac)#注册验证函数

        self.srcip_check=True
        self.dstip_check=True
        self.srcport_check=True
        self.dstport_check=True
        self.srcmac_check=True
        self.dstmac_check=True

    def specify_arg(self):
        if self.random_arg.get()=="0":
            self.l31.pack(side='left')
            self.l21.pack(side='left')
            self.l32.pack(side='left')
            self.l22.pack(side='left')
            self.l33.pack(side='left')
            self.l23.pack(side='left')
            self.l34.pack(side='left')
            self.l24.pack(side='left')
            self.l35.pack(side='left')
            self.l25.pack(side='left')
            self.l36.pack(side='left')
            self.l26.pack(side='left')
            self.l4.delete("0",'end')
            self.l4.insert('0', "1")
            self.change_ensure()
            self.l6.config(text='指定')

        else:

            self.l31.pack_forget()
            self.l21.pack_forget()
            self.l32.pack_forget()
            self.l22.pack_forget()
            self.l33.pack_forget()
            self.l23.pack_forget()
            self.l34.pack_forget()
            self.l24.pack_forget()
            self.l35.pack_forget()
            self.l25.pack_forget()
            self.l36.pack_forget()
            self.l26.pack_forget()
            self.change_ensure()
            self.l6.config(text='随机')

    def change_ensure(self):
        if self.srcip_check and self.dstip_check and self.srcport_check and self.dstport_check and self.srcmac_check and self.dstmac_check and self.filepath!='':
            self.l2.config(state='')
        else:
            self.l2.config(state='disable')
            self.l3.insert('end','输入不合法'+'\n')

    def check_srcip(self,x):
        if x=='':
            self.srcip_check=True
            self.change_ensure()
            return True
        try:
            ipaddress.ip_address(x)
            self.srcip_check=True
            self.change_ensure()
            return True
        except:
            self.srcip_check=False
            self.change_ensure()
            return False

    def check_dstip(self,x):
        if x=='':
            self.dstip_check=True
            self.change_ensure()
            return True
        try:
            ipaddress.ip_address(x)
            self.dstip_check=True
            self.change_ensure()
            return True
        except:
            self.dstip_check=False
            self.change_ensure()
            return False

    def check_srcport(self,x):
        if x=='':
            self.srcport_check=True
            self.change_ensure()
            return True
        elif x.isdecimal() and int(x)<65535:
            self.srcport_check=True
            self.change_ensure()
            return True
        else:
            self.srcport_check=False
            self.change_ensure()
            return False

    def check_dstport(self,x):
        if x=='':
            self.dstport_check=True
            self.change_ensure()
            return True
        elif x.isdecimal() and int(x)<65535:
            self.dstport_check=True
            self.change_ensure()
            return True
        else:
            self.dstport_check=False
            self.change_ensure()
            return False

    def check_srcmac(self,x):
        pattern = r'^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})$'
        if x=='':
            self.srcmac_check=True
            self.change_ensure()
            return True
        elif re.match(pattern, x):
            self.srcmac_check=True
            self.change_ensure()
            return True
        else:
            self.srcmac_check=False
            self.change_ensure()
            return False

    def check_dstmac(self,x):
        pattern = r'^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})$'
        if x=='':
            self.dstmac_check=True
            self.change_ensure()
            return True
        elif re.match(pattern, x):
            self.dstmac_check=True
            self.change_ensure()
            return True
        else:
            self.dstmac_check=False
            self.change_ensure()
            return False


    def ensure(self):
        # print("count",int(self.l4.get()),"revise_mode=",self.l6.cget('text'),"filepath=",self.filepath,
        #       "srcip_mode=",int(self.srcip.get()),"dstip_mode=",int(self.dstip.get()),
        #                     " srcport_mode=",int(self.srcport.get()),"dstport_mode=",int(self.dstport.get()),
        #       "srcip=",self.l21.get(),"dstip=",self.l22.get(),"srcport=",self.l23.get(),"dstport=",self.l24.get())
        # return 1
        try:
            if not self.l4.get().isdecimal():
                self.l3.insert('end', "修改次数输入有误" + '\n')
                return
            self.l2.config(state='disable')
            self.l5.config(state='disable')
            time.sleep(0.2)
            self.l3.insert('end',"srcip:"+self.filepath+'\n')
            self.l3.insert('end',"srcip:"+self.srcip.get()+'\n')
            self.l3.insert('end',"dstip:"+self.dstip.get()+'\n')
            self.l3.insert('end',"srcport:"+self.srcport.get()+'\n')
            self.l3.insert('end',"dstport:"+self.dstport.get()+'\n')
            self.l3.insert('end',"srcmac:"+self.srcmac.get()+'\n')
            self.l3.insert('end',"dstmac:"+self.dstmac.get()+'\n')
            self.l3.insert('end','修改次数：'+self.l4.get()+'\n')
            self.l3.insert('end',"开始执行"+'\n')
            self.l13.start(200) #间隔默认为200毫秒（5步/秒）
            self.l3.insert('end',"正在执行"+'\n')
            tmp=ChangePacket(count=int(self.l4.get()),revise_mode=self.l6.cget('text'),filepath=self.filepath,srcip_mode=int(self.srcip.get()),dstip_mode=int(self.dstip.get()),
                             srcport_mode=int(self.srcport.get()),dstport_mode=int(self.dstport.get()),srcmac_mode=int(self.srcmac.get()),dstmac_mode=int(self.dstmac.get()),srcip=self.l21.get(),dstip=self.l22.get(),srcport=self.l23.get(),dstport=self.l24.get(),srcmac=self.l25.get(),dstmac=self.l26.get())
            Thread(target=tmp.run,args=(self.l3,self.l2,self.l5,self.l13)).start()
        except Exception as e:
            self.l3.insert('end',str(e)+'\n')
            self.l3.insert('end',"未知错误"+'\n')

    def open_file(self):
        path = askopenfilename(title= "Select pcap file", filetypes= (("pcap files", "*.pcap"),("pcap files", "*.pcapng")))
        self.l3.insert('end',path + '\n')
        # print(path)
        self.l1.configure(text=path)
        self.l1.pack(side='left',padx=5)
        if not path:
            # print('请选择pcap文件')
            self.filepath = ''
            self.l3.insert('end', '请选择pcap文件' + '\n')
            return
        if path.endswith('.pcap') or path.endswith('.pcapng'):
            self.l3.insert('end', '文件类型正确' + '\n')
            self.filepath=path
            self.change_ensure()
            return
        else:
            self.l2.config(state='disable')
            self.filepath = ''
            self.l3.insert('end', '文件类型错误' + '\n')
            # print('文件类型错误')
            return

    def lay(self):

        self.franme1 = ttk.Frame(self.window)
        self.franme1.pack(pady=5)
        self.franme4 = ttk.Frame(self.window)
        self.franme4.pack(pady=5)
        self.franme2 = ttk.Frame(self.window)
        self.franme2.pack(pady=5)
        self.franme4 = ttk.Frame(self.window)
        self.franme4.pack(pady=5)
        self.franme3 = ttk.Frame(self.window)
        self.franme3.pack(pady=5)
        self.l5=ttk.Button(self.franme1,text="选择文件",command=self.open_file)
        self.l5.pack(side='left',padx=5)
        self.l1=ttk.Label(self.franme4)

        ttk.Checkbutton(self.franme2, text="源IP", variable=self.variable_content[0][0]).pack(side=ttk.LEFT, padx=5)
        ttk.Checkbutton(self.franme2, text="目的IP", variable=self.variable_content[1][0]).pack(side=ttk.LEFT, padx=5)
        ttk.Checkbutton(self.franme2, text="源端口", variable=self.variable_content[2][0]).pack(side=ttk.LEFT, padx=5)
        ttk.Checkbutton(self.franme2, text="目的端口", variable=self.variable_content[3][0]).pack(side=ttk.LEFT, padx=5)
        ttk.Checkbutton(self.franme4, text="源mac", variable=self.variable_content[4][0]).pack(side=ttk.LEFT, padx=5)
        ttk.Checkbutton(self.franme4, text="目的mac", variable=self.variable_content[5][0]).pack(side=ttk.LEFT, padx=5)


        self.random_arg=ttk.StringVar()
        self.random_arg.set("1")
        self.l6=ttk.Checkbutton(self.franme1, text="随机",variable=self.random_arg, bootstyle="round-toggle",command=self.specify_arg)
        self.l6.pack(side=ttk.LEFT, padx=5)

        ttk.Label(self.franme3,text='修改次数:').pack(side=ttk.LEFT)
        self.l4=ttk.Entry(self.franme3,width=3)
        self.l4.insert('0','1')
        self.l4.pack(side=ttk.LEFT, padx=10)

        self.l2=ttk.Button(self.franme3,text="确定",state='disable',command=self.ensure)
        self.l2.pack(side=ttk.LEFT, padx=5)

        self.l13 = ttk.Progressbar(self.franme3, bootstyle="primary-striped",mode=ttk.INDETERMINATE)
        self.l13.pack(side=ttk.LEFT)



        self.franme5 = ttk.Frame(self.window)
        self.franme5.pack(pady=5)
        self.l31=ttk.Label(self.franme5,text='源IP：         ')
        self.l21=ttk.Entry(self.franme5,validate="focus", validatecommand=(self.check_srcip2, '%P'))

        self.franme6 = ttk.Frame(self.window)
        self.franme6.pack(pady=5)
        self.l32=ttk.Label(self.franme6,text='目的IP：     ')
        self.l22=ttk.Entry(self.franme6,validate="focus", validatecommand=(self.check_dstip2, '%P'))

        self.franme7 = ttk.Frame(self.window)
        self.franme7.pack(pady=5)
        self.l33=ttk.Label(self.franme7,text='源端口：     ')
        self.l23=ttk.Entry(self.franme7,validate="focus", validatecommand=(self.check_srcport2, '%P'))
        #
        self.franme8 = ttk.Frame(self.window)
        self.franme8.pack(pady=5)
        self.l34=ttk.Label(self.franme8,text='目的端口：  ')
        self.l24=ttk.Entry(self.franme8,validate="focus", validatecommand=(self.check_dstport2, '%P'))

        self.franme9 = ttk.Frame(self.window)
        self.franme9.pack(pady=5)
        self.l35=ttk.Label(self.franme9,text='源mac：      ')
        self.l25=ttk.Entry(self.franme9,validate="focus", validatecommand=(self.check_srcmac2, '%P'))

        self.franme10 = ttk.Frame(self.window)
        self.franme10.pack(pady=5)
        self.l36=ttk.Label(self.franme10,text='目的mac：    ')
        self.l26=ttk.Entry(self.franme10,validate="focus", validatecommand=(self.check_dstmac2, '%P'))


        self.l3=ttk.ScrolledText(self.window,width=40,height=10)
        self.l3.insert('end','1、支持同时修改多条流'+'\n')
        self.l3.insert('end','2、只有勾选的项才会被修改'+'\n')
        self.l3.insert('end','3、某些协议无法改变IP和端口，比如ARP'+'\n')
        self.l3.insert('end','4、支持指定源目IP、端口；如果输入为空，表示该项随机'+'\n')
        self.l3.insert('end','5、指定IP模式，不支持IPv4和IPv6之间相互转换'+'\n')
        self.l3.insert('end','6、随机IP模式，支持同时修改IPv4和IPv6(多条流)，但不会互相转换'+'\n')
        self.l3.insert('end',"7、某些协议依赖端口进行识别，修改之后可能导致无法识别出原有协议或者识别出原pcap没有的协议"+'\n')
        self.l3.pack(padx=10)

    def run(self):
        self.lay()
        self.window.mainloop()



if __name__ == '__main__':
    aaa=ChangePacetUI(1)
    aaa.run()