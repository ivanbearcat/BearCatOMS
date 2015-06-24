#coding=utf-8
from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet import threads
# from twisted.protocols.basic import LineReceiver
from conf.config import factory,server
# from libs.log import logger
import time,os
from twisted.internet import reactor
# from lib.data_analysis import ProtoControl
# from lib.c_include import *
# from orm.factorywork import server_info_save, load_history_online, workRegos, workLostClient,query_device, check_online
# from conf.epconfig import EPConfig, MServerConfig,ZS_SERVER


# from zope.interface import implements
# from twisted.cred import portal, checkers
# from twisted.python import filepath
# from twisted.protocols import ftp
# from twisted.internet import task
# from monitorthread import monitor_thread_start, monitor_job_put
# import thread
# from monitor.thread_pool import thread_pool_start


class server_protocol(Protocol):

    def __init__(self):
        self.recvBuf = ""
        self.online_num = {}
        self.oid = None

    def connectionMade(self):
        """
        #第一次连接时需要做的事情
        发送数据
        act:行为，告诉cm需要做什么
        1. 登入服务器
        """
        ip = self.transport.getPeer().host
        if not ip in server['allow']:
            """
            禁IP
            """
            self.transport.write('The IP (%s) not allow' % ip)
            self.transport.loseConnection()
            # logger.info('The IP (%s) not allow' % ip)
        # else:
        #     self.factory.clientips.append(ip)
        #     self.factory.client_map[ip] = self
            # logger.info('Client connect %s' % ip)


    # def sendDataNoProtaol(self, data):
    #     """
    #     数据发送不处理
    #     """
    #     logger.debug('发送数据(%s)' % len(data))
    #     # outdata = data_analysis.sendData(callid, data)
    #     outdata = data
    #     self.transport.write(outdata)
    #
    # def sendData(self, data):
    #     """
    #     数据协议封包处理后发送
    #     """
    #
    #     s = data.get('act',None)
    #     if s == "heartbeat" or s == "graph_view":
    #         pass
    #     else:
    #         # logger.debug(data)
    #     data = ProtoControl.sendData(data)
    #     self.transport.write(data)

    # def sendError(self, m):
    #     msg = {"code":2,"msg":m ,"act":"sendError"}
    #     self.sendData(msg)
    #     self.transport.loseConnection()

    def dataReceived(self, data):

        def in_func(self ,data):
            self.recvBuf += data
            while len(self.recvBuf):
                try:
                    self.transport.write('data')
                except Exception, e:
                    print e
        threads.deferToThread(in_func,self,data)



    def connectionLost(self, reason):
        # try:
        #     os.remove(EPConfig['PID_FILE'])
        # except OSError, e:
        #     logger.info("Not find pid file")
        print self.transport.client, 'disconnected'
        # logger.info("---Client--connectionLost===>%s" % reason)



    # def InvokeAction(self,data):
    #     """
    #     命令调度
    #     """
    #     act = data.get('act')
    #
    #     if act == 'regos':
    #         #注册处理
    #         self.oid = data['oid']
    #         self.factory.addClient(self, data)
    #         self.factory.execRego(data)
    #
    #     elif act == 'heartbeat':
    #         #心跳处理
    #         self.factory.addClient(self, data)
    #         self.factory.execHeartBeat(data)



# class EPClientFactory(ClientFactory):
#     protocol = EPProtocolGame
#     clientips = []
#     def clientConnectionLost(self, connector, reason):
#         logger.debug('connection lost:%s' % reason.getErrorMessage())
#         logger.debug("10s later reconnect")
#         reactor.callLater(10, connector.connect)
#
#
#     def clientConnectionFailed(self, connector, reason):
#         logger.debug('connection failed:%s' % reason.getErrorMessage())
#         logger.debug("10s later reconnect")
#         reactor.callLater(10, connector.connect)


class server_factory(Factory):
    protocol = server_protocol
    #本系统最大允许10000人同时在线
    max_connections = factory['max_connections']
    timeout = factory['timeout']
    perdefer = factory['perdefer'] #每个进程运行的子线程数

    def __init__(self):
        pass
