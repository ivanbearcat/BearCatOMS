#!/usr/bin/env python
#coding:utf-8
import commands,socket

class open_web_shell(object):

    port_pool = range(20001,20004)

    def open(self,ip_list):
        for i in ip_list:
            port = self.port_pool.pop(0)
            self.port_pool.append(port)
            if self.port_test(i,port):
                code,result = commands.getstatusoutput('/usr/local/shellinabox/bin/shellinabox -u shellinabox -g shellinabox -b -c /var/lib/shellinabox -p %s -s /:SSH:%s' % (port,i))
                return code
            else:
                return 1

    def port_test(self,ip,port):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip,int(port)))
            s.shutdown(2)
            return True
        except:
            return False