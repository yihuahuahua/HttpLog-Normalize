
import os
import sys
import csv
import time
import datetime
from lib.AccessLogClass import AccessLogClass
from lib.AttackLogClass import AttackLogClass

def timechange(time1, time2, prefix_name, suffix_name = ".txt"):
    # 判断日期是否合法
    try:
        time.strptime(time1, "%Y-%m-%d")
        time.strptime(time2, "%Y-%m-%d")
    except:
        print(f"The input is Error in \"timechange\" about {time1} !!!")
        exit(1)

    if time.strptime(time1, "%Y-%m-%d").tm_mon > time.strptime(time2, "%Y-%m-%d").tm_mon:
        print(f"Error!!! The First time is bigger than Second Time")
        exit(1)
    elif time.strptime(time1, "%Y-%m-%d").tm_mon == time.strptime(time2, "%Y-%m-%d").tm_mon:
        if time.strptime(time1, "%Y-%m-%d").tm_mday > time.strptime(time2, "%Y-%m-%d").tm_mday:
            print(f"Error!!! The First time is bigger than Second Time")
            exit(1)

    dates = []
    dt = datetime.datetime.strptime(time1, "%Y-%m-%d")
    date = time1[:]
    while date <= time2:
        path = prefix_name + "localhost_access_log." + date + suffix_name
        if os.path.exists(path):
            dates.append(path)
        else:
            open(path, 'w', newline='')
            print(f"The path is create in function 'timechange' '{path}'")
            dates.append(path)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

# 将一个txt格式的日志转换为一个csv格式的日志
def onefile_txt_to_csv(infile_path, outfile_path):
    result_csv = open(outfile_path, 'w', newline='')
    writer = csv.writer(result_csv)
    writer.writerow(["Safe", "IP", "Times", "Request_method", "Request_resource", "Request_protocol", "Status", "Bytes",
                     "URL", "Label"])
    with open(infile_path) as f:
        data = f.readlines()
        for line in data:
            if line[0] == '\"':
                line = line[1:len(line)-2]
            else:
                line = line[0:len(line)-1]
            log_elements = line.split(" ", 10)
            log_url_label = log_elements[10].split("\" \"", 1)
            writer.writerow([0, log_elements[0], log_elements[3][1:], log_elements[5][1:], log_elements[6],
                             log_elements[7][0:len(log_elements[7])-1], log_elements[8], log_elements[9],
                             log_url_label[0][1:], log_url_label[1][0:len(log_url_label[1])-1]])

def log_txt_to_csv(time1, time2, infile_way, outfile_way):
    # 根据相应的目录和时间，转换为对应的文件路径组
    load_path = timechange(time1, time2, infile_way)
    output_path = timechange(time1, time2, outfile_way, ".csv")
    # 一对一转换
    for infile, outfile in zip(load_path, output_path):
        onefile_txt_to_csv(infile, outfile)

def log_csv_to_onefile_csv(time1, time2, infile_way, outfile_way, way = "None"):
    if way == "None":
        load_paths = timechange(time1, time2, infile_way, ".csv")
        output_path = outfile_way + "localhost_access_log." + time1 + "-" + time2 + ".csv"
    else:
        load_paths = []
        list = os.listdir(infile_way)
        for dir1 in list:
            load_paths.append(os.path.join(infile_way, dir1))
        output_path = outfile_way
    result_csv = open(output_path, 'w', newline='')
    writer = csv.writer(result_csv)
    writer.writerow(["Safe", "IP", "Times", "Request_method", "Request_resource", "Request_protocol", "Status", "Bytes",
                     "Url", "Label"])
    A = AccessLogClass()
    for load_path in load_paths:
        print("\" ",load_path, " \" is reading.")
        A.set_path_csv(load_path)
        A.load_logs()
        for row in A.log_data:
            writer.writerow(row)
        A.clear()

def merge_csv_log(time1, time2, infile_way, outfile_way):
    log_csv_to_onefile_csv(time1, time2, infile_way, outfile_way)

def onefile_csv_to_sortip_csv(infile_way, outfile_way):
    load_path = infile_way
    output_path = outfile_way[:-4] + "sortip.csv"
    result_csv = open(output_path, 'w', newline='')
    writer = csv.writer(result_csv)
    writer.writerow(["Safe", "IP", "Times", "Request_method", "Request_resource", "Request_protocol", "Status", "Bytes",
                     "Url", "Label"])
    A = AccessLogClass()
    A.set_path_csv(load_path)
    A.load_logs()
    A.analysis_ip()
    for k, v in A.ip_data.items():
        for i in v:
            writer.writerow(A.log_data[i])
    A.clear()

def sort_csv_log(infile_way, outfile_way):
    files = os.listdir(infile_way)
    for file in files:
        infile_path = infile_way + file
        outfile_path = outfile_way + file
        onefile_csv_to_sortip_csv(infile_path, outfile_path)

def wash_log_usrful(request_resource):
    if ((request_resource[-4:] == ".css") or (request_resource[-4:] == ".png") or (request_resource[-3:] == ".js") or
        (request_resource[-4:] == ".gif") or (request_resource[-4:] == ".jpg") or (request_resource[-4:] == ".ico") or
        (request_resource == "\\") or (request_resource == "/loadjs.htm") or (request_resource == "/image.jsp")):
        return 0
    return 1

def wash_log_GET(request_method):
    if request_method == "GET":
        return 1
    return 0

spider_data = []
with open("../log/spider_log/spider_log.txt") as f:
    spider_data = f.readlines()
def wash_log_nospider(label):
    for ii in spider_data:
        if label in ii or ii[:-1] in label:
            return 0
    return 1

def wash_log_200(status):
    if status == "-":
        return 0
    if int(status) > 299:
        return 0
    return 1

def wash_onelog(infile_path, outfile_path):
    # 写入 csv 之前的一些必要操作
    result_csv = open(outfile_path, 'w', newline='')
    writer = csv.writer(result_csv)
    # 向 csv 写入表头
    writer.writerow(["Safe", "IP", "Times", "Request_method", "Request_resource", "Request_protocol", "Status", "Bytes",
                     "Url", "Label"])
    with open(infile_path, 'r') as f:
        # 读取初始数据并输出
        # 将 csv 不支持的字符进行转换
        reader = csv.reader(_.replace('\x00', '') for _ in f)
        result = list(reader)

        for row in result[1:]:
            if (wash_log_GET(row[3])) and (wash_log_usrful(row[4])) and (wash_log_200(row[6])) and \
                (wash_log_nospider(row[9])):
                writer.writerow(row)
    result_csv.close()

def wash_log(time1, time2, infile_way, outfile_way):
    load_path = timechange(time1, time2, infile_way, ".csv")
    output_path = timechange(time1, time2, outfile_way, ".csv")
    # 一对一转换
    for infile, outfile in zip(load_path, output_path):
        wash_onelog(infile, outfile)

def get_attack_methods():
    attack_methods = {}
    with open("../log/txt_attack_methods_log/attack_method.txt", 'r', encoding='UTF-8') as f:
        methods = f.readlines()
        methodnum = 0
        for method in methods:
            #print(method)
            methodnum = methodnum + 1
            attack_methods[method[:-1]] = methodnum
    return attack_methods

def oneatkfile_csv_to_sortip_csv(infile_way, outfile_way):
    loadpath = infile_way
    outputpath = outfile_way[:-4] + "ip.csv"
    result_csv = open(outputpath, 'w', newline='')
    writer = csv.writer(result_csv)
    writer.writerow(["Attack_method", "IP", "Times", "URL", "Status"])
    A = AttackLogClass()
    A.get_path_csv(loadpath)
    A.loadlogs()
    A.analysis_ip()
    for k, v in A.ip_data.items():
        for i in v:
            writer.writerow(A.log_data[i])
    A.clear()

# 将标签文件转换为 csv 格式
def onewaflog_txt_to_csv(infile_path, outfile_path):
    # 获取攻击方法表 dict
    attack_methods = get_attack_methods()
    # 写入 csv 之前的一些必要操作
    result_csv = open(outfile_path, 'w', newline='')
    writer = csv.writer(result_csv)
    # 向 csv 写入表头
    writer.writerow(["Attack_method", "IP", "Times", "URL", "Status"])
    with open(infile_path, encoding='utf-8') as f:
        data = f.readlines()
        for row in data:
            # 将数据按照制表符分割
            row_elements = row.split("\t")
            # 将时间格式转化为 accesslog 格式
            timeArray = time.strptime(row_elements[4], "%Y-%m-%d %H:%M:%S")
            row_elements[4] = time.strftime("%d/%b/%Y:%H:%M:%S", timeArray)
            # 去掉URL中的转义字符
            row_elements[3] = row_elements[3].replace('amp;', '')
            # 写入相关数据
            writer.writerow([attack_methods[row_elements[1]], row_elements[2],
                             row_elements[4], row_elements[3], row_elements[5]])
    result_csv.close()

def waflog_txt_to_csv(infile_way, outfile_way):
    files = os.listdir(infile_way)
    for file in files:
        infile_path = infile_way + file
        outfile_path = outfile_way + file[:-4] + '.csv'
        onewaflog_txt_to_csv(infile_path, outfile_path)

def waflog_csv_to_sortip_csv(infile_way, outfile_way):
    files = os.listdir(infile_way)
    for file in files:
        infile_path = infile_way + file
        outfile_path = outfile_way + file[:-4] + '.csv'
        oneatkfile_csv_to_sortip_csv(infile_path, outfile_path)