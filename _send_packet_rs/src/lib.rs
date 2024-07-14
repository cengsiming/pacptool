use pcap;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn to_send_packet(file_path: &str, count: i32, iface: &str, mac: bool, ip: bool, port: bool) {
    let buf_vec = read_pcap(file_path);
    let count2: i32;
    if count == 0 {
        count2 = 100000;
    } else {
        count2 = count;
    }
    send_packet(count2, iface, buf_vec, mac, ip, port);
    println!("发送完毕!")
}

fn read_pcap(filepath: &str) -> Vec<Vec<u8>> {
    let mut cap1 = pcap::Capture::from_file(filepath).unwrap();
    let mut buf_vec: Vec<Vec<u8>> = Vec::new(); // 创建一个 Vec<Vec<u8>> 来存储所有包的数据
    while let Ok(packet) = cap1.next_packet() {
        if packet.len() <= 1514 {
            let packet_data: Vec<u8> = packet.data.to_vec(); // 创建一个新的 Vec<u8> 来存储当前包的数据
            buf_vec.push(packet_data); // 将当前包的数据添加到 buf_vec 中
        }
    }
    buf_vec
}

fn send_packet(
    count: i32,
    iface: &str,
    mut buf_vec: Vec<Vec<u8>>,
    mac: bool,
    ip: bool,
    port: bool,
) {
    let mut cap: pcap::Capture<pcap::Active> =
        pcap::Capture::from_device(iface).unwrap().open().unwrap();
    let mut sq = pcap::sendqueue::SendQueue::new(4294967295).unwrap();
    for _ in 0..count {
        for i in buf_vec.iter_mut() {
            if mac {
                // 修改源mac
                i[5] = i[5] % 255 + 1;
                if i[5] == 1 {
                    i[4] = i[4] % 255 + 1;
                    if i[4] == 1 {
                        i[3] = i[3] % 255 + 1;
                        if i[3] == 1 {
                            i[2] = i[2] % 255 + 1;
                            if i[2] == 1 {
                                i[1] = i[1] % 255 + 1;
                                if i[1] == 1 {
                                    i[0] = i[0] % 255 + 1;
                                }
                            }
                        }
                    }
                }
                // 修改目的mac
                i[11] = i[11] % 255 + 1;
                if i[11] == 1 {
                    i[10] = i[10] % 255 + 1;
                    if i[10] == 1 {
                        i[9] = i[9] % 255 + 1;
                        if i[9] == 1 {
                            i[8] = i[8] % 255 + 1;
                            if i[8] == 1 {
                                i[7] = i[7] % 255 + 1;
                                if i[7] == 1 {
                                    i[6] = i[6] % 255 + 1;
                                }
                            }
                        }
                    }
                }
            }
            if i[12] == 8 && i[13] == 0 {
                //判断为IPv4
                if ip {
                    // 修改源IPv4
                    i[29] = i[29] % 255 + 1;
                    if i[29] == 1 {
                        i[28] = i[28] % 255 + 1;
                        if i[28] == 1 {
                            i[27] = i[27] % 255 + 1;
                            if i[27] == 1 {
                                i[26] = i[26] % 255 + 1;
                            }
                        }
                    }
                    // 修改目的IPv4
                    i[33] = i[33] % 255 + 1;
                    if i[33] == 1 {
                        i[32] = i[32] % 255 + 1;
                        if i[32] == 1 {
                            i[31] = i[31] % 255 + 1;
                            if i[31] == 1 {
                                i[30] = i[30] % 255 + 1;
                            }
                        }
                    }
                }
                if port {
                    //修改端口
                    if i[23] == 6 || i[23] == 17 {
                        //修改源端口
                        i[35] = i[35] % 255 + 1;
                        if i[35] == 1 {
                            i[34] = i[34] % 255 + 1;
                        }
                        //修改目的端口
                        i[37] = i[37] % 255 + 1;
                        if i[37] == 1 {
                            i[36] = i[36] % 255 + 1;
                        }
                    }
                }
            } else if i[12] == 8 && i[13] == 6 && ip {
                //判断为ARP
                // 修改源IP
                i[31] = i[31] % 255 + 1;
                if i[31] == 1 {
                    i[30] = i[30] % 255 + 1;
                    if i[30] == 1 {
                        i[29] = i[29] % 255 + 1;
                        if i[29] == 1 {
                            i[28] = i[28] % 255 + 1;
                        }
                    }
                }
                // 修改目的IP
                i[41] = i[41] % 255 + 1;
                if i[41] == 1 {
                    i[40] = i[40] % 255 + 1;
                    if i[40] == 1 {
                        i[39] = i[39] % 255 + 1;
                        if i[39] == 1 {
                            i[38] = i[38] % 255 + 1;
                        }
                    }
                }
            } else if i[12] == 134 && i[13] == 221 {
                // 判断为ipv6
                if ip {
                    // 修改源IPv6
                    i[37] = i[37] % 255 + 1;
                    if i[37] == 1 {
                        i[36] = i[36] % 255 + 1;
                        if i[36] == 1 {
                            i[35] = i[35] % 255 + 1;
                            if i[35] == 1 {
                                i[34] = i[34] % 255 + 1;
                            }
                        }
                    }
                    // 修改目的IPv6
                    i[53] = i[53] % 255 + 1;
                    if i[53] == 1 {
                        i[52] = i[52] % 255 + 1;
                        if i[52] == 1 {
                            i[51] = i[51] % 255 + 1;
                            if i[51] == 1 {
                                i[50] = i[50] % 255 + 1;
                            }
                        }
                    }
                }
                if port {
                    //修改端口
                    if i[20] == 6 || i[20] == 17 {
                        //修改源端口
                        i[55] = i[55] % 255 + 1;
                        if i[55] == 1 {
                            i[54] = i[54] % 255 + 1;
                        }
                        //修改目的端口
                        i[57] = i[57] % 255 + 1;
                        if i[57] == 1 {
                            i[56] = i[56] % 255 + 1;
                        }
                    }
                }
            }
            sq.queue(None, &i).unwrap();
            sq.transmit(&mut cap, pcap::sendqueue::SendSync::Off)
                .unwrap_or_else(|_| println!("发送数据包出错!"));
        }
    }
}

#[pymodule]
fn send_packet_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(to_send_packet, m)?)?;
    Ok(())
}
