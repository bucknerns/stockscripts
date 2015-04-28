from client import Client, Query

a = Client("http://www.backtest.org")
# a.proxies = {
#     "http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
dic = {}
count = 0
for screen in Client.screens[:]:
    for year in [2010]:  # range(2000, 2011, 5) + [2011, 2013]:
        for picks in xrange(1, 10):
            for hold in [1]:
                q = [Query(100, hold, screen, 1, picks)]
                dic[(screen, year, picks, hold)] = a.test_run(year, 2014, 1, q)
                count += 1
                print count


def sorted_max(dic):
    return sorted([([k, v[-1].total]) for k, v in dic.items()],
                  key=lambda k: k[1])

for i in sorted_max(dic):
    print i
