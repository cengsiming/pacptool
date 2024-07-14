
from scapy.all import *
from ttkbootstrap import *
import ttkbootstrap as tk
from tkinter.filedialog import askopenfilename
import tkinter.font as tkFont
from tkinter.messagebox import showinfo,showerror,showwarning
from scapy_layer_all import *



class EditPackets:
    def __init__(self,root):
        # self.root = tk.Window()
        # self.root.title('pcap字段编辑工具')
        # self.root.geometry('900x600')

        self.window=tk.Toplevel(
        master=root,
        title='pcap字段编辑工具',
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        size=(900, 610)
        )
        self.window.grab_set()


        self.frame0 = tk.Frame(self.window)
        self.frame0.place(x=10, y=10, width=880, height=30, )

        self.frame1 = tk.Frame(self.window)
        self.frame1.place(x=10, y=90, width=880, height=158,)

        self.frame2 = tk.Frame(self.window )
        self.frame2.place(x=10, y=270, width=880, height=158,)
        # 设定黄色，以确定我实际发生测试的区域
        # self.frame2.config(bg='blue')

        self.frame3 = tk.Frame(self.window )
        self.frame3.place(x=10, y=440, width=880, height=158, )
        # 设定黄色，以确定我实际发生测试的区域
        # self.frame3.config(bg='yellow')
        self.packet_handling = None

        self.button()
        self.packet_list()
        self.tree_layer()
        self.hex_content()
        # self.update_layer_list(packet)
        self.packets = []
        self.count = 0


    def select_file(self):
        self.filepath = askopenfilename(title= "Select pcap file", filetypes= (("pcap files", "*.pcap"),("pcap files", "*.pcapng")))
        self.ll1.config(text=self.filepath)
        if '.pcap' in self.ll1.cget('text'):
            self.Button0.configure(state='')
            self.Button2.configure(state='disable')
        else:
            self.Button0.configure(state='disable')

    def button(self):

        self.Button0 = tk.Button(self.frame0,text="Start", command=self.get_packet,state='disable',style='dark')
        self.Button0.pack(side=LEFT,padx=10)

        self.Button1 = tk.Button(self.frame0,text="Save", command=self.save_pcap,state='disable',style='dark')
        self.Button1.pack(side=LEFT,padx=40)

        self.Button2 = tk.Button(self.frame0,text="选择文件", command=self.select_file,style='dark')
        self.Button2.pack(side=LEFT,padx=20)

        self.ll1=tk.Label(self.frame0,text='')
        self.ll1.pack(side=LEFT,padx=20)

    def packet_list(self):
        columns = ['No', 'Source', 'Destination', 'Protocol', 'Length', 'Info']

        sl = Scrollbar(self.frame1)
        sl.pack(side=RIGHT, fill=Y)

        self.table = Treeview(
            master=self.frame1,  # 父容器
            height=7,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列
            yscrollcommand=sl.set
        )
        sl['command'] = self.table.yview

        # ybar.grid(row=2,column=2,sticky='ns')
        self.table.bind("<<TreeviewSelect>>", self.onSelect_packet_list)
        self.table.heading(column='No', text='No', )  # 定义表头
        self.table.heading('Source', text='Source', )  # 定义表头
        self.table.heading('Destination', text='Destination', )  # 定义表头
        self.table.heading('Protocol', text='Protocol', )  # 定义表头
        self.table.heading('Length', text='Length', )  # 定义表头
        self.table.heading('Info', text='Info', )  # 定义表头
        self.table.column('No', width=70, minwidth=10, anchor=S)  # 定义列
        self.table.column('Source', width=150, minwidth=10, anchor=S)  # 定义列
        self.table.column('Destination', width=150, minwidth=10, anchor=S)  # 定义列
        self.table.column('Protocol', width=100, minwidth=10, anchor=S)  # 定义列
        self.table.column('Length', width=70, minwidth=10, anchor=S)  # 定义列
        self.table.column('Info', width=310, minwidth=10, anchor=S)  # 定义列
        self.table.pack(side=LEFT, fill=Y)

    def save_pcap(self):
        self.newname=f'{time.time()}.pcap'
        try:
            wrpcap(self.newname, self.packets)
            showinfo(title='', message=f'文件已保存至{self.newname}')
        except Exception as e:
            showerror(title='', message='保存文件失败'+str(e))

    def onSelect_packet_list(self, e):
        itm = self.table.set(self.table.focus())
        print(itm)
        packet = self.packets[eval(itm['No']) - 1]
        self.tempacket=packet
        self.packet_handling = packet
        self.update_layer_list(packet)
        pass


    def start(self):
        T1 = threading.Thread(name='t1', target=self.get_packet, daemon=True)  # 子线程
        T1.start()  # 启动

    def get_packet(self):
        self.packets = sniff(
            offline=self.ll1.cget("text"),
            count=4000
        )
        self.Button0.configure(state='disable')

        print('开始载入')
        for i in self.packets:
            self.count += 1
            self.thread_handle_packet(i)

    def thread_handle_packet(self, packet):
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
        else:
            src = packet.src
            dst = packet.dst
        layer = None
        for var in self.get_packet_layers(packet):
            if not isinstance(var, (Padding, Raw)):
                layer = var
        if layer.name[0:3] == "DNS":
            protocol = "DNS"
        else:
            protocol = layer.name
        length = f"{len(packet)}"
        try:
            info = str(packet.summary())
        except:
            info = "error"
        show_info = [self.count, src, dst, protocol, length, info]
        self.table.insert('', END, values=show_info)

    def get_packet_layers(self, packet):
        counter = 0
        while True:
            layer = packet.getlayer(counter)
            if layer is None:
                break
            yield layer
            counter += 1

    def edit_item(self, x):
        item_id = self.tree_layer.focus()
        self.parent_layer=self.tree_layer.item(self.tree_layer.parent(item_id) ,option='text')
        try:
            layer_name = self.tree_layer.item(item_id, option='text')  # 获取点击的是哪一层
        except:
            return
        old_values = [layer_name]

        # 创建编辑窗口
        edit_window = tk.Toplevel(
        master=self.window,
        title='编辑字段',
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        size=(300, 100)
        )

        # 创建编辑输入框
        edit_entries = []
        for i, value in enumerate(old_values):
            entry = tk.Entry(edit_window)
            entry.insert(0, value if value is not None else "")
            entry.pack(pady=5)
            edit_entries.append(entry)

        def save_changes():
            self.new_values = [entry.get() for entry in edit_entries]
            self.tree_layer.item(item_id, text=self.new_values[0])
            edit_window.destroy()
            try:
                if self.new_values[0].split(':')[1].strip().isdigit():
                    setattr(self.tempacket[self.parent_layer], self.new_values[0].split(':')[0].strip(),
                            int(self.new_values[0].split(':')[1].strip()))
                else:
                    # print('不是数字')
                    self.tempacket[self.parent_layer].setfieldval(self.new_values[0].split(':')[0].strip(),self.new_values[0].split(':')[1].strip())
                    # setattr(self.tempacket[self.parent_layer], self.new_values[0].split(':')[0], self.new_values[0].split(':')[1])
            except Exception as e:
                showwarning(title='', message='修改失败'+str(e))

                # self.tempacket[self.parent_layer].setfieldval(self.new_values[0].split(':')[0],
                #                                                             int(self.new_values[0].split(':')[1]))

            ls(self.tempacket)
            try:
                self.tempacket.payload.chksum=None
                self.tempacket.payload.payload.chksum = None
            except:
                ...
            self.Button1.configure(state='')

        # 创建保存按钮
        save_button = tk.Button(edit_window, text="Save", command=save_changes,style='dark')
        save_button.pack(pady=5)



    def tree_layer(self):
        self.tree_layer = Treeview(self.frame2, height=8, columns=('qy'), show='tree')
        self.tree_layer.column('#0', width=650, stretch=False)
        self.tree_layer.pack(side=LEFT)
        s2 = Scrollbar(self.frame2)
        s2.pack(side=RIGHT, fill=Y)

        self.tree_layer['yscrollcommand'] = s2.set

        s2['command'] = self.tree_layer.yview
        self.tree_layer.bind("<Double-1>", self.edit_item)
        self.tree_layer.bind("<<TreeviewSelect>>", self.onSelect_tree_layer)

    def onSelect_tree_layer(self, e):
        item_id = self.tree_layer.focus()
        try:
            layer_name = self.tree_layer.item(item_id, option='text')  # 获取点击的是哪一层
            print(layer_name)
        except:
            return
        packet = self.packet_handling
        counter = 0
        while True:
            layer = packet.getlayer(counter)
            try:
                if layer.name == layer_name:
                    break
                if layer is None:
                    break
                counter += 1
            except:
                return
        self.hex_text.delete(1.0, END)
        self.hex_text.insert(INSERT, hexdump(layer, dump=True))

    def update_layer_list(self, packet):
        x = self.tree_layer.get_children()
        for item in x:
            self.tree_layer.delete(item)
        layer_name = []
        counter = 0
        Ethernet_layer = packet.getlayer(0)
        self.hex_text.delete(1.0, END)
        if Ethernet_layer.name == 'Ethernet':
            self.hex_text.insert(INSERT, hexdump(Ethernet_layer, dump=True))
        while True:
            layer = packet.getlayer(counter)
            if layer is None:
                break
            layer_name.append(layer)
            counter += 1
        parent_chile = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        for index, layer in enumerate(layer_name):
            parent_chile[index] = self.tree_layer.insert("", index, text=layer.name)
            print(layer.name)
            for name, value in layer.fields.items():
                self.tree_layer.insert(parent_chile[index], index, text=f"{name}: {value}")
                # if packet.haslayer(HTTPRequest):
                #     print('哈哈哈哈')
                #     print(packet[HTTPRequest].fields)

    def hex_content(self):

        self.hex_text = Text(self.frame3, width=120, height=9)
        self.hex_text.pack(side=LEFT)
        fontExample = tkFont.Font(size=10)

        self.hex_text.configure(font=fontExample)
        s3 = Scrollbar(self.frame3)
        s3.pack(side=RIGHT, fill=Y)

        self.hex_text['yscrollcommand'] = s3.set

        s3['command'] = self.hex_text.yview

    def run(self):
        self.window.mainloop()
if __name__ == '__main__':
    ...