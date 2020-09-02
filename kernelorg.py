#!-*-coding:utf-8-*-
import os,sys
import urllib
import urllib2
from lxml import etree
from time import sleep

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

def myspider(url,header):
    my_request = urllib2.Request(url,headers=header)
    try_time = 3
    while(try_time):
        try:
            my_response = urllib2.urlopen(my_request,timeout=60)
            break
        except Exception as e:
            sleep((6 - try_time) * 10)
            print('try again !!!!!!!!!!!!!!!!!!!!!!')
            try_time = try_time - 1
    if try_time == 0:
        with open('failurl.txt','a') as fd:
            fd.write(url + '\n')
        return 'mllj'
    my_page = my_response.read()
    return my_page

def mysolve(page,my_data):
    content = etree.HTML(page)
    name_lists = content.xpath('//a')
    new_urls = content.xpath('//a/@href')

    for i in range(len(name_lists)):
        fname = name_lists[i].xpath('string(.)')
        my_data[fname] = new_urls[i]

if __name__ == "__main__":
    base_url = 'https://mirrors.tuna.tsinghua.edu.cn/kernel'
    fir_page = myspider(base_url,header)
    if fir_page == 'mllj':
        print ('fetch index page fail!')
        sys.exit(1)
    fir_dir = {}
    mysolve(fir_page,fir_dir)
    for fkey,fvalue in fir_dir.items():
        if fkey[0] == 'v':
            if fkey[:-1] not in os.listdir('.'):
                os.mkdir(fkey)
            print ('start download %s:'%fkey)
            print ('--------------------------------')
            sec_url = base_url + '/' + fvalue
            sec_page = myspider(sec_url,header)
            if sec_page == 'mllj':
                continue
            sec_dir = {}
            mysolve(sec_page,sec_dir)
            for skey,svalue in sec_dir.items():
                if 'linux' in skey and 'tar.gz' in skey:
                    if skey in os.listdir(fkey):
                        print ('package %s has downloaded!'%skey)
                        continue
                    last_url = sec_url + svalue
                    print ('download package %s:'%skey)
                    print ('****************************************')
                    if os.system('wget -P %s %s'%(fkey,last_url)) != 0:
                        print ('download %s fail!'%skey)
                        with open('failpack.txt','a') as fp:
                            fp.write('%s\n'%last_url)
                    print ('downlaod %s success!'%skey)
                    print ('****************************************')
                    sleep(0.5)
            print ('finsh download %s'%fkey)
            print ('---------------------------------')
            sleep(1)

