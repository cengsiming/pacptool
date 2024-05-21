from multiping import MultiPing
import ipaddress
import asyncio



class MMMping():
    def __init__(self,input_Hosts,input_Port,l2,l3):
        self.input_Hosts = input_Hosts
        self.input_Port = input_Port
        self.l2 = l2
        self.l3 = l3
        self.Hostlist = []

    #添加ip到Hostlist,输入示例：192.168.1.1;172.17.18.50-172.17.18.51;10.0.0.8/30
    def formatHost(self):
        try:
            for input_Host in self.input_Hosts:
                if '-' in input_Host:
                    # 如果输入包含 "-"，则认为是 IP 段
                    start_ip, end_ip = input_Host.split('-')
                    start = ipaddress.IPv4Address(start_ip)
                    end = ipaddress.IPv4Address(end_ip)
                    for ip_int in range(int(start), int(end) + 1):
                        self.Hostlist.append(str(ipaddress.IPv4Address(ip_int)))
                elif '/' in input_Host:
                    # 如果输入包含 "/"，则认为是 IP+掩码
                    ip_network = ipaddress.ip_network(input_Host, strict=False)
                    for ip in ip_network:
                        self.Hostlist.append(str(ip))
                        
                else:
                    # 单独地址，直接添加到hosts列表
                    self.Hostlist.append(input_Host)
            self.checklink2()
        except Exception as e: 
            self.l3.insert('end',str(e)+'\n')
            return        

    def checklink2(self):
        if 65536>len(self.Hostlist)>0:
            self.l3.insert('end','Host:'+str(len(self.Hostlist))+'\n')
        else:
            self.l3.insert('end','请检查输入 扫描主机不能超过65535个'+'\n')
            self.l2.config(state='')
            return
        self.l3.insert('end','扫描中..:'+'\n')
        mp = MultiPing(self.Hostlist)
        mp.send()
        responses, _ = mp.receive(1)
        self.l3.insert('end','>>>>>>>>>>>>>>>>>>'+'\n')
        self.l3.insert('end','存活主机'+'\n')
        for i in responses:
            self.l3.insert('end',i+'\n')
        self.l3.insert('end','>>>>>>>>>>>>>>>>>>'+'\n')
        ports = self.convert_to_ports(self.input_Port)
        if not ports:
            self.l2.config(state='')
            self.l3.insert('end','done!'+'\n')
            return
        self.l3.insert('end','开放端口'+'\n')
        
        asyncio.run(self.main(responses,ports))
            
            
        self.l2.config(state='')
        self.l3.insert('end','done!'+'\n')
    def convert_to_ports(self,input_str):
        if not input_str:
            self.l3.insert('end','不扫描端口'+'\n')
            return []
        try:
            input_list = input_str.split(',')  # 按逗号分隔字符串，得到列表
            ports = []
            for item in input_list:
                if '-' in item:
                    start_port, end_port = item.split('-')
                    start_port = int(start_port)
                    end_port = int(end_port)
                    ports.extend([port  for port in range(start_port, end_port + 1)])
                else:
                    port = int(item)
                    ports.append(port)
            return ports
        except Exception as e:
            self.l3.insert('end','port输入错误'+str(e)+'\n')
            return []    
        
    async def portscanner(self,host, port,semaphore):
        try:
            if port > 65535 or port <= 0:
                return
            async with semaphore:
                _, writer = await asyncio.open_connection(host, port)
                self.l3.insert('end',f"{host}:{port} open"+'\n')
                writer.close()
        except:
            pass
    async def main(self,responses, ports):
        if not ports:
            return 
        semaphore = asyncio.Semaphore(10000)
        for ip in responses:
            tasks = [self.portscanner(ip, port, semaphore) for port in ports]
            await asyncio.gather(*tasks)
            self.l3.insert('end',ip+"扫描完成"+'\n')

if __name__ == '__main__':
    xx = MMMping(["10.0.0.101","10.0.0.200"],[22,33,6666,65432])
    xx.formatHost()
