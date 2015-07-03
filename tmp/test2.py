#coding:utf-8
import commands

code,result = commands.getstatusoutput('/usr/local/shellinabox/bin/shellinabox -u shellinabox -g shellinabox -b -c /var/lib/shellinabox -p %s -s /:SSH:%s' % (port,i))
print code,result