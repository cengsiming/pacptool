
import ttkbootstrap as ttk
from threading import Thread
from scanping import MMMping

class Scan:
    def __init__(self,root):
        # self.window=ttk.Window(
        # title='修改IP和端口',
        # resizable=None,         #设置窗口是否可以更改大小
        # alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        # )
        self.window=root
        # self.window=ttk.Toplevel(
        # master=root,
        # title='扫描器',
        # resizable=None,         #设置窗口是否可以更改大小
        # alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        # )
        # self.window.grab_set()

    def commit(self):
        try:
            iplist = self.l4.get().split(',')
            if self.random_arg.get() == "0":
                port = ""
            else:
                port=self.l5.get()
            self.l2.config(state='disable')
            xx = MMMping(iplist,port,self.l2,self.l3)
            Thread(target=xx.formatHost,daemon=True).start()


        except Exception as e:
            self.l3.insert('end','参数错误！！！'+str(e)+'\n')
            self.l2.config(state='')


    def lay(self):
        self.franme1 = ttk.Frame(self.window)
        self.franme1.pack(pady=5,fill='both')
        self.franme2 = ttk.Frame(self.window)
        self.franme2.pack(pady=5,fill='both')
        self.franme3 = ttk.Frame(self.window)
        self.franme3.pack(pady=5)

        ttk.Label(self.franme1,text='IP:').pack(side=ttk.LEFT, padx=10)
        self.l4=ttk.Entry(self.franme1,width=300)
        self.l4.pack(side=ttk.LEFT,fill='both')

        ttk.Label(self.franme2,text='Port:').pack(side=ttk.LEFT, padx=4)
        self.l5=ttk.Entry(self.franme2,width=300)
        self.l5.pack(side=ttk.LEFT,fill='both')

        self.random_arg=ttk.StringVar()
        self.random_arg.set("0")
        self.l6=ttk.Checkbutton(self.franme3,text="扫描端口",variable=self.random_arg, bootstyle="round-toggle")
        self.l6.pack(side=ttk.LEFT, padx=40)

        self.l2=ttk.Button(self.franme3,text="确定",command=self.commit)
        self.l2.pack(side=ttk.LEFT, padx=20)

        self.l3=ttk.ScrolledText(self.window,height=50)
        self.l3.insert('end','1、IP输入示例：192.168.1.1,172.17.18.50-172.17.18.51,10.0.0.8/30'+'\n')
        self.l3.insert('end','2、Port输入示例：80,8080,6000-7000'+'\n')
        self.l3.insert('end','3、每次扫描不能超过65535个IP地址'+'\n')
        self.l3.insert('end','4、端口扫描比较缓慢，最好指定IP'+'\n')
        self.l3.pack(fill='both')
        ...

    def run(self):
        self.lay()
        self.window.mainloop()



if __name__ == '__main__':
    aaa=Scan(1)
    aaa.run()