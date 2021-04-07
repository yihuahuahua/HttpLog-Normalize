from ..lib.AccessLogClass import  AccessLogClass
import os
import csv
import time
import datetime


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

def onefile_csv_to_sortip_csv(outfile_way):
    load_path = outfile_way
    output_path = outfile_way[:-4] + "ip.csv"
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

def ip_classification(time1, time2, infile_way, outfile_way):
    # 将多个 csv 格式文件转换为一个 csv 文件
    log_csv_to_onefile_csv(time1, time2, infile_way, outfile_way)
    # 单个 csv 格式文件进行 ip 排序，同 ip 根据时间来排序
    outfile_way = outfile_way + "localhost_access_log." + time1 + "-" + time2 + ".csv"
    onefile_csv_to_sortip_csv(outfile_way)
    print("ip_classification is finished.")