import csv

class AccessLogClass(object):
    def __init__(self):
        self.log_path = "-"         # 待处理的日志路径
        self.log_data = []          # 日志数据
        self.ip_dict = {}           # 存储 ip 字典
        self.ip_data = {}           # 存储 ip 索引

    # 设置文件路径
    def set_path_csv(self, infile_path):
        self.log_path = infile_path

    # 加载文件数据
    def load_logs(self):
        with open(self.log_path, 'r') as f:
            reader = csv.reader(_.replace('\x00', '') for _ in f)
            self.log_data = list(reader)
            self.log_data = self.log_data[1:]

    # 统计 ip 数据
    def analysis_ip(self):
        log_num = -1
        for row in self.log_data:
            log_num = log_num + 1;
            self.ip_dict[row[1]] = self.ip_dict.get(row[1], 0) + 1
            if(self.ip_data.get(row[1], 0) == 0):
                self.ip_data[row[1]] = self.ip_data.get(row[1], [])
            self.ip_data[row[1]].append(log_num)

    # 释放内存
    def clear(self):
        self.log_path = "-"
        self.log_data.clear()
        self.ip_dict.clear()



