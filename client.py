from dateutil.parser import parse
from HTMLParser import HTMLParser
import requests
import sys


class Picks(object):
    def __init__(self, purchased, gain, annd, s_p, total, picks):
        self.purchased = purchased
        self.gain = int(gain)
        self.annd = int(annd)
        self.s_p = int(s_p)
        self.total = int(total)
        self.picks = picks

    def __eq__(self, obj):
        if ((self.purchased == obj.purchased) and
            (self.gain == obj.gain) and
            (self.annd == obj.annd) and
            (self.s_p == obj.s_p) and
            (self.total == obj.total) and
                (self.picks == obj.picks)):
            return True
        return False

    def __ne__(self, obj):
        return not self.__eq__(obj)


class MyList(list):
    pass


class Parser1(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._list = []
        self._table = False
        self._table_start = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._table = True

    def handle_endtag(self, tag):
        if tag == "table":
            self._table = False

    def handle_data(self, data):
        data = data.strip()
        if self._table and data:
            self._list.append(data.strip())
            if data == "P":
                self._table_start.append(len(self._list))

    def parse_data(self, string):
        self._list = []
        self.feed(string)
        big_table = MyList()

        args = []
        for item in self._list[self._table_start[2] + 2:]:
            args.append(item)
            if len(args) == 6:
                try:
                    big_table.append(Picks(*args))
                except:
                    pass
                args = []
        return big_table


class Parser2(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.list_ = []
        self.state = "OUT"
        self.strong = False
        self.date = ""

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.list_ = []
            self.state = "IN_TABLE"
        if tag == "a" and self.state == "IN_TABLE":
            self.state = "GET_DATA"
        if tag == "strong":
            self.strong = True

    def handle_endtag(self, tag):
        if tag == "a" and self.state == "GET_DATA":
            self.state = "IN_TABLE"
        if tag == "table":
            self.state = "OUT"
        if tag == "strong":
            self.strong = False

    def handle_data(self, data):
        if self.state == "GET_DATA":
            self.list_.append(data.strip())
        if self.strong:
            try:
                parse(data)
                self.date = data
            except:
                pass

    def parse_data(self, string):
        self.list_ = []
        self.feed(string)
        return self.list_, self.date


class Query(object):
    def __init__(self, percent, hold, screen, posa, posb):
        self.percent = percent
        self.hold = hold
        self.screen = screen
        self.posa = posa
        self.posb = posb


class Client(requests.Session):
    screens = [
        "3PT_SCV_pst", "3PT_SCV_pst_slta", "3PT_Value_SmallCap", "AssRS13",
        "AssRS26", "BETA", "BLITZ", "Benchmark", "BenchmarkFCF", "CAPLOWEG",
        "CAPRS", "CDPD", "DIVIDEND_GROWTH", "EG", "EG5PE", "EG5_AT", "EG5_PEG",
        "EGPLOW_PE", "EGPLOW_PE_E", "EGPR_PE", "EGRSW", "EG_PELA", "ERS13",
        "ERS26", "FOG_BDF", "FOG_MI", "FORM90", "Foolish4", "Fundamentals",
        "GAR4", "GAR4CFS", "GAR4CFSpbvlt3", "GAR4pbvlt3", "GARPEG", "GAR_EG5",
        "H52EarnPS", "H52EgPS", "H52EgPSlta", "HBSP", "HIGHCASHFLOW",
        "HIGH_CASH", "HIPRICE", "HIYIELD", "HI_DIV", "HI_INC_CSH", "IN_RS26",
        "JLC_DIV", "KEY100", "KEYCLQ", "KEYEPS", "KEYRSW", "KEYSTONE", "LLTD",
        "LOWDV", "LOWPB", "LOWPE", "LOWPE_ZLTD", "LOWPE_ZLTDA", "LOWPSR",
        "LPCF", "LPE_YLD", "LPS1+2_R26", "LPS1+2_RSW", "LPSAD", "LPSB",
        "LowPEsafe", "NoMo", "NoMoSafe", "OPTION_A", "OVER_PEG", "OVER_RS",
        "Olap_RS52keyeps", "Olap_RS52keystone", "Overlap_4_13", "PEBsize",
        "PEG", "PEG-Minimalist", "PEG-NT", "PEG13", "PEGFF", "PEGRSW", "PIH4",
        "PIH_CSO_safe", "PIH_CSO_simple", "PIH_MCP", "PLOW26WK", "PLOWBKLD",
        "PLOWBVS", "PLOWEG5_RS631", "PLOWLD_NRS", "PLOWPBV", "PLOWRSW",
        "PLOW_PE", "PLOW_PE2", "PLOW_PE2MOD", "PL_LD_NRS", "PL_LD_NRS_ALT",
        "PST_5-10", "R13_EG", "R13_EG2", "R13_EG_E", "REIT", "REP", "REV",
        "ROC_RS26WK", "ROEPLOW", "ROIC", "RS13WK", "RS13WKT12", "RS1WK",
        "RS2020", "RS26WK", "RS26WKT12", "RS4WK", "RS4WKT12", "RS52WK",
        "RS52WKT12", "RSCAP", "RSEG-rgonsal", "RSEP", "RSIBD", "RSPEG1",
        "RSPEG2", "RSPEGOL", "RSPS", "RSW", "RSWEPS", "SAFETY_BOUNCE",
        "SAFETY_HICCUP", "SHORT_A", "SHORT_ALTMAN_Z", "SHORT_B", "SHORT_C",
        "SHORT_DCB", "SHORT_K", "SHORT_M", "SHORT_SOS", "SHORT_V", "SLS_RS13",
        "SLS_RS26", "SOSBM_E", "SOS_A", "SOS_Ancer", "SOS_Ancer_2007",
        "SOS_Annual", "SOS_B", "SOS_BMOD", "SOS_C", "SOS_D", "SOS_DT",
        "SOS_DT4D", "SOS_E", "SOS_Elan_v2000", "SOS_Elan_v2001",
        "SOS_Elan_v2002", "SOS_F", "SOS_G", "SOS_GJ", "SOS_K", "SOS_KJ",
        "SOS_KitchenSink", "SOS_Plow_RS", "SPARK", "SPARKRSW", "Screamers",
        "SomeMo", "SomeMoC", "SomeMoJoeSafe", "SomeMoSafe", "TA_A", "TK1_R52",
        "TK2_R52", "TPEG13", "TREPPE", "TREPPE_E", "TTI", "TVALUE", "UG",
        "UG90", "ValueRatio", "Value_EG", "YEYPayout", "YIELD4",
        "YLDEARNYEAR", "YLDEARNYEAR2", "YLDYEAR", "YldDiv", "ZLTD", "ZLTDA"]

    def __init__(self, url, *args, **kwargs):
        super(Client, self).__init__()
        self.url = url
        self.parser = Parser1()
        self.parser2 = Parser2()

    def test_run(self, from_date=2000, to_date=2016, month=1, query_list=None):
        dic = {
            "tester": "BL", "submit": "Run", "from": from_date, "to": to_date,
            "month": month}
        for i, m in enumerate(query_list[:8]):
            dic["percent" + str(i + 1)] = m.percent
            dic["hold" + str(i + 1)] = m.hold
            dic["screen" + str(i + 1)] = m.screen
            dic["posa" + str(i + 1)] = m.posa
            dic["posb" + str(i + 1)] = m.posb
        return self.parser.parse_data(self.post(self.url, data=dic).content)

    def get_current(self):
        url = ("http://backtest.org/saucer/?V=2;p0=1;pn=1;x=10;k0=1;kn=4;e=1;n"
               "=SS%28TREPPE_E%29%28YLDEARNYEAR%29%28EGPLOW_PE_E%29%28PLOWEG5_"
               "RS631%29qb1m10l4;o=v;f=1;s=TREPPE_E;s=YLDEARNYEAR;s=EGPLOW_PE_"
               "E;s=PLOWEG5_RS631;s=EGPLOW_PE;rr=")
        return self.parser2.parse_data(self.get(url).content)

    def get_price(self, stock):
        params = {"symbol": stock}
        return self.get(
            "http://dev.markitondemand.com/Api/v2/Quote/json",
            params=params).json()

    def get_prices(self, stocks=None):
        stocks = stocks or self.get_current()[0]
        return reversed(sorted([{
            "stock": i, "price": float(self.get_price(i).get("LastPrice"))}
            for i in stocks], key=lambda k: k.get("price")))

    def calculate_purchases(self, money, stocks=None):
        stocks, date = (stocks, "") if stocks else self.get_current()
        start_money = money = float(money) - 8 * len(stocks)
        prices = self.get_prices(stocks)
        print "{0:<10}{1:<10}{2:<15}{3:<10}".format(
            "Stock", "Shares", "Cost/Share", "Total Cost")
        for i, dic in enumerate(prices):
            shares = int(money / (len(stocks) - i) / dic.get("price"))
            cost = shares * dic.get("price")
            money -= cost
            print "{0:<10}{1:<10}{2:<15}{3:<10}".format(
                dic.get("stock"), shares, dic.get("price"), cost)
        print "Spent: {0}\nRemaining: {1}\nDate: {2}".format(
            start_money-money, money, date)

if __name__ == "__main__":
    client = Client("http://www.backtest.org")
    client.calculate_purchases(sys.argv[1], sys.argv[2:])
