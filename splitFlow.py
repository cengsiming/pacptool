import os
import random
import copy
import time
from scapy.all import rdpcap, wrpcap
import ipaddress
import hashlib


class SplitFlow():
    def __init__(self, filepath):
        self.not_to_modify=''
        self.original_packets = rdpcap(fr'{filepath}')
        self.dic = {}
        self.dic2 = {}
        self.get_hashdict()

    def get_hashdict(self):
        for j, i in enumerate(self.original_packets):
            ha = hashlib.md5()
            try:
                srcip = i.payload.src
                dstip = i.payload.dst
            except:
                self.not_to_modify+=('无法修改,序号：'+str(j + 1)+'\n')
                # print('无法修改,序号：',j + 1)
                srcip = ""
                dstip = ""
            try:
                srcport = str(i.payload.payload.sport)
                dstport = str(i.payload.payload.dport)
            except:
                srcport = ""
                dstport = ""
            li = [srcip, dstip, srcport, dstport]
            li.sort()
            ss = ','.join(li)
            ha.update(ss.encode())
            if self.dic.get(ha.hexdigest()):#以会话的第一个包的四元组做value
                ...
            else:
                self.dic[ha.hexdigest()] = []
                srcip=srcip.replace(':',"：")
                dstip=dstip.replace(':',"：")
                self.dic2[ha.hexdigest()] = str(f'srcip-{srcip}_dstip-{dstip}_srcport-{srcport}_dstport-{dstport}')

    def to_split(self,l):
        new_packets = copy.deepcopy(self.original_packets)
        for j, i in enumerate(new_packets):
            ha = hashlib.md5()
            try:
                srcip = i.payload.src
                dstip = i.payload.dst
            except:
                srcip = ''
                dstip = ''
            try:
                srcport = str(i.payload.payload.sport)
                dstport = str(i.payload.payload.dport)
            except:
                srcport = ""
                dstport = ""
            li = [srcip, dstip, srcport, dstport]
            li.sort()
            ss = ','.join(li)
            ha.update(ss.encode())
            self.dic[ha.hexdigest()].append(i)
        tmpdir=f'{time.time()}'
        os.mkdir(tmpdir)
        for m,n in self.dic.items():
            wrpcap(f'./{tmpdir}/{self.dic2[m]}'+'.pcap',n)
        # print(f'共拆分出{len(self.dic)}条流')
        # print(f'已保存至{tmpdir}目录下')
        l.insert('end',f"共拆分出{len(self.dic)}条流"+'\n')
        l.insert('end',f"已保存至{tmpdir}目录下"+'\n')



if __name__ == '__main__':
    s = time.time()
    print('正在执行')
    aaa = SplitFlow(r'C:\Users\Admin\Desktop\学习资料\test1.pcap')
    aaa.to_split()
    print(time.time() - s)
