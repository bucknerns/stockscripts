import cPickle

from statistics import stdev

from client import Client


def avg(list_):
    return float(sum(list_))/len(list_)

dic = cPickle.loads(open("data.pickle").read())
avg_gain_dic = {}
print "screen,stddev,avg of 3,avg of 5,avg of 10,,picks"
for screen in Client.screens:
    for pick in range(1,11):
        sum_gain = 0
        for i, model in enumerate(dic[(screen, pick)]):
            sum_gain += model.gain
        avg_gain_dic[screen] = avg_gain_dic.setdefault(screen, []) + [float(sum_gain) / i]
    count = 0
    list_ = avg_gain_dic[screen]


    print "{0},{1},{2},{3},{4},,{5}".format(
        screen, stdev(list_), avg(list_[:3]), avg(list_[:5]), avg(list_),
        ",".join([str(x) for x in list_]))



