from core.coreApi import *

'''
将一些 txt格式日志转换为 csv格式，并剔除不重要的信息
'''
def log_txt_to_csv(time1, time2, infile_way, outfile_way):
    # 根据目录和时间，转换为对应的文件路径组
    load_path = timechange(time1, time2, infile_way)
    output_path = timechange(time1, time2, outfile_way, ".csv")
    # 一对一转换
    for infile, outfile in zip(load_path, output_path):
        onefile_txt_to_csv(infile, outfile)