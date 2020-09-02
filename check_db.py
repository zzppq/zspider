#!-*-coding:utf8-*-
import os
import sys
import argparse
import pymysql as mdb

HAVE_NAME = 0
HAVE_URL = 0
ALL_NO = 1
NO_ARGS = 3

class ConnDb():
    def openclose(func):
        def connectdb(self,sql=None):
            conn = mdb.connect(host='192.168.1.251',port=3306,user='root',passwd='123456',db='projects_urls',charset='utf8')
            cur = conn.cursor()
            try:
                cur.execute(func(self,sql))
                conn.commit()
                rlists = cur.fetchall()
            except Exception as e:
                conn.rollback()
                print 'exec ' + str(func) + 'error:' + str(e)
            finally:
                cur.close()
                conn.close()
            try:
                return rlists
            except:
                print('no results !')
        return connectdb

    @openclose
    def runsql(self,sql=None):
        return sql

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--proname',type=str,help="Project name.")
parser.add_argument('--prourl',type=str,help="Project url.")
args = parser.parse_args()

project_name = args.proname
project_url = args.prourl

if project_name is None or project_url is None:
    parser.print_usage()
    sys.exit(NO_ARGS)

def main():
    mydb = ConnDb()

    sql_search_name = "select * from projects_urls_info where project_name = '%s'"%(project_name)
    sql_search_url = "select * from projects_urls_info where project_url = '%s'"%(project_url)
    if len(mydb.runsql(sql_search_url)) > 0:
        return HAVE_URL
    elif len(mydb.runsql(sql_search_name)) > 0:
        return HAVE_NAME
    else:
        insert_commond = "insert into projects_urls_info (project_name, project_url) values ('%s','%s')"%(project_name,project_url)
        mydb.runsql(insert_commond)
        return ALL_NO

if __name__ == "__main__":
    ret_num = main()
    if ret_num == 0:
        print "%s has download!"%project_name
    sys.exit(ret_num
