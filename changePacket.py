import random
import copy
import time
from scapy.all import rdpcap, wrpcap
import ipaddress
import hashlib


class ChangePacket():
    def __init__(self, count, revise_mode,filepath, srcip_mode=True, dstip_mode=True, srcport_mode=True, dstport_mode=True,srcip='',dstip='',srcport='',dstport=''):
        self.count = count
        self.not_to_modify=''
        self.n = random.randint(1, 65535 - count)
        self.original_packets = rdpcap(fr'{filepath}')
        self.dic = {}
        self.get_hashdict()
        self.allpackets = []
        self.srcip_mode = srcip_mode
        self.dstip_mode = dstip_mode
        self.srcport_mode = srcport_mode
        self.dstport_mode = dstport_mode
        if revise_mode=='指定':
            self.srcip=srcip
            self.dstip=dstip
            self.srcport=int(srcport) if srcport!='' else ''
            self.dstport=int(dstport) if dstport!='' else ''
        else:
            self.srcip=''
            self.dstip=''
            self.srcport=''
            self.dstport=''


    def change_ip(self, i, n, srcip_mode, dstip_mode,srcip,dstip):
        specify_srcip=srcip
        specify_dstip=dstip
        if srcip_mode:
            if specify_srcip=='':
                try:
                    i.payload.src = ipaddress.ip_address(i.payload.src) + n
                except:
                    i.payload.src = ipaddress.ip_address(18100101) + n
            else:
                try:
                    if (":" in i.payload.src and ":" in specify_srcip) or  ("." in i.payload.src and  ":"  not in i.payload.src and "." in specify_srcip) :
                        i.payload.src = ipaddress.ip_address(specify_srcip)
                    else:
                        ...
                except:
                    ...
        if dstip_mode:
            if specify_dstip=='':
                try:
                    i.payload.dst = ipaddress.ip_address(i.payload.dst) + n
                except:
                    i.payload.dst = ipaddress.ip_address(18100101) + n
            else:
                try:
                    if (":" in i.payload.dst and ":" in specify_dstip) or  ("." in i.payload.dst and  ":"  not in i.payload.dst and "." in specify_dstip) :
                        i.payload.dst = ipaddress.ip_address(specify_dstip)
                    else:
                        ...
                except:
                    ...
        else:
            ...




    def change_port(self, i, n, srcport_mode, dstport_mode,srcport,dstport):
        specify_srcport=srcport
        specify_dstport=dstport
        if not srcport_mode and not dstport_mode:
            return None
        try:
            srcport = i.payload.payload.sport
            dstport = i.payload.payload.dport
        except:
            return None
        if srcport_mode:
            if specify_srcport=='':
                i.payload.payload.sport = (srcport + n) % 65535
            else:
                i.payload.payload.sport = int(specify_srcport)
        if dstport_mode:
            if specify_dstport=='':
                i.payload.payload.dport = (dstport + n) % 65535
            else:
                i.payload.payload.dport = int(specify_dstport)

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
                self.dic[ha.hexdigest()] = [srcip, dstip, srcport, dstport]

    def to_change(self, n, srcip_mode, dstip_mode, srcport_mode, dstport_mode):
        specify_srcip=self.srcip
        specify_dstip=self.dstip
        specify_srcport=self.srcport
        specify_dstport=self.dstport
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
            if srcip == self.dic[ha.hexdigest()][0]:
                self.change_ip(i, n, srcip_mode, dstip_mode,specify_srcip,specify_dstip)
                self.change_port(i, n, srcport_mode, dstport_mode,specify_srcport,specify_dstport)
            elif srcip == self.dic[ha.hexdigest()][1]:
                self.change_ip(i, n, dstip_mode, srcip_mode,specify_dstip,specify_srcip)
                self.change_port(i, n, dstport_mode, srcport_mode,specify_dstport,specify_srcport)
            else:
                self.not_to_modify+=('无法修改的数据包,序号：'+str(j + 1)+'\n')
                # print('无法修改', j + 1)
            try:
                i.payload.chksum = None
            except:
                ...
            try:
                i.payload.payload.chksum = None
            except:
                ...
            try:
                i.payload.payload.payload.chksum = None
            except:
                ...
        self.allpackets += new_packets

    def run(self,l3,l2,l5,l13):
        s=time.time()
        for i in range(self.count):
            self.to_change(self.n, self.srcip_mode, self.dstip_mode, self.srcport_mode, self.dstport_mode)
            self.n += 1
        newfilename=str(time.time())+ '.pcap'
        wrpcap(newfilename , self.allpackets)
        print(time.time()-s)
        l3.insert('end', self.not_to_modify + '\n')
        l3.insert('end', "执行完毕,文件保存在当前目录下:" + newfilename + '\n')
        l3.insert('end', '运行时间:'+str(time.time() - s) + '\n')
        l2.config(state='')
        l5.config(state='')
        l13.stop()



if __name__ == '__main__':
    s = time.time()
    print('某些协议无法改变IP端口，比如ARP')
    print('某些协议依赖端口进行识别')
    print('修改之后可能导致无法识别出协议或者识别出源pcap没有的协议')
    print('正在执行')
    aaa = ChangePacket(1,'指定' ,r'C:\Users\z1203\Desktop\test1.pcap', srcip_mode=True, dstip_mode=True, srcport_mode=True,
                       dstport_mode=True,srcip='192.168.1.1',dstip='f1::01',srcport=111,dstport=222)
    aaa.run(1,2,3,4)
    print(time.time() - s)
