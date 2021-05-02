from core.coreApi import *
import shutil
import datetime

def setLabel():
    # 开始预处理标签日志
    waflog_txt_to_csv("../log/txt_base_attack_label_log/", "../log/csv_base_attack_label_log/")
    waflog_csv_to_sortip_csv("../log/csv_base_attack_label_log/", "../log/csv_sortip_attack_label_log/")


def mainFun(time1, time2):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(str(nowTime) + "：开始预处理 " + time1 + " 到 " + time2 + " 的日志......")

    # 将txt格式的日志转换为csv格式的日志
    print("---------当前任务1：将txt格式日志转化为csv格式日志-------------------------")
    log_txt_to_csv(time1, time2, "../log/txt_base_log/", "../log/csv_base_log/")
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(str(nowTime) + "：任务1完成！日志保存在 /log/csv_base_log/ 目录下......")

    # 对csv日志进行合并
    print("---------当前任务2：合并csv格式日志---------------------------------------")
    merge_csv_log(time1, time2, "../log/csv_base_log/", "../log/csv_base_sum_log/")
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(str(nowTime) + "：任务2完成！日志保存在 /log/csv_base_sum_log/ 目录下......")

    # 对日志按照ip进行排序
    print("---------当前任务3：对合并后的csv格式日志按照ip排序------------------------")
    sort_csv_log("../log/csv_base_sum_log/", "../log/csv_sortip_sum_log/")
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(str(nowTime) + "：任务3完成！日志保存在 /log/csv_sortip_sum_log/ 目录下......")

    # 对日志进行标注
    print("---------当前任务4：对日志进行标注----------------------------------------")
    # 对csv原始日志进行清洗
    # print("---------当前任务3：清洗csv格式日志---------------------------------------")
    # wash_log(time1, time2, "../log/csv_base_log/", "../log/csv_wash_log/")
    # nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(str(nowTime) + "：任务3完成！日志保存在 /log/csv_wash_log/ 目录下......")


def cleanAllLog():
    if os.path.exists("../log/csv_base_log/"):
        shutil.rmtree("../log/csv_base_log/")
    if os.path.exists("../log/csv_base_sum_log/"):
        shutil.rmtree("../log/csv_base_sum_log/")
    if os.path.exists("../log/csv_sortip_sum_log/"):
        shutil.rmtree("../log/csv_sortip_sum_log/")
    os.mkdir("../log/csv_base_log/")
    os.mkdir("../log/csv_base_sum_log/")
    os.mkdir("../log/csv_sortip_sum_log/")
    print("已清除所有生成的日志文件")

if __name__ == '__main__':

    # sort_log("2018-04-23", "2018-04-24", "../log/csv_base_log/", "../log/csv_sortip_log/")
    # cleanAllLog()
    mainFun("2018-04-23", "2018-04-24")
