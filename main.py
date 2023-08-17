import ttkbootstrap as ttk
from changePacetUI import ChangePacetUI
from compare_pcap_ui import Compare_ui
from merge_pcap_ui import Merge_ui
from splitFlow_ui import Split_ui
from machProto_danger_ui import MachProto_danger_ui
from editPackets import EditPackets

root = ttk.Window(
    title='Pcaptool',
    size=(300,320)
)
root.place_window_center()    #让显现出的窗口居中
# root.wm_attributes('-topmost', 1)  # 让主窗口置顶
root.call('tk', 'scaling', 1.333)

def ip_port():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    changeipportwindowobject = ChangePacetUI(root)
    changeipportwindowobject.run()

def com_packet():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    comparewindowobject = Compare_ui(root)
    comparewindowobject.layout_1()

def edit_packets():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    comparewindowobject = EditPackets(root)
    comparewindowobject.run()

def merge_pcap():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    comparewindowobject = Merge_ui(root)
    comparewindowobject.layout_1()

def split_pcap():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    comparewindowobject = Split_ui(root)
    comparewindowobject.layout_1()

def mach_Proto_danger():
    # print(ttk.Style().theme_names())#可设置主题风格['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero']
    comparewindowobject = MachProto_danger_ui(root)
    comparewindowobject.layout_1()


ttk.Button(text="合并pcap文件 ",bootstyle='info', command=merge_pcap).pack(pady=10)
ttk.Button(text="拆分pcap为多条流 ",bootstyle='success', command=split_pcap).pack(pady=10)
ttk.Button(text="对比两个pcap文件 ",bootstyle='warning', command=com_packet).pack(pady=10)
ttk.Button(text="pcap字段编辑工具 ",bootstyle='dark',command=edit_packets).pack(pady=10)
ttk.Button(text="修改pcap的IP和端口 ",bootstyle='primary', command=ip_port).pack(pady=10)
ttk.Button(text="生成标准协议和威胁报文 ",bootstyle='danger',command=mach_Proto_danger).pack(pady=10)


root.mainloop()