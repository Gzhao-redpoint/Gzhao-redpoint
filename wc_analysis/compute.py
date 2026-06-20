# -*- coding: utf-8 -*-
"""
World Cup betting backtest: always bet the higher FIFA-ranked team to WIN in
regulation (90 min). A draw or a loss for the favorite = lost bet.
Equal stake per match (1 unit). Even-money assumption (decimal 2.0) for the
money column, so net profit == net wins. We also report hit rate.

Lower rank number = better ranked = the favorite we bet on.
Matches between two equally-ranked teams are recorded separately (no clear favorite).
"""

from collections import OrderedDict

# Each tournament: (ranks dict, list of matches). Match = (teamA, scoreA, scoreB, teamB)
# scores are the 90-minute REGULATION result.

TOURNAMENTS = OrderedDict()

# ----------------------------------------------------------------------------
# 2002 (Korea/Japan) — ranks as of 15 May 2002
# ----------------------------------------------------------------------------
ranks_2002 = {
    "France": 1, "Brazil": 2, "Argentina": 3, "Portugal": 5, "Italy": 6,
    "Mexico": 7, "Spain": 8, "Germany": 11, "England": 12, "USA": 13,
    "Ireland": 15, "Cameroon": 17, "Paraguay": 18, "Sweden": 19, "Denmark": 20,
    "Croatia": 21, "Turkey": 22, "Belgium": 23, "Uruguay": 24, "Slovenia": 25,
    "Nigeria": 27, "Russia": 28, "Costa Rica": 29, "Tunisia": 31, "Japan": 32,
    "Saudi Arabia": 34, "Ecuador": 36, "South Africa": 37, "Poland": 38,
    "South Korea": 40, "Senegal": 42, "China": 50,
}
matches_2002 = [
    ("Senegal",1,0,"France"),("Denmark",2,1,"Uruguay"),("Denmark",1,1,"Senegal"),
    ("France",0,0,"Uruguay"),("Denmark",2,0,"France"),("Senegal",3,3,"Uruguay"),
    ("Paraguay",2,2,"South Africa"),("Spain",3,1,"Slovenia"),("Spain",3,1,"Paraguay"),
    ("South Africa",1,0,"Slovenia"),("South Africa",2,3,"Spain"),("Slovenia",1,3,"Paraguay"),
    ("Brazil",2,1,"Turkey"),("China",0,2,"Costa Rica"),("Brazil",4,0,"China"),
    ("Costa Rica",1,1,"Turkey"),("Costa Rica",2,5,"Brazil"),("Turkey",3,0,"China"),
    ("South Korea",2,0,"Poland"),("USA",3,2,"Portugal"),("South Korea",1,1,"USA"),
    ("Portugal",4,0,"Poland"),("Portugal",0,1,"South Korea"),("Poland",3,1,"USA"),
    ("Ireland",1,1,"Cameroon"),("Germany",8,0,"Saudi Arabia"),("Germany",1,1,"Ireland"),
    ("Cameroon",1,0,"Saudi Arabia"),("Cameroon",0,2,"Germany"),("Saudi Arabia",0,3,"Ireland"),
    ("Argentina",1,0,"Nigeria"),("England",1,1,"Sweden"),("Sweden",2,1,"Nigeria"),
    ("Argentina",0,1,"England"),("Sweden",1,1,"Argentina"),("Nigeria",0,0,"England"),
    ("Croatia",0,1,"Mexico"),("Italy",2,0,"Ecuador"),("Italy",1,2,"Croatia"),
    ("Mexico",2,1,"Ecuador"),("Mexico",1,1,"Italy"),("Ecuador",1,0,"Croatia"),
    ("Japan",2,2,"Belgium"),("Russia",2,0,"Tunisia"),("Japan",1,0,"Russia"),
    ("Tunisia",1,1,"Belgium"),("Tunisia",0,2,"Japan"),("Belgium",3,2,"Russia"),
    # R16
    ("Germany",1,0,"Paraguay"),("Denmark",0,3,"England"),("Sweden",1,1,"Senegal"),
    ("Spain",1,1,"Ireland"),("Mexico",0,2,"USA"),("Brazil",2,0,"Belgium"),
    ("Japan",0,1,"Turkey"),("South Korea",1,1,"Italy"),
    # QF
    ("England",1,2,"Brazil"),("Germany",1,0,"USA"),("Spain",0,0,"South Korea"),
    ("Senegal",0,0,"Turkey"),
    # SF
    ("Germany",1,0,"South Korea"),("Brazil",1,0,"Turkey"),
    # 3rd, Final
    ("South Korea",2,3,"Turkey"),("Germany",0,2,"Brazil"),
]
TOURNAMENTS["2002"] = (ranks_2002, matches_2002)

# ----------------------------------------------------------------------------
# 2014 (Brazil) — ranks as of 5 June 2014
# ----------------------------------------------------------------------------
ranks_2014 = {
    "Spain":1,"Germany":2,"Brazil":3,"Portugal":4,"Argentina":5,"Switzerland":6,
    "Uruguay":7,"Colombia":8,"Italy":9,"England":10,"Belgium":11,"Greece":12,
    "USA":13,"Chile":14,"Netherlands":15,"France":17,"Russia":19,"Mexico":20,
    "Bosnia":21,"Algeria":22,"Ivory Coast":23,"Ecuador":26,"Costa Rica":28,
    "Honduras":33,"Ghana":37,"Iran":43,"Nigeria":44,"Japan":46,"Cameroon":56,
    "South Korea":57,"Australia":62,
}
matches_2014 = [
    ("Brazil",3,1,"Croatia"),  # NOTE Croatia rank missing -> add
    ("Mexico",1,0,"Cameroon"),("Brazil",0,0,"Mexico"),("Cameroon",0,4,"Croatia"),
    ("Cameroon",1,4,"Brazil"),("Croatia",1,3,"Mexico"),
    ("Spain",1,5,"Netherlands"),("Chile",3,1,"Australia"),("Australia",2,3,"Netherlands"),
    ("Spain",0,2,"Chile"),("Australia",0,3,"Spain"),("Netherlands",2,0,"Chile"),
    ("Colombia",3,0,"Greece"),("Ivory Coast",2,1,"Japan"),("Colombia",2,1,"Ivory Coast"),
    ("Japan",0,0,"Greece"),("Japan",1,4,"Colombia"),("Greece",2,1,"Ivory Coast"),
    ("Uruguay",1,3,"Costa Rica"),("England",1,2,"Italy"),("Uruguay",2,1,"England"),
    ("Italy",0,1,"Costa Rica"),("Italy",0,1,"Uruguay"),("Costa Rica",0,0,"England"),
    ("Switzerland",2,1,"Ecuador"),("France",3,0,"Honduras"),("Switzerland",2,5,"France"),
    ("Honduras",1,2,"Ecuador"),("Honduras",0,3,"Switzerland"),("Ecuador",0,0,"France"),
    ("Argentina",2,1,"Bosnia"),("Iran",0,0,"Nigeria"),("Argentina",1,0,"Iran"),
    ("Nigeria",1,0,"Bosnia"),("Nigeria",2,3,"Argentina"),("Bosnia",3,1,"Iran"),
    ("Germany",4,0,"Portugal"),("Ghana",1,2,"USA"),("Germany",2,2,"Ghana"),
    ("USA",2,2,"Portugal"),("USA",0,1,"Germany"),("Portugal",2,1,"Ghana"),
    ("Belgium",2,1,"Algeria"),("Russia",1,1,"South Korea"),("Belgium",1,0,"Russia"),
    ("South Korea",2,4,"Algeria"),("South Korea",0,1,"Belgium"),("Algeria",1,1,"Russia"),
    # R16 (90-min scores)
    ("Brazil",1,1,"Chile"),("Colombia",2,0,"Uruguay"),("Netherlands",2,1,"Mexico"),
    ("Costa Rica",1,1,"Greece"),("France",2,0,"Nigeria"),("Germany",0,0,"Algeria"),
    ("Argentina",0,0,"Switzerland"),("Belgium",0,0,"USA"),
    # QF
    ("France",0,1,"Germany"),("Brazil",2,1,"Colombia"),("Argentina",1,0,"Belgium"),
    ("Netherlands",0,0,"Costa Rica"),
    # SF
    ("Brazil",1,7,"Germany"),("Netherlands",0,0,"Argentina"),
    # 3rd, Final
    ("Brazil",0,3,"Netherlands"),("Germany",0,0,"Argentina"),
]
# Croatia rank in June 2014 was 18 (non? actually Croatia qualified, rank 18)
ranks_2014["Croatia"] = 18
TOURNAMENTS["2014"] = (ranks_2014, matches_2014)

# ----------------------------------------------------------------------------
# 2018 (Russia) — ranks as of 7 June 2018
# ----------------------------------------------------------------------------
ranks_2018 = {
    "Russia":70,"Saudi Arabia":67,"Egypt":45,"Uruguay":14,"Portugal":4,"Spain":10,
    "Morocco":41,"Iran":37,"France":7,"Australia":36,"Peru":11,"Denmark":12,
    "Argentina":5,"Iceland":22,"Croatia":20,"Nigeria":48,"Brazil":2,"Switzerland":6,
    "Costa Rica":23,"Serbia":34,"Germany":1,"Mexico":15,"Sweden":24,"South Korea":57,
    "Belgium":3,"Panama":55,"Tunisia":21,"England":12,"Poland":8,"Senegal":27,
    "Colombia":16,"Japan":61,
}
matches_2018 = [
    ("Russia",5,0,"Saudi Arabia"),("Egypt",0,1,"Uruguay"),("Morocco",0,1,"Iran"),
    ("Portugal",3,3,"Spain"),("France",2,1,"Australia"),("Argentina",1,1,"Iceland"),
    ("Peru",0,1,"Denmark"),("Croatia",2,0,"Nigeria"),("Costa Rica",0,1,"Serbia"),
    ("Germany",0,1,"Mexico"),("Brazil",1,1,"Switzerland"),("Sweden",1,0,"South Korea"),
    ("Belgium",3,0,"Panama"),("Tunisia",1,2,"England"),("Colombia",1,2,"Japan"),
    ("Poland",1,2,"Senegal"),("Russia",3,1,"Egypt"),("Portugal",1,0,"Morocco"),
    ("Uruguay",1,0,"Saudi Arabia"),("Iran",0,1,"Spain"),("Denmark",1,1,"Australia"),
    ("France",1,0,"Peru"),("Argentina",0,3,"Croatia"),("Brazil",2,0,"Costa Rica"),
    ("Nigeria",2,0,"Iceland"),("Serbia",1,2,"Switzerland"),("Belgium",5,2,"Tunisia"),
    ("South Korea",1,2,"Mexico"),("Germany",2,1,"Sweden"),("England",6,1,"Panama"),
    ("Japan",2,2,"Senegal"),("Poland",0,3,"Colombia"),("Uruguay",3,0,"Russia"),
    ("Saudi Arabia",2,1,"Egypt"),("Spain",2,2,"Morocco"),("Iran",1,1,"Portugal"),
    ("Denmark",0,0,"France"),("Australia",0,2,"Peru"),("Nigeria",1,2,"Argentina"),
    ("Iceland",1,2,"Croatia"),("Mexico",0,3,"Sweden"),("South Korea",2,0,"Germany"),
    ("Serbia",0,2,"Brazil"),("Switzerland",2,2,"Costa Rica"),("Japan",0,1,"Poland"),
    ("Senegal",0,1,"Colombia"),("England",0,1,"Belgium"),("Panama",1,2,"Tunisia"),
    # R16 (90-min)
    ("France",4,3,"Argentina"),("Uruguay",2,1,"Portugal"),("Spain",1,1,"Russia"),
    ("Croatia",1,1,"Denmark"),("Brazil",2,0,"Mexico"),("Belgium",3,2,"Japan"),
    ("Sweden",1,0,"Switzerland"),("Colombia",1,1,"England"),
    # QF
    ("Uruguay",0,2,"France"),("Brazil",1,2,"Belgium"),("Sweden",0,2,"England"),
    ("Russia",2,2,"Croatia"),
    # SF (Croatia-England 1-1 at 90)
    ("France",1,0,"Belgium"),("Croatia",1,1,"England"),
    # 3rd, Final
    ("Belgium",2,0,"England"),("France",4,2,"Croatia"),
]
TOURNAMENTS["2018"] = (ranks_2018, matches_2018)

# ----------------------------------------------------------------------------
# 2022 (Qatar) — ranks as of 6 October 2022
# ----------------------------------------------------------------------------
ranks_2022 = {
    "Brazil":1,"Belgium":2,"Argentina":3,"France":4,"England":5,"Spain":7,
    "Netherlands":8,"Portugal":9,"Denmark":10,"Germany":11,"Croatia":12,"Mexico":13,
    "Uruguay":14,"Switzerland":15,"USA":16,"Senegal":18,"Wales":19,"Iran":20,
    "Serbia":21,"Morocco":22,"Japan":24,"Poland":26,"South Korea":28,"Tunisia":30,
    "Costa Rica":31,"Australia":38,"Canada":41,"Cameroon":43,"Ecuador":44,"Qatar":50,
    "Saudi Arabia":51,"Ghana":61,
}
matches_2022 = [
    ("Qatar",0,2,"Ecuador"),("Senegal",0,2,"Netherlands"),("Qatar",1,3,"Senegal"),
    ("Netherlands",1,1,"Ecuador"),("Ecuador",1,2,"Senegal"),("Netherlands",2,0,"Qatar"),
    ("England",6,2,"Iran"),("USA",1,1,"Wales"),("Wales",0,2,"Iran"),
    ("England",0,0,"USA"),("Wales",0,3,"England"),("Iran",0,1,"USA"),
    ("Argentina",1,2,"Saudi Arabia"),("Mexico",0,0,"Poland"),("Poland",2,0,"Saudi Arabia"),
    ("Argentina",2,0,"Mexico"),("Poland",0,2,"Argentina"),("Saudi Arabia",1,2,"Mexico"),
    ("Denmark",0,0,"Tunisia"),("France",4,1,"Australia"),("Tunisia",0,1,"Australia"),
    ("France",2,1,"Denmark"),("Australia",1,0,"Denmark"),("Tunisia",1,0,"France"),
    ("Germany",1,2,"Japan"),("Spain",7,0,"Costa Rica"),("Japan",0,1,"Costa Rica"),
    ("Spain",1,1,"Germany"),("Japan",2,1,"Spain"),("Costa Rica",2,4,"Germany"),
    ("Morocco",0,0,"Croatia"),("Belgium",1,0,"Canada"),("Belgium",0,2,"Morocco"),
    ("Croatia",4,1,"Canada"),("Croatia",0,0,"Belgium"),("Canada",1,2,"Morocco"),
    ("Switzerland",1,0,"Cameroon"),("Brazil",2,0,"Serbia"),("Cameroon",3,3,"Serbia"),
    ("Brazil",1,0,"Switzerland"),("Serbia",2,3,"Switzerland"),("Cameroon",1,0,"Brazil"),
    ("Uruguay",0,0,"South Korea"),("Portugal",3,2,"Ghana"),("South Korea",2,3,"Ghana"),
    ("Portugal",2,0,"Uruguay"),("Ghana",0,2,"Uruguay"),("South Korea",2,1,"Portugal"),
    # R16 (90-min)
    ("Netherlands",3,1,"USA"),("Argentina",2,1,"Australia"),("France",3,1,"Poland"),
    ("England",3,0,"Senegal"),("Japan",1,1,"Croatia"),("Brazil",4,1,"South Korea"),
    ("Morocco",0,0,"Spain"),("Portugal",6,1,"Switzerland"),
    # QF (90-min: Croatia-Brazil 0-0, Ned-Arg 2-2)
    ("Croatia",0,0,"Brazil"),("Netherlands",2,2,"Argentina"),("Morocco",1,0,"Portugal"),
    ("England",1,2,"France"),
    # SF
    ("Argentina",3,0,"Croatia"),("France",2,0,"Morocco"),
    # 3rd, Final (90-min: Arg-Fra 2-2)
    ("Croatia",2,1,"Morocco"),("Argentina",2,2,"France"),
]
TOURNAMENTS["2022"] = (ranks_2022, matches_2022)

# ----------------------------------------------------------------------------
# 1998 (France) — ranks as of 20 May 1998 (no June 1998 ranking was published)
# ----------------------------------------------------------------------------
ranks_1998 = {
    "Brazil":1,"Germany":2,"Mexico":4,"England":5,"Argentina":6,"Norway":7,
    "Yugoslavia":8,"Chile":9,"Colombia":10,"USA":11,"Japan":12,"Morocco":13,
    "Italy":14,"Spain":15,"France":18,"Croatia":19,"South Korea":20,"Tunisia":21,
    "Romania":22,"South Africa":24,"Netherlands":25,"Denmark":27,"Paraguay":29,
    "Jamaica":30,"Austria":31,"Saudi Arabia":34,"Bulgaria":35,"Belgium":36,
    "Scotland":41,"Iran":42,"Cameroon":49,"Nigeria":74,
}
matches_1998 = [
    ("Brazil",2,1,"Scotland"),("Morocco",2,2,"Norway"),("Scotland",1,1,"Norway"),
    ("Brazil",3,0,"Morocco"),("Scotland",0,3,"Morocco"),("Brazil",1,2,"Norway"),
    ("Italy",2,2,"Chile"),("Cameroon",1,1,"Austria"),("Chile",1,1,"Austria"),
    ("Italy",3,0,"Cameroon"),("Italy",2,1,"Austria"),("Chile",1,1,"Cameroon"),
    ("Saudi Arabia",0,1,"Denmark"),("France",3,0,"South Africa"),("South Africa",1,1,"Denmark"),
    ("France",4,0,"Saudi Arabia"),("France",2,1,"Denmark"),("South Africa",2,2,"Saudi Arabia"),
    ("Paraguay",0,0,"Bulgaria"),("Spain",2,3,"Nigeria"),("Nigeria",1,0,"Bulgaria"),
    ("Spain",0,0,"Paraguay"),("Nigeria",1,3,"Paraguay"),("Spain",6,1,"Bulgaria"),
    ("South Korea",1,3,"Mexico"),("Netherlands",0,0,"Belgium"),("Belgium",2,2,"Mexico"),
    ("Netherlands",5,0,"South Korea"),("Netherlands",2,2,"Mexico"),("Belgium",1,1,"South Korea"),
    ("Yugoslavia",1,0,"Iran"),("Germany",2,0,"USA"),("Germany",2,2,"Yugoslavia"),
    ("USA",1,2,"Iran"),("Germany",2,0,"Iran"),("USA",0,1,"Yugoslavia"),
    ("England",2,0,"Tunisia"),("Romania",1,0,"Colombia"),("Colombia",1,0,"Tunisia"),
    ("Romania",2,1,"England"),("Colombia",0,2,"England"),("Romania",1,1,"Tunisia"),
    ("Argentina",1,0,"Japan"),("Jamaica",1,3,"Croatia"),("Japan",0,1,"Croatia"),
    ("Argentina",5,0,"Jamaica"),("Argentina",1,0,"Croatia"),("Japan",1,2,"Jamaica"),
    # knockout (90-min regulation scores)
    ("Italy",1,0,"Norway"),("Brazil",4,1,"Chile"),("France",0,0,"Paraguay"),
    ("Nigeria",1,4,"Denmark"),("Germany",2,1,"Mexico"),("Netherlands",2,1,"Yugoslavia"),
    ("Romania",0,1,"Croatia"),("Argentina",2,2,"England"),
    ("Italy",0,0,"France"),("Brazil",3,2,"Denmark"),("Netherlands",2,1,"Argentina"),
    ("Germany",0,3,"Croatia"),("Brazil",1,1,"Netherlands"),("France",2,1,"Croatia"),
    ("Netherlands",1,2,"Croatia"),("Brazil",0,3,"France"),
]
TOURNAMENTS["1998"] = (ranks_1998, matches_1998)

# ----------------------------------------------------------------------------
# 2006 (Germany) — ranks as of 17 May 2006 (verified, cross-checked 3 sources)
# Ties: USA=Spain=5, Iran=Croatia=23, Poland=South Korea=29 (none met head-to-head)
# ----------------------------------------------------------------------------
ranks_2006 = {
    "Brazil":1,"Czech Republic":2,"Netherlands":3,"Mexico":4,"USA":5,"Spain":5,
    "Portugal":7,"France":8,"Argentina":9,"England":10,"Italy":13,"Sweden":16,
    "Japan":18,"Germany":19,"Tunisia":21,"Iran":23,"Croatia":23,"Costa Rica":26,
    "Poland":29,"South Korea":29,"Ivory Coast":32,"Paraguay":33,"Saudi Arabia":34,
    "Switzerland":35,"Ecuador":39,"Australia":42,"Serbia and Montenegro":44,
    "Ukraine":45,"Trinidad and Tobago":47,"Ghana":48,"Angola":57,"Togo":61,
}
matches_2006 = [
    ("Germany",4,2,"Costa Rica"),("Poland",0,2,"Ecuador"),("Germany",1,0,"Poland"),
    ("Ecuador",3,0,"Costa Rica"),("Costa Rica",1,2,"Poland"),("Ecuador",0,3,"Germany"),
    ("England",1,0,"Paraguay"),("Trinidad and Tobago",0,0,"Sweden"),("England",2,0,"Trinidad and Tobago"),
    ("Sweden",1,0,"Paraguay"),("Paraguay",2,0,"Trinidad and Tobago"),("Sweden",2,2,"England"),
    ("Argentina",2,1,"Ivory Coast"),("Serbia and Montenegro",0,1,"Netherlands"),
    ("Argentina",6,0,"Serbia and Montenegro"),("Netherlands",2,1,"Ivory Coast"),
    ("Netherlands",0,0,"Argentina"),("Ivory Coast",3,2,"Serbia and Montenegro"),
    ("Mexico",3,1,"Iran"),("Angola",0,1,"Portugal"),("Mexico",0,0,"Angola"),
    ("Portugal",2,0,"Iran"),("Portugal",2,1,"Mexico"),("Iran",1,1,"Angola"),
    ("USA",0,3,"Czech Republic"),("Italy",2,0,"Ghana"),("Czech Republic",0,2,"Ghana"),
    ("Italy",1,1,"USA"),("Czech Republic",0,2,"Italy"),("Ghana",2,1,"USA"),
    ("Australia",3,1,"Japan"),("Brazil",1,0,"Croatia"),("Japan",0,0,"Croatia"),
    ("Brazil",2,0,"Australia"),("Croatia",2,2,"Australia"),("Japan",1,4,"Brazil"),
    ("South Korea",2,1,"Togo"),("France",0,0,"Switzerland"),("France",1,1,"South Korea"),
    ("Togo",0,2,"Switzerland"),("Togo",0,2,"France"),("Switzerland",2,0,"South Korea"),
    ("Spain",4,0,"Ukraine"),("Tunisia",2,2,"Saudi Arabia"),("Saudi Arabia",0,4,"Ukraine"),
    ("Spain",3,1,"Tunisia"),("Saudi Arabia",0,1,"Spain"),("Ukraine",1,0,"Tunisia"),
    # R16 (90-min)
    ("Germany",2,0,"Sweden"),("Argentina",1,1,"Mexico"),("England",1,0,"Ecuador"),
    ("Portugal",1,0,"Netherlands"),("Italy",1,0,"Australia"),("Switzerland",0,0,"Ukraine"),
    ("Brazil",3,0,"Ghana"),("Spain",1,3,"France"),
    # QF (90-min)
    ("Germany",1,1,"Argentina"),("Italy",3,0,"Ukraine"),("England",0,0,"Portugal"),
    ("Brazil",0,1,"France"),
    # SF (90-min: Germany 0-0 Italy, both goals in ET)
    ("Germany",0,0,"Italy"),("Portugal",0,1,"France"),
    # 3rd, Final (90-min: Italy 1-1 France)
    ("Germany",3,1,"Portugal"),("Italy",1,1,"France"),
]
TOURNAMENTS["2006"] = (ranks_2006, matches_2006)

# ----------------------------------------------------------------------------
# 2010 (South Africa) — ranks as of 26 May 2010
# ----------------------------------------------------------------------------
ranks_2010 = {
    "Brazil":1,"Spain":2,"Portugal":3,"Netherlands":4,"Italy":5,"Germany":6,
    "Argentina":7,"England":8,"France":9,"Greece":13,"USA":14,"Serbia":15,
    "Uruguay":16,"Mexico":17,"Chile":18,"Cameroon":19,"Australia":20,"Nigeria":21,
    "Switzerland":24,"Slovenia":25,"Ivory Coast":27,"Algeria":30,"Paraguay":31,
    "Ghana":32,"Slovakia":34,"Denmark":36,"Honduras":38,"Japan":45,"South Korea":47,
    "New Zealand":78,"South Africa":83,"North Korea":105,
}
matches_2010 = [
    ("South Africa",1,1,"Mexico"),("Uruguay",0,0,"France"),("South Africa",0,3,"Uruguay"),
    ("France",0,2,"Mexico"),("Mexico",0,1,"Uruguay"),("France",1,2,"South Africa"),
    ("South Korea",2,0,"Greece"),("Argentina",1,0,"Nigeria"),("Argentina",4,1,"South Korea"),
    ("Greece",2,1,"Nigeria"),("Nigeria",2,2,"South Korea"),("Greece",0,2,"Argentina"),
    ("England",1,1,"USA"),("Algeria",0,1,"Slovenia"),("Slovenia",2,2,"USA"),
    ("England",0,0,"Algeria"),("Slovenia",0,1,"England"),("USA",1,0,"Algeria"),
    ("Serbia",0,1,"Ghana"),("Germany",4,0,"Australia"),("Germany",0,1,"Serbia"),
    ("Ghana",1,1,"Australia"),("Ghana",0,1,"Germany"),("Australia",2,1,"Serbia"),
    ("Netherlands",2,0,"Denmark"),("Japan",1,0,"Cameroon"),("Netherlands",1,0,"Japan"),
    ("Cameroon",1,2,"Denmark"),("Denmark",1,3,"Japan"),("Cameroon",1,2,"Netherlands"),
    ("Italy",1,1,"Paraguay"),("New Zealand",1,1,"Slovakia"),("Slovakia",0,2,"Paraguay"),
    ("Italy",1,1,"New Zealand"),("Slovakia",3,2,"Italy"),("Paraguay",0,0,"New Zealand"),
    ("Ivory Coast",0,0,"Portugal"),("Brazil",2,1,"North Korea"),("Brazil",3,1,"Ivory Coast"),
    ("Portugal",7,0,"North Korea"),("Portugal",0,0,"Brazil"),("North Korea",0,3,"Ivory Coast"),
    ("Honduras",0,1,"Chile"),("Spain",0,1,"Switzerland"),("Chile",1,0,"Switzerland"),
    ("Spain",2,0,"Honduras"),("Chile",1,2,"Spain"),("Switzerland",0,0,"Honduras"),
    # R16 (90-min: USA-Ghana 1-1, Paraguay-Japan 0-0)
    ("Uruguay",2,1,"South Korea"),("USA",1,1,"Ghana"),("Germany",4,1,"England"),
    ("Argentina",3,1,"Mexico"),("Netherlands",2,1,"Slovakia"),("Brazil",3,0,"Chile"),
    ("Paraguay",0,0,"Japan"),("Spain",1,0,"Portugal"),
    # QF (90-min: Uruguay-Ghana 1-1)
    ("Netherlands",2,1,"Brazil"),("Uruguay",1,1,"Ghana"),("Argentina",0,4,"Germany"),
    ("Paraguay",0,1,"Spain"),
    # SF
    ("Uruguay",2,3,"Netherlands"),("Germany",0,1,"Spain"),
    # 3rd, Final (90-min: Netherlands 0-0 Spain)
    ("Uruguay",2,3,"Germany"),("Netherlands",0,0,"Spain"),
]
TOURNAMENTS["2010"] = (ranks_2010, matches_2010)


# ----------------------------------------------------------------------------
# ENGINE
# ----------------------------------------------------------------------------
def analyze():
    grand_won = grand_lost = grand_push = grand_ties = 0
    print(f"{'Year':<6}{'Bets':>6}{'Won':>6}{'Lost':>6}{'HitRate':>9}{'NetUnits':>10}")
    print("-"*43)
    per_year = {}
    for year in sorted(TOURNAMENTS):
        ranks, matches = TOURNAMENTS[year]
        won = lost = ties = 0
        details = []
        for (a, sa, sb, b) in matches:
            if a not in ranks:
                raise SystemExit(f"[{year}] missing rank for {a}")
            if b not in ranks:
                raise SystemExit(f"[{year}] missing rank for {b}")
            ra, rb = ranks[a], ranks[b]
            if ra == rb:
                ties += 1
                continue
            fav, fs, os_ = (a, sa, sb) if ra < rb else (b, sb, sa)
            if fs > os_:
                won += 1
                details.append((fav, "WON"))
            else:
                lost += 1
                details.append((fav, "LOST"))
        bets = won + lost
        hit = won / bets * 100 if bets else 0
        net = won - lost  # even-money: +1 win, -1 loss
        print(f"{year:<6}{bets:>6}{won:>6}{lost:>6}{hit:>8.1f}%{net:>+10d}")
        grand_won += won; grand_lost += lost; grand_ties += ties
        per_year[year] = (bets, won, lost, hit, net)
    print("-"*43)
    tot_bets = grand_won + grand_lost
    tot_hit = grand_won / tot_bets * 100
    print(f"{'TOTAL':<6}{tot_bets:>6}{grand_won:>6}{grand_lost:>6}{tot_hit:>8.1f}%{grand_won-grand_lost:>+10d}")
    print(f"\nEqual-rank matches skipped (no favorite): {grand_ties}")
    print(f"\nMoney @ even odds (1 unit/match, win returns 2.0): "
          f"net {grand_won-grand_lost:+d} units on {tot_bets} units staked "
          f"= ROI {(grand_won-grand_lost)/tot_bets*100:+.1f}%")
    print(f"Break-even decimal odds needed: {tot_bets/grand_won:.3f} "
          f"(i.e. favorites must average >= this price to profit)")

if __name__ == "__main__":
    analyze()
