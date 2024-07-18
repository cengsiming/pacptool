# import tkinter as tk
import ttkbootstrap as ttk
from scan_UI import Scan
from sniffPcap_ui import sniff_GUI
from send_pacet_UI import SendPacetUI
from merge_pcap_ui import Merge_ui
from change_time import ChangeTime_ui
from splitFlow_ui import Split_ui
from compare_pcap_ui import Compare_ui
from editPackets import EditPackets
from changePacetUI import Change_Pacet_UI
from machProto_danger_ui import MachProto_danger_ui

def show_frame(container, frame_class,funcName,size):
    # 销毁容器内的所有子组件
    for widget in container.winfo_children():
        widget.destroy()
    # 创建新帧并添加到容器中
    new_frame = frame_class(container)
    main_Labelframe.config(text=funcName)
    root.geometry(size)
    new_frame.run()



def scan():
    show_frame(main_frame, Scan,"扫描器","800x700")

def sniff():
        # 销毁容器内的所有子组件
    for widget in main_frame.winfo_children():
        widget.destroy()
    # 创建新帧并添加到容器中
    new_frame = sniff_GUI(root,main_frame)
    main_Labelframe.config(text="网络嗅探")
    root.geometry("1100x720")
    new_frame.run()


def send_pcap():
    show_frame(main_frame, SendPacetUI,"发送数据包","800x700")

def merge_pcap():
    show_frame(main_frame, Merge_ui,"合并pcap文件","800x700")


def change_time():
    show_frame(main_frame, ChangeTime_ui,"修改时间戳","800x700")


def split_pcap():
    show_frame(main_frame, Split_ui,"拆分pcap为多条流","800x700")


def compare_pcap():
    show_frame(main_frame, Compare_ui,"对比两个pcap文件","800x700")


def edit_packet():
    show_frame(main_frame, EditPackets,"pcap字段编辑工具","1100x700")


def change_six():
    show_frame(main_frame, Change_Pacet_UI,"修改pcap的六元组","800x700")


def danger():
    show_frame(main_frame, MachProto_danger_ui,"生成标准协议和威胁报文","800x700")



root = ttk.Window(
    title='Pcaptool',
    size=(1100,700)
)


# 创建侧边导航栏
sidebar = ttk.Frame(root)
sidebar.pack(side='left',padx=5,pady=10, fill='y')

# 创建主页面容器
main_Labelframe = ttk.Labelframe(root,bootstyle="secondary")
main_Labelframe.pack(padx=5,pady=5,  fill='both')

main_frame = ttk.Frame(main_Labelframe)

main_frame.pack(padx=10,pady=10, fill='both')

# 添加导航按钮
ttk.Button(sidebar,bootstyle="light", text='扫描器', command=scan).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='网络嗅探', command=sniff).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light",text='发送数据包', command=send_pcap).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='合并pcap文件', command=merge_pcap).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='修改时间戳', command=change_time).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='拆分pcap为多条流', command=split_pcap).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='对比两个pcap文件', command=compare_pcap).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='pcap字段编辑工具', command=edit_packet).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='修改pcap的六元组', command=change_six).pack(pady=3, fill='x')
ttk.Button(sidebar,bootstyle="light", text='生成标准协议和威胁报文', command=danger).pack(pady=3, fill='x')

# 初始化显示
scan()

root.mainloop()
