from scapy.all import rdpcap
import time
import hashlib
import asyncio

finalresult=''
async def read_pcap2(file_path):
    loop=asyncio.get_event_loop()
    future=loop.run_in_executor(None,rdpcap,file_path)
    return await future,file_path


def invert_dic(packets):
    dic,n={},1
    for i in packets:
        ha=hashlib.md5()
        ha.update(bytes(i))
        dic[ha.hexdigest()]=n
        n+=1
    return dic

def wirte_result2():
    with open( str(time.time()) + '.txt', 'w',encoding='utf8') as f:
        f.write(finalresult)


def check_packet(dic1,dic2,file_name1,file_name2,l):
    global finalresult
    file_name1=file_name1.split('/')[-1]
    file_name2=file_name2.split('/')[-1]
    aa=[dic1[i] for i in dic1 if not dic2.get(i)]
    finalresult+=f"{file_name1}中存在，{file_name2}不存在的数据包序号有"+str(aa)+'\n'
    l.insert('end',f"{file_name1}中存在，{file_name2}不存在的数据包序号有"+str(aa)+'\n')
    # print(f"\033[0;36m{file_name1}\033[0m中存在，\033[0;36m{file_name2}\033[0m不存在的数据包序号有",end='')
    # print(f"\033[0;33m{aa}\033[0m")
    # print('\n')




def start_run(file1,file2,l,l5,l6):
    global finalresult
    finalresult=''
    l6.config(state='disable')
    s=time.time()
    l.insert('end', '正在读取pcap文件' + '\n')
    # print('开始读取pcap文件')
    result=asyncio.run(asyncio.wait([read_pcap2(file1),
                                read_pcap2(file2)]))
    l.insert('end', '读取用时：'+str(time.time()-s)+"s" + '\n')
    # print('用时：',time.time()-s,"s")
    s=time.time()
    l.insert('end', '正在对比pcap文件' + '\n')
    done=result[0]
    result_list=[i.result() for i in done]
    dict_list=[invert_dic(i[0]) for i in result_list]
    file_names_list=[i[1] for i in result_list]
    check_packet(dict_list[0],dict_list[1],file_names_list[0],file_names_list[1],l)
    check_packet(dict_list[1],dict_list[0],file_names_list[1],file_names_list[0],l)
    l.insert('end', '对比用时：'+str(time.time()-s)+"s" + '\n')
    l5.stop()
    l6.config(state='')





if __name__ == '__main__':
    ...
    start_run(*['C:/Users/Admin/Desktop/ftp1.pcap', 'C:/Users/Admin/Desktop/ftp2.pcap'],1)

