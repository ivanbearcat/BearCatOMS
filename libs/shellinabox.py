#!/usr/bin/env python
#coding:utf-8
import os,socket

class open_web_shell(object):

    port_pool = range(20001,20004)

    def open(self,ip_list):
        for i in ip_list:
            port = self.port_pool.pop(0)
            self.port_pool.append(port)
            if self.port_test(i,port):
                if os.system('netstat -natp|grep shellinabox|grep %s' % port):
                    os.system('''kill `netstat -natp|grep shellinabox|grep 10000|awk '{print $7}'|awk -F'/' '{print $1}'`''')
                code,result = os.system('/usr/local/shellinabox/bin/shellinaboxd -u shellinabox -g shellinabox -b -c /var/lib/shellinabox -p %s -s /:SSH:%s' % (port,i))
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