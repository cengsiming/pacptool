import os.path
import ttkbootstrap as ttk
import shutil
from create_danger_pcap import Create_danger_pcap

class MachProto_danger_ui:
    def __init__(self,root):
        self.window = root
        # self.window=ttk.Toplevel(
        # master=root,
        # title='生成标准协议和威胁报文',
        # resizable=None,         #设置窗口是否可以更改大小
        # alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        # )
        # self.window.grab_set()
        # self.window = ttk.Window()  # 实例化
        # self.window.call('tk', 'scaling', 1.333)  # 设置程序缩放为1.333
        # self.window.geometry('300x200')  # 窗口大小
        # self.window.title('生成标准协议和威胁报文')
        self.repath=os.path.dirname(os.path.realpath(__file__))
        self.create_danger=Create_danger_pcap()
        # self.layout_1()


    def get_mode(self):
        self.modename=self.l1.get()
        self.modename2=self.l0.get()
        if self.modename and self.modename!='常见协议':
            shutil.copy(fr'{self.repath}/machproto/{self.modename}.pcap',f'./{self.modename}_demo.pcap')
        if self.modename2 and self.modename2!='威胁报文':
            self.create_danger.start_modify(self.modename2)
        self.l2.config(text='done！ 保存至当前目录', state='disable')
        self.l3.insert('end',f'已生成{self.modename}_demo.pcap\n')


    def run(self):
        self.l0 = ttk.Combobox(self.window, width=20,bootstyle="danger",values=['威胁报文','tcp_synflood','udp_synflood','Bot_Scanner','CVE-2019-0801','Weblogic','Powershell_script'],state='readonly')
        self.l0.current(0)  # 首先展示values里面索引的对应的值
        self.l0.pack(pady=10,fill='both')
        self.l1 = ttk.Combobox(self.window, width=20, bootstyle="danger",values=['常见协议','ARP','DHCP','DNS','FTP','ICMP','HTTP','HTTPS','SSH','TCP','UDP'],state='readonly')
        self.l1.current(0)  # 首先展示values里面索引的对应的值
        self.l1.pack(pady=30,fill='both')
        self.l2=ttk.Button(self.window,text='确定', bootstyle="danger",command=self.get_mode)
        self.l2.pack(fill='both')
        self.l3=ttk.ScrolledText(self.window,height=50)
        self.l3.pack(pady=5,fill='both')


if __name__ == '__main__':
    ...