#!/usr/bin/env python
#coding:utf-8
import MySQLdb,sys,os
import server_list

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
        for i in all_servers:
            print i
        hostname = raw_input('请输入要登录的主机名：')
        if hostname == '' or hostname not in all_servers:continue
        os.system('python audit_shell.py %s %s' % (hostname,server_list[hostname]))
    except Exception:
        continue