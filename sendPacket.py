import random
import copy
import time
import os
from scapy.all import rdpcap, sendp
import ipaddress
import hashlib


class SendPacket():
    def __init__(self, stop_event,iface,send_rate,count, revise_mode,filepath, srcip_mode=False, dstip_mode=False, srcport_mode=False, dstport_mode=False,srcmac_mode=False,dstmac_mode=False,srcip='',dstip='',srcport='',dstport='',srcmac='',dstmac=''):
        self.stop_event = stop_event  # 停止信号
        self.iface = iface  # 网卡
        self.send_rate = send_rate  # 发送速率
        self.last_time = 0 # 上一个包时间戳
        self.send_num = 0 # 发送报文数
        self.count = 1000000 if count==0  else count # 循环次数
        self.not_to_modify='' # 无法修改的序号
        self.n = random.randint(1, 65535)  # 修改的初始随机值
        self.filepath = filepath 
        self.dic = {}
        self.srcip_mode = srcip_mode
        self.dstip_mode = dstip_mode
        self.srcport_mode = srcport_mode
        self.dstport_mode = dstport_mode
        self.srcmac_mode = srcmac_mode
        self.dstmac_mode = dstmac_mode
        if revise_mode=='指定':
            self.srcip=srcip
            self.dstip=dstip
            self.srcport=int(srcport) if srcport!='' else ''
            self.dstport=int(dstport) if dstport!='' else ''
            self.srcmac=srcmac
            self.dstmac=dstmac
        else:
            self.srcip=''
            self.dstip=''
            self.srcport=''
            self.dstport=''
            self.srcmac=''
            self.dstmac=''


    def to_send(self,packet):
        interval_time= float(packet.time-self.last_time)
        if interval_time>10:
            interval_time = 10
        try:
            if self.send_rate == "原速":
                time.sleep(interval_time)
            elif self.send_rate == "最高":
                ...
            elif self.send_rate == "1/2x":
                time.sleep(interval_time*2)
            elif self.send_rate == "1/4x":
                time.sleep(interval_time*4)
            elif self.send_rate == "2x":
                time.sleep(interval_time*1/2)
            elif self.send_rate == "4x":
                time.sleep(interval_time*1/4)
        except:
            # print("存在时间戳乱序包")
            ...   
        finally:
            sendp(packet, iface=self.iface, verbose=False)
            self.send_num += 1
            self.last_time = packet.time
            if self.count != 1000000:
                self.l13.step(self.once_step)


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

    def change_mac(self, i, n, srcmac_mode, dstmac_mode,srcmac,dstmac):
        if srcmac_mode:
            if srcmac=='':
                srcmac = i.src
                decimal_mac = int(srcmac.replace(":", ""), 16)
                # 将十进制数字加n
                decimal_mac += n
                # 将加1后的十进制数字转换为MAC地址
                new_mac_address = ':'.join(format(decimal_mac, '012x')[i:i+2] for i in range(0, 12, 2))
                i.src = new_mac_address
            else:
                i.src = srcmac
        if dstmac_mode:
            if dstmac=='':
                dstmac = i.dst
                decimal_mac = int(dstmac.replace(":", ""), 16)
                # 将十进制数字加n
                decimal_mac += n

                # 将加1后的十进制数字转换为MAC地址
                new_mac_address = ':'.join(format(decimal_mac, '012x')[i:i+2] for i in range(0, 12, 2))
                i.dst = new_mac_address
            else:
                i.dst = dstmac


    def get_hashdict(self):
        for j, i in enumerate(self.original_packets):
            ha = hashlib.md5()
            try:
                srcip = i.payload.src
                dstip = i.payload.dst
            except:
                self.not_to_modify+=('无法获取IP,序号：'+str(j + 1)+'\n')
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

    def to_change(self, n, srcip_mode, dstip_mode, srcport_mode, dstport_mode,srcmac_mode,dstmac_mode):
        specify_srcip=self.srcip
        specify_dstip=self.dstip
        specify_srcport=self.srcport
        specify_dstport=self.dstport
        new_packets = copy.deepcopy(self.original_packets)
        for j, i in enumerate(new_packets):
            if self.stop_event.is_set():
                # print("捕捉到停止信号,停止执行")
                return 
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
                self.change_mac(i, n, srcmac_mode, dstmac_mode,self.srcmac,self.dstmac)
            elif srcip == self.dic[ha.hexdigest()][1]:
                self.change_ip(i, n, dstip_mode, srcip_mode,specify_dstip,specify_srcip)
                self.change_port(i, n, dstport_mode, srcport_mode,specify_dstport,specify_srcport)
                self.change_mac(i, n, dstmac_mode, srcmac_mode,self.dstmac,self.srcmac)
        
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
            self.to_send(i)

    
    def not_to_change(self):
        for i in self.original_packets:
            if self.stop_event.is_set():
                # print("捕捉到停止信号,停止执行")
                return 
            self.to_send(i)


    def run(self,l3,l2,l5,l13):
        if self.filepath.endswith('.pcap')  or self.filepath.endswith('.pcapng'):
            l3.insert('end', "开始读取数据包..\n")
            self.original_packets = rdpcap(fr'{self.filepath}')
        else:
            l3.insert('end', "开始读取目录..\n")
            self.original_packets = []
            file_list = os.listdir(self.filepath)
            pcap_files = [os.path.join(self.filepath, f) for f in file_list if f.endswith('.pcap')  or f.endswith('.pcapng')]
            for i in pcap_files:
                self.original_packets.extend(rdpcap(i))

        self.last_time = self.original_packets[0].time  
        l3.insert('end', "开始计算HASH..\n")
        self.get_hashdict()

        
        self.l13 = l13 # 进度条
        l3.insert('end', '开始发送流量..' + '\n')
        if self.count == 1000000:
            self.total_number = "无限循环" # 需要发送的总包数
            self.l13.start()
        else:            
            self.total_number = self.count*len(self.original_packets) # 需要发送的总包数
            self.once_step = float(100/self.total_number) # 每次发送后进度条的步长
        l3.insert('end', '需要发送的总包数：'+ str(self.total_number) + '\n')
        s=time.time()
        try:
            for _ in range(self.count):
                if self.stop_event.is_set():
                    l3.insert('end', "捕捉到停止信号,停止执行\n")
                    break
                if (not self.srcip_mode) and  (not self.dstip_mode) and (not self.srcport_mode) and  (not self.dstport_mode) and (not self.srcmac_mode) and (not self.dstmac_mode):
                    # 不需要修改直接发送
                    print("不需要修改直接发送")
                    self.not_to_change()
                else:
                    # 需要修改后再发送
                    print("需要修改后再发送")
                    self.to_change(self.n, self.srcip_mode, self.dstip_mode, self.srcport_mode, self.dstport_mode,self.srcmac_mode, self.dstmac_mode)
                    self.n += 1
        except Exception as e:
            l3.insert('end', "发包异常\n")
            l3.insert('end', str(e) + '\n')
            if "文件名、目录名或卷标语法不正确" in str(e):
                l3.insert('end', "请检查网卡名\n")
        l3.insert('end', self.not_to_modify + '\n')
        l3.insert('end', "执行完毕\n")
        l3.insert('end', "实际发送包数"+str(self.send_num)+"\n")
        l3.insert('end', '运行时间:'+str(time.time() - s) + '\n')
        l2.config(state='')
        l5.config(state='')
        self.l13.stop()



