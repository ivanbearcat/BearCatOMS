#!/usr/bin/env python
#coding:utf-8
import MySQLdb,sys,os
from libs.server_list_conf import server_lists

username = sys.argv[1]
server_groups = []
all_servers = []
try:
    conn=MySQLdb.connect(host='192.168.100.151',user='BearCat',passwd='xzm_123.',db='BearCatOMS',port=3306,charset="utf8")
    cur=conn.cursor()
    cur.execute('select server_groups from user_manage_perm where username="%s"' % username)
    data = cur.fetchall()
    for i in data:
        for j in i:
            for n in j.split(','):
                server_groups.append(n)
    for i in server_groups:
        cur.execute('select members_server from operation_server_group_list where server_group_name="%s"' % i)
        data = cur.fetchall()
        for j in  data:
            for n in j:
                for m in n.split(','):
                    all_servers.append(m)
    print all_servers
    conn.commit()
    cur.close()
    conn.close()
except Exception,e:
    print e
    sys.exit(1)

while 1:
    try:
        print '=================='
        for i in all_servers:
            print i
        print '=================='

        hostname = raw_input('please input hostname to login("exit" to logout)：').strip()
	if hostname == 'exit':
	    sys.exit(0)
        if hostname == '' or hostname not in all_servers:
            print '主机名不正确'
            continue
        os.system('python libs/audit_server/audit_shell.py %s %s' % (server_lists[hostname],hostname))
    except Exception:
        continue
    except KeyboardInterrupt:
	continue
