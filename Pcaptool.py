import ttkbootstrap as ttk
from changePacetUI import ChangePacetUI
from compare_pcap_ui import Compare_ui
from merge_pcap_ui import Merge_ui
from splitFlow_ui import Split_ui
from machProto_danger_ui import MachProto_danger_ui
from editPackets import EditPackets
from change_time import ChangeTime_ui
from sniffPcap_ui import GUI
from scan_UI import Scan
from send_pacet_UI import SendPacetUI

root = ttk.Window(
    title='Pcaptool',
    size=(300,520)
)
root.place_window_center()  
root.call('tk', 'scaling', 1.333)

def ip_port():
 
    viewobject = ChangePacetUI(root)
    viewobject.run()

def com_packet():
    
    viewobject = Compare_ui(root)
    viewobject.layout_1()

def edit_packets():
   
    viewobject = EditPackets(root)
    viewobject.run()

def merge_pcap():
   
    viewobject = Merge_ui(root)
    viewobject.layout_1()

def split_pcap():
 
    viewobject = Split_ui(root)
    viewobject.layout_1()

def mach_Proto_danger():
 
    viewobject = MachProto_danger_ui(root)
    viewobject.layout_1()

def changeTime():
  
    viewobject = ChangeTime_ui(root)
    viewobject.layout_1()

def sniffPcap():
   
    GUI(root)

def scan_packets():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    viewobject = Scan(root)
    viewobject.run()


def send_packets():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    viewobject = SendPacetUI(root)
    viewobject.run()


ttk.Button(text="扫描器 ",bootstyle="light", command=scan_packets).pack(pady=10)
ttk.Button(text="网络嗅探 ",bootstyle="dark-outline", command=sniffPcap).pack(pady=10)
ttk.Button(text="发送数据包 ",bootstyle="dark-outline", command=send_packets).pack(pady=10)
ttk.Button(text="合并pcap文件 ",bootstyle='info', command=merge_pcap).pack(pady=10)
ttk.Button(text="修改pcap时间戳 ",bootstyle='secondary',command=changeTime).pack(pady=10)
ttk.Button(text="拆分pcap为多条流 ",bootstyle='success', command=split_pcap).pack(pady=10)
ttk.Button(text="对比两个pcap文件 ",bootstyle='warning', command=com_packet).pack(pady=10)
ttk.Button(text="pcap字段编辑工具 ",bootstyle='dark',command=edit_packets).pack(pady=10)
ttk.Button(text="修改pcap的六元组 ",bootstyle='primary', command=ip_port).pack(pady=10)
ttk.Button(text="生成标准协议和威胁报文 ",bootstyle='danger',command=mach_Proto_danger).pack(pady=10)


root.mainloop()