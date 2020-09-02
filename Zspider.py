import os, sys, urllib, urllib2
import time
import argparse
from lxml import etree
from time import sleep
from time import ctime
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
url_break = False

dest_src_dir = ''
dest_tmp_dir = ''

def ZSpider(url, header):
    my_request = urllib2.Request(url, headers=header)
    try_time = 3
    while(try_time):
        try:
            my_response = urllib2.urlopen(my_request,timeout=60)
            break
        except Exception as e:
            sleep((6 - try_time) * 10)
            print("try again!!!!!!!!!!!!")
            try_time = try_time - 1
    if try_time == 0:
        with open('failurl.txt','a') as fd:
            fd.write(url + '\n')
        return 'mllj'
    my_page = my_response.read()
    return my_page


def GetTagSolve(page, my_data):
    content = etree.HTML(page)
    url_name = content.xpath('//ul[@class="numbers-summary"]//a[last()]')
    num_name = content.xpath('//ul[@class="numbers-summary"]//a/span')
    new_urls = content.xpath('//ul[@class="numbers-summary"]//a/@href')
    for i in range(len(num_name)):
        fname = url_name[i].xpath('string(.)').strip().split(' ')[(-1)]
        fnum = num_name[i].xpath('string(.)')
        my_data[fname] = fnum.strip()


def GetTagNum(each_url):
    each_page = ZSpider(each_url, header)
    if each_page == 'mllj':
        return 0
    z_data = {}
    GetTagSolve(each_page, z_data)
    if len(z_data) == 0:
        return -1
    if 'release' in z_data.keys():
        return 1
    if ',' in z_data['releases']:
        tag_num_str = z_data['releases'].strip()
        tag_num_list = tag_num_str.split(',')
        if len(tag_num_list) != 2:
            print tag_num_str
            return -1
        return int(tag_num_list[0]) * 1000 + int(tag_num_list[1])
    return int(z_data['releases'])


def GetUrlSolve(page, my_data):
    content = etree.HTML(page)
    name_lists = content.xpath('//a')
    new_urls = content.xpath('//a/@href')
    for i in range(len(name_lists)):
        fname = name_lists[i].xpath('string(.)')
        my_data[fname] = new_urls[i]


def GetUrls(base_url, url_lists):
    global url_break
    if len(url_lists) % 10 == 0:
        return 0
    gpage = ZSpider(base_url, header)
    if gpage == 'mllj':
        url_break = True
        return 0
    g_dir = {}
    GetUrlSolve(gpage, g_dir)
    for gkey, gvalue in g_dir.items():
        if gkey.strip() == 'Next':
            url_lists.append(gvalue.strip())
            print url_lists
            sleep(0.5)
            GetUrls(gvalue.strip(), url_lists)
            break
            #continue
    return 0


def GetUrlsMain(tag_num, base_url):
    global url_break
    pname = os.path.basename(base_url)
    ufname = dest_tmp_dir + os.sep + pname + '-urls.txt'
    with open(ufname, 'w') as (fp):
        fp.write(base_url + '/tags\n')
    while True:
        with open(ufname, 'r') as (fd):
            base_url = fd.readlines()[(-1)].strip()
            url_lists = [base_url]
            GetUrls(base_url, url_lists)
        with open(ufname, 'a') as (fp):
            for each_url in url_lists[1:]:
                fp.write(each_url + '\n')

        with open(ufname, 'r') as (fs):
            if tag_num % 10 == 0 and len(fs.readlines()) == tag_num / 10:
                break
            if len(fs.readlines()) == tag_num / 10 + 1:
                break
            if url_break:
                url_break = False
                break


def DownloadSolve(page, my_data):
    content = etree.HTML(page)
    #name_lists = content.xpath('//h4/a')
    new_urls = content.xpath('//h4/a/@href')
    for i in range(len(new_urls)):
        #fname = name_lists[i].xpath('string(.)')
        fname = os.path.basename(new_urls[i])
        my_data[fname] = new_urls[i]


def Download(base_url):
    pname = os.path.basename(base_url)
    dir_name = pname + '-' + base_url.split('/')[(-2)]
    if dir_name not in os.listdir(dest_src_dir):
        os.mkdir(dest_src_dir + os.sep + dir_name)
    ufname = dest_tmp_dir + os.sep + pname + '-urls.txt'
    download_url = base_url + '/archive/'
    with open(ufname, 'r') as (fp):
        for line in fp.readlines():
            fir_page = ZSpider(line.strip(), header)
            if fir_page == 'mllj':
                continue
            fir_dir = {}
            DownloadSolve(fir_page, fir_dir)
            for fkey in fir_dir.keys():
                full_url = download_url + fkey.strip() + '.tar.gz'
                if fkey.strip() + '.tar.gz' in os.listdir(dest_src_dir + os.sep + dir_name):
                    print 'package %s has downloaded!' % fkey.strip()
                    continue
                print 'download package %s:' % fkey.strip()
                print '****************************************'
                if os.system('wget "%s" -P %s' % (full_url, dest_src_dir + os.sep + dir_name)) != 0:
                    print 'download %s fail!' % fkey.strip()
                    with open('failpack.txt', 'a') as (fd):
                        fd.write('%s\n' % full_url)
                print 'downlaod %s success!' % fkey.strip()
                print '****************************************'
                sleep(1)

            sleep(1)

    cpname = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) + pname
    os.system('mv %s/%s-urls.txt %s/%s-url.txt' % (dest_tmp_dir, pname, dest_tmp_dir, cpname))


def main(base_url):
    tag_num = GetTagNum(base_url)
    if tag_num < 0:
        print 'error 1!'
        sys.exit(-1)
    elif tag_num == 0:
        print "no release!"
        sys.exit(0)
    try:
        GetUrlsMain(tag_num, base_url)
    except Exception, e:
        print 'error 2!'
        print str(e)
        sys.exit(-2)

    Download(base_url)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--baseurl',type=str,help="Base url.")
parser.add_argument('--destdir',type=str,help="Dest dir path.")
args = parser.parse_args()

base_url = args.baseurl
dest_dir = args.destdir
if base_url is None or dest_dir is None:
    parser.print_usage()
    sys.exit(0)

dest_src_dir = dest_dir + '/src'
dest_tmp_dir = dest_dir + '/tmp'
cur_dirs = os.listdir(dest_dir)
if 'src' not in cur_dirs:
    os.mkdir(dest_src_dir)
if 'tmp' not in cur_dirs:
    os.mkdir(dest_tmp_dir)

main(base_url)

