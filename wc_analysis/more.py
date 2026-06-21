# -*- coding: utf-8 -*-
"""
Further extensions:
  A) Blind single-team betting: "always bet team X to win every match it plays".
  B) "Always bet the team ranked world #1 that tournament" and "always bet the host".
  C) Equity (bankroll) curves over all 448 matches, flat-2.0 vs modeled real odds.
All on 90-minute regulation results.
"""
from compute import TOURNAMENTS

ORDER = sorted(TOURNAMENTS)  # 1998..2022 chronological
HOSTS = {"1998":"France","2002":["South Korea","Japan"],"2006":"Germany",
         "2010":"South Africa","2014":"Brazil","2018":"Russia","2022":"Qatar"}

def team_record(team):
    """Bet `team` to win every match it plays, across all WCs it appears in."""
    w=l=0; per={}
    for y in ORDER:
        ranks,matches=TOURNAMENTS[y]
        if team not in ranks: continue
        yw=yl=0
        for (a,sa,sb,b) in matches:
            if team==a: gf,ga=sa,sb
            elif team==b: gf,ga=sb,sa
            else: continue
            if gf>ga: yw+=1
            else: yl+=1
        if yw+yl: per[y]=(yw,yl); w+=yw; l+=yl
    return w,l,per

def A_single_teams():
    teams=["Brazil","Germany","Argentina","Spain","France","Netherlands","Italy",
           "England","Portugal","Mexico","USA","Uruguay","Croatia","Belgium"]
    print("A) 无脑押单支球队取胜(每场，平=输) — 1998-2022")
    print(f"{'球队':<12}{'参赛届':>6}{'下注':>6}{'赢':>5}{'输':>5}{'命中率':>8}{'净@2.0':>8}")
    print("-"*53)
    rows=[]
    for t in teams:
        w,l,per=team_record(t)
        n=w+l
        if not n: continue
        rows.append((t,len(per),n,w,l,w/n*100,w-l))
    for t,cups,n,w,l,hit,net in sorted(rows,key=lambda r:-r[6]):
        print(f"{t:<12}{cups:>6}{n:>6}{w:>5}{l:>5}{hit:>7.1f}%{net:>+8d}")

def B_rank1_and_host():
    print("\nB) 押'当届世界第一' / 押东道主 (每场取胜，平=输)")
    # world #1 that tournament = the team with min rank value
    print(f"{'届次':<6}{'世界第一':<14}{'第一战绩':>10}{'东道主':<14}{'东道主战绩':>10}")
    print("-"*58)
    tot1=[0,0]; toth=[0,0]
    for y in ORDER:
        ranks,matches=TOURNAMENTS[y]
        top=min(ranks,key=lambda k:ranks[k])
        def rec(team):
            w=l=0
            for (a,sa,sb,b) in matches:
                if team==a: gf,ga=sa,sb
                elif team==b: gf,ga=sb,sa
                else: continue
                if gf>ga: w+=1
                else: l+=1
            return w,l
        w1,l1=rec(top); tot1[0]+=w1; tot1[1]+=l1
        hosts=HOSTS[y] if isinstance(HOSTS[y],list) else [HOSTS[y]]
        hw=hl=0
        for h in hosts:
            a,b=rec(h); hw+=a; hl+=b
        toth[0]+=hw; toth[1]+=hl
        host_label="/".join(hosts)
        print(f"{y:<6}{top+'('+str(ranks[top])+')':<14}{f'{w1}胜{l1}负':>10}{host_label:<14}{f'{hw}胜{hl}负':>10}")
    print("-"*58)
    print(f"{'合计':<6}{'':<14}{f'{tot1[0]}胜{tot1[1]}负 {tot1[0]/sum(tot1)*100:.0f}%':>14}"
          f"{'':<6}{f'{toth[0]}胜{toth[1]}负 {toth[0]/sum(toth)*100:.0f}%':>14}")

# ---- C) equity curves ----
def bucket_odds():
    bins=[(1,3),(4,7),(8,14),(15,24),(25,200)]
    freq={b:[0,0,0,0] for b in bins}
    def binof(g):
        for lo,hi in bins:
            if lo<=g<=hi: return (lo,hi)
    for y in ORDER:
        ranks,matches=TOURNAMENTS[y]
        for (a,sa,sb,b) in matches:
            ra,rb=ranks[a],ranks[b]; gap=abs(ra-rb)
            fav_s,dog_s=(sa,sb) if ra<=rb else (sb,sa)
            bb=binof(gap); freq[bb][3]+=1
            if fav_s>dog_s: freq[bb][0]+=1
            elif fav_s==dog_s: freq[bb][1]+=1
            else: freq[bb][2]+=1
    MARGIN=1.06
    ow={b:1/((freq[b][0]/freq[b][3])*MARGIN) for b in bins}
    return binof,ow

def C_equity_curve():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    binof,ow=bucket_odds()
    flat=[0.0]; real=[0.0]; xs=[0]; n=0
    boundaries=[]
    for y in ORDER:
        ranks,matches=TOURNAMENTS[y]
        boundaries.append((n,y))
        for (a,sa,sb,b) in matches:
            ra,rb=ranks[a],ranks[b]; gap=abs(ra-rb)
            fav_s,dog_s=(sa,sb) if ra<=rb else (sb,sa)
            win = fav_s>dog_s
            n+=1; xs.append(n)
            flat.append(flat[-1] + (1 if win else -1))            # flat 2.0
            o=ow[binof(gap)]
            real.append(real[-1] + ((o-1) if win else -1))        # modeled real odds
    plt.figure(figsize=(11,6))
    plt.plot(xs,flat,label="Bet favorite to win @ flat 2.0 odds (naive)",lw=2,color="#1f77b4")
    plt.plot(xs,real,label="Bet favorite to win @ modeled real odds (6% margin)",lw=2,color="#d62728")
    plt.axhline(0,color="gray",lw=.8,ls="--")
    for x,y in boundaries:
        plt.axvline(x,color="#cccccc",lw=.7)
        plt.text(x+1,plt.ylim()[1]*0.92,y,fontsize=8,color="#666")
    plt.title("World Cup ranking-bet equity curve (1998-2022, 448 matches)")
    plt.xlabel("match # (chronological)"); plt.ylabel("cumulative units")
    plt.legend(loc="lower left"); plt.grid(alpha=.25)
    plt.tight_layout(); plt.savefig("equity_curve.png",dpi=130)
    print(f"\nC) 资金曲线已保存 equity_curve.png  | 终点: 固定2.0={flat[-1]:+.0f}  真实赔率模型={real[-1]:+.1f}")

if __name__=="__main__":
    A_single_teams()
    B_rank1_and_host()
    C_equity_curve()
