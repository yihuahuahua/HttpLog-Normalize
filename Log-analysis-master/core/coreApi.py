import os
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