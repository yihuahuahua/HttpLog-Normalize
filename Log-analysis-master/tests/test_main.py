from ..core.coreApi import *

if __name__ == '__main__':
    #将一些 txt 格式的日志转换为 csv 根式的日志， 并剔除一些不重要的信息
    log_txt_to_csv("2018-04-23", "2018-04-25", "logs/", "csv_logs/")
