import sys
sys.path.append('../')
from core.coreApi import *


if __name__ == '__main__':

    #将一些 txt 格式的日志转换为 csv 格式的日志， 并剔除一些不重要的信息
    #log_txt_to_csv("2018-04-27", "2018-04-30", "../../log/txt_base_log/", "../../log/csv_base_log/")
    #将一些 csv 格式的日志转为一个日志，并根据 ip 排列
    #ip_classification("2018-04-27", "2018-04-30", "../../log/csv_base_log/", "../../log/csv_sortip_log/")
    #清洗日志
    wash_log("2018-04-27", "2018-04-30", "../../log/csv_base_log/", "../../log/csv_wash_log/")