#!/usr/bin/env python
'''
Usage:
   hao123_crawl.py <query_file>
'''
from gevent import monkey
import gevent
import urllib2
import urllib
import config
from docopt import docopt
monkey.patch_all()
ip_list = []

def process_input(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip().split('\t')
            yield line[0]

def gen_url(filename):
    for item in process_input(filename):
        yield config.domain+"&"+urllib.urlencode({"wd":item})

def urlopen_wrapper(url,i):
    retry = 0
    while retry < 5:
        try:
            r = urllib2.urlopen(url)
            if r.getcode() == 200:
                print "get"+":"+str(i)
                break
            else: retry += 1
        except:
            retry += 1

def crawl_process(filename,spawn_num = 300):
    threads = []
    num = 0
    for i,url in enumerate(gen_url(filename)):
        threads.append(gevent.spawn(urlopen_wrapper,url,i))
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
    crawl_process(args['<query_file>'])
    print 'all done'
