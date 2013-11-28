#!/usr/bin/env python
'''
Usage:
   process_cdn <img_file> <ip_file> 
'''
from gevent import monkey
import gevent
import urllib2
from docopt import docopt
monkey.patch_all()
ip_list = []

def process_input(filename):
    with open(filename) as f:
        for line in f:
            index = line.find("it/")
            yield line[index:].strip()
def process_ip(ip_filename):
    with open(ip_filename) as f:
        for line in f:
            ip_list.append(line.strip())
def cdn_url(filename,ip_filename):
    process_ip(ip_filename)
    for item in process_input(filename):
        for ip in ip_list:
            yield "http://"+ip+"/"+item
def urlopen_wrapper(url):
    print url
    req = urllib2.Request(url)
    req.add_header('Referer','www.baidu.com')
    for i in range(5):
        r = urllib2.urlopen(req)
        if r.info().getheader('CDN-AGE') == '1':
            print 'cached'
            break
def cdn_hit(filename,ip_filename,spawn_num = 300):
    threads = []
    num = 0
    for url in cdn_url(filename,ip_filename):
        threads.append(gevent.spawn(urlopen_wrapper,url))
        num += 1
        if num == spawn_num:
            gevent.joinall(threads)
            treads = []
            num = 0
    gevent.joinall(threads)
#    for url in cdn_url(filename,ip_filename):
#        urlopen_wrapper(url)
if __name__ == '__main__':
    args = docopt(__doc__)
    cdn_hit(args['<img_file>'],args['<ip_file>'])
    print 'all done'
