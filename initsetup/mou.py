import wmi
import configparser
import globals
import re
import serial
import time
import pythoncom
import os
import pywinusb.hid as hid
import ctypes
from ctypes import wintypes
def  getmousenumber():

# 查询鼠标设备
    mouse_devices = globals.gwmihead.Win32_PointingDevice()
    return len(mouse_devices)
'''
for device in mouse_devices:
    # 获取厂商名字、PID和VID
    manufacturer = device.Manufacturer
    pnp_id_parts = device.PNPDeviceID
    device_name = device.Name
    # 获取其他属性
    device_id = device.DeviceID
    description = device.Description
    status = device.Status
    device_name2 = device.Caption  # 获取真正的鼠标名字
    print("manufacturer:", manufacturer)
    print("device_name2:", device_name2)
    print("device_name:", device_name)
    print("pnp_id_parts:", pnp_id_parts)
    print("device_id:", device_id)
    print("description:", description)
    print("status:", status)
    print()'''
def write_vid_pid(vid_value, pid_value):
    # 创建配置解析器对象
    config = configparser.ConfigParser()
    
    # 读取配置文件
    config.read(globals.gfileinit)

    # 检查是否存在 'section'，如果不存在则创建
    if not config.has_section('section'):
        config.add_section('section')

    # 写入 vid 和 pid 值
    config.set('section', 'vid', vid_value)
    config.set('section', 'pid', pid_value)

    # 写回到配置文件
    with open(globals.gfileinit, 'w') as configfile:
        config.write(configfile)

def checkmouseisok():
    print(globals.gfileinit)
    if os.path.exists(globals.gfileinit)==False:
        return False

    config = configparser.ConfigParser()
    config.read(globals.gfileinit)

    # 读取特定配置项的值
    vid_value = config.get('section', 'vid')
    pid_value = config.get('section', 'pid')
    # 连接到WMI服务
    c = wmi.WMI()
# 查询鼠标设备
    matching_devices_count=0
    mouse_devices = c.Win32_PointingDevice()
    print('@@@@@@@@@@@')
    for device in mouse_devices:
        # 获取厂商名字、PID和VID
        manufacturer = device.Manufacturer
        pnp_id_parts = device.PNPDeviceID
        device_name = device.Name
        # 获取其他属性
        device_id = device.DeviceID
        description = device.Description
        status = device.Status
        device_name2 = device.Caption  # 获取真正的鼠标名字
        print("manufacturer:", manufacturer)
        print("device_name2:", device_name2)
        print("device_name:", device_name)
        print("pnp_id_parts:", pnp_id_parts)
        print("device_id:", device_id)
        print("description:", description)
        print("status:", status)
        print()
        # 使用正则表达式匹配 VID 和 PID
        matches = re.search(r'VID_([A-F0-9]+)&PID_([A-F0-9]+)', pnp_id_parts, re.IGNORECASE)

        if matches:
            vid = matches.group(1)
            pid = matches.group(2)
            print("VID:", vid)
            print("PID:", pid)

             # 检查设备的 VID 和 PID 是否与 INI 文件中的匹配
            if vid_value == vid and pid_value ==pid:
                matching_devices_count += 1
        else:
            print("Unable to extract VID and PID.")
    return (matching_devices_count>1)

def getcomdevice():
    comname=""
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc}")

        if "Arduino" in desc:
            comname=port
            break
    if comname!="":
        return True,comname,1
    
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc}")

        if "USB 串行设备" in desc:
            comname=port
            break
    if comname!="":
        return True,comname,2
    return False,"",0

def get_value_within_seven_seconds():
    start_time = time.time()
    end_time = start_time + 7  # 终止时间为起始时间加7秒
    time.sleep(0.3)
    while time.time() < end_time:
        isp,value,ctye = getcomdevice()  # 获取值的函数，需要根据实际情况替换
        #if isp==True and ctye==1:
        if isp==True:
            return isp,value,1 
       
        time.sleep(0.3)  # 每隔1秒继续尝试获取值
    
    return False,'',0  # 在七秒钟内未能获取到值，返回None

def restecom(port):
    try:
        if  globals.garduino is not None:
            globals.garduino.close()
    except serial.SerialException as e:
        print(f"duino.close(){e}")
    baud_rate = 1200  # 波特率
    timeout = 1  # 超时时间（秒）
    # 初始化串口
    ret=0
    ser = None  # 初始化 ser 变量
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        # 发送重置命令
        ser.setDTR(False)  # 先拉低DTR
        time.sleep(0.1)  # 等待一段时间
        ser.setDTR(True)  # 再拉高DTR
        # 等待重置完成
        time.sleep(3)  # 这里可以根据实际情况调整等待时间
        print("重置完成")
        
    except serial.SerialException as e:
        print(f"串口通信错误：{e}")
        ret=1
    finally:
        # 关闭串口连接
                # 关闭串口连接，确保 ser 变量已定义
        if ser is not None:
            ser.close()
    return ret




def get_mouse_device_map():
    device_map = {}
    all_devices = hid.HidDeviceFilter().get_devices()
    for device in all_devices:
        vid = hex(device.vendor_id)[2:].upper()
        pid = hex(device.product_id)[2:].upper()
        key = f"{vid}-{pid}"
        value = device.product_name
        if key not in device_map:
            device_map[key] = value
    return device_map

def get_device_name_by_key(key):
    if globals.gmousemap is not None and key in globals.gmousemap:
        return globals.gmousemap[key]
    return None


def get_mouse_sensitivity():
    user32 = ctypes.windll.user32
    SPI_GETMOUSESPEED = 0x0070  # 获取鼠标速度的参数值
    speed = ctypes.c_int()
    
    # 调用SystemParametersInfo函数获取鼠标速度
    user32.SystemParametersInfoW(SPI_GETMOUSESPEED, 0, ctypes.byref(speed), 0)
    
    # 根据获取到的值计算灵敏度
    sensitivity = (speed.value + 1) / 10.0
    
    return sensitivity

