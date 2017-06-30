from scrapy import cmdline

cmdline.execute("scrapy crawl medpred -a forum=8".split())
# or
# -a forum=ALL
