from cPickle import dumps
from client import Client, Query

a = Client("http://www.backtest.org")
# a.proxies = {
#     "http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
dic = {}
count = 0
for screen in Client.screens:
    for pick in range(2, 11, 2):
        q = [Query(
            percent=100, hold=1, screen=screen, posa=pick, posb=pick)]
        dic[(screen, pick)] = a.test_run(from_date=2000, query_list=q)
        count += 1


fp = open("data2.pickle", "wb")
fp.write(dumps(dic))
fp.close()

