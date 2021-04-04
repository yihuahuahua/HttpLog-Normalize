

class LogClass(object):

    def __init__(self):
        self.ip = "0.0.0.0"
        self.times = "-"
        self.request_method = "null"    # HTTP请求方法
        self.request_resource = "null"  # HTTP请求资源
        self.request_protocol = "null"  # HTTP请求协议
        self.status = 0                 # 返回的状态码
        self.bytes = 0                  # 传输的数据量
        self.url = "-"                  # 上一个页面
        self.label = "-"                # 浏览器标识

    def getIp(self):
        return self.ip

    def getTimes(self):
        return self.times

    def getRequestMethod(self):
        return self.request_method

    def getRequestResource(self):
        return self.request_resource

    def getRequestProtocol(self):
        return self.request_protocol

    def getStatus(self):
        return self.status

    def getBytes(self):
        return self.bytes

    def getUrl(self):
        return self.getUrl

    def getLabel(self):
        return self.label