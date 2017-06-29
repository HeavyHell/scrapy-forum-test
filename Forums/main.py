from scrapy import cmdline

cmdline.execute("scrapy crawl medpred -a forum=ALL".split())
# or
# -a forum=ALL
