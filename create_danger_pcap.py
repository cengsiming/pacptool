from scapy.all import *
import random
import os
import copy
import pickle
import base64
class Create_danger_pcap:
    def __init__(self):
        ...
        self.path=os.path.dirname(os.path.realpath(__file__))#py真实路径
        self.path2 = os.path.dirname(os.path.realpath(__name__))#exe真实路径

    def IP_ran(self):
        return  f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}'

    def port_ran(self):
        return random.randint(1,65536)

    def start_modify(self,modename):
        with open(fr'{self.path}\danger_pcap_pickle\{modename}.pcap.pickle', 'rb') as f:
            ccc = pickle.load(f)
        bbb = base64.b64decode(ccc)
        aaa = base64.b64decode(bbb)
        with open(fr'{self.path}\{modename}.pcap', 'wb') as f:
            f.write(aaa)
        tcp_synflood=rdpcap(fr'{self.path}\{modename}.pcap')
        src=tcp_synflood[0].payload.src
        dst=tcp_synflood[0].payload.dst
        newsrc=self.IP_ran()
        newdst=self.IP_ran()
        tempcap_list=[]
        for j in tcp_synflood:
            i=copy.deepcopy(j)
            if i.payload.src==src:
                i.payload.src=newsrc
                i.payload.dst=newdst
            elif  i.payload.src==dst:
                i.payload.src=newdst
                i.payload.dst=newsrc
            else:
                print('不对')
            i.payload.chksum = None
            i.payload.payload.chksum = None
            tempcap_list.append(i)
        wrpcapng(fr'{self.path2}\{modename}_demo.pcap',tempcap_list)


if __name__ == '__main__':
    ...
    aaa=Create_danger_pcap()
    # aaa.start_modify('tcp_synflood')
    # aaa.start_modify('Bot_Scanner')
    # aaa.start_modify('CVE-2019-0801')
    # aaa.start_modify('Powershell_script')
    # aaa.start_modify('WebLogic')



