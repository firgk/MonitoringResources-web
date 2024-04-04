import psutil
# import schedule
import time



# 保存上一次的磁盘IO信息
prev_disk_io = {}
def display_system_resources():
    result=''
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    result+=f'CPU 使用率：{cpu_percent}%\n'
    result+=(f'内存使用率：{memory.percent}%\n')
    result+=get_network_speed()
    result+=display_disk_io_speed()
    result+=display_disk_info()
    result+=('-------------')
    return result

def get_network_speed():
    last_net_io = psutil.net_io_counters()
    time.sleep(0.5)
    current_net_io = psutil.net_io_counters()
    sent_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent)*2 / 1024 / 1024  # MB/s
    recv_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv)*2 / 1024 / 1024  # MB/s
    return (f'网络发送速率：{sent_speed:.2f} MB/s  网络接收速率：{recv_speed:.2f} MB/s  \n')

def display_disk_info():
    disks = psutil.disk_partitions(all=False)  # 获取所有磁盘分区
    temp=''
    for disk in disks:
        disk_usage = psutil.disk_usage(disk.mountpoint)  # 获取磁盘使用情况
        # print(f'磁盘：{disk.device}')  # 打印磁盘设备名称
        # print(f'磁盘总量：{round(disk_usage.total / (1024**3), 2)} GB')  # 打印磁盘总量
        # print(f'磁盘使用率：{disk_usage.percent}%')  # 打印磁盘使用率
        temp+=(f'磁盘：{disk.device} 磁盘总量：{round(disk_usage.total / (1024**3), 2)} GB 磁盘使用率：{disk_usage.percent}%\n')
    return temp

def display_disk_io_speed():
    disk_io = psutil.disk_io_counters(perdisk=True)  # 获取磁盘I/O信
    temp=''
    for disk, io in disk_io.items():
        prev_io = prev_disk_io.get(disk, io)  # 获取前一次的I/O信息
        # 计算磁盘读写速率
        read_speed = (io.read_bytes - prev_io.read_bytes) / 1024 / 1024
        write_speed = (io.write_bytes - prev_io.write_bytes) / 1024 / 1024
        prev_disk_io[disk] = io  # 更新prev_disk_io
        temp+=(f'磁盘 {disk.split("Drive")[1]} 读速率：{read_speed:.2f} MB/s  磁盘 {disk.split("Drive")[1]} 写速率：{write_speed:.2f} MB/s  \n')  # 打印磁盘读速率
    return temp

# 每隔0秒展示一次系统资源使用情况
# schedule.every(8).seconds.do(display_system_resources)


# display_system_resources()
# print(display_system_resources())