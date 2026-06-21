# -*- coding: utf-8 -*-
"""
Extended strategy comparison, built on the data in compute.py.
All outcomes use the 90-minute regulation result.

For each strategy we classify every applicable match as WON / LOST / PUSH and report:
  - bets (won+lost+push)
  - won, lost, push
  - hit rate = won / (won+lost)          (pushes excluded)
  - net @ flat 2.0 odds (win +1, loss -1, push 0)
  - break-even decimal odds = (won+lost)/won

Then a market-efficiency reality check: derive realistic market odds from the
empirical W/D/L frequencies (bucketed by ranking gap) plus a typical 6% margin,
and compute each strategy's realized ROI against those prices.
"""
from compute import TOURNAMENTS

def iter_matches():
    for year in sorted(TOURNAMENTS):
        ranks, matches = TOURNAMENTS[year]
        for (a, sa, sb, b) in matches:
            ra, rb = ranks[a], ranks[b]
            # favorite = lower rank number
            if ra <= rb:
                fav_s, dog_s, gap = sa, sb, rb - ra
            else:
                fav_s, dog_s, gap = sb, sa, ra - rb
            if fav_s > dog_s:
                res = "FAVWIN"
            elif fav_s == dog_s:
                res = "DRAW"
            else:
                res = "FAVLOSS"
            yield year, gap, res

ALL = list(iter_matches())

# ----- strategy definitions: map result -> 'W' / 'L' / 'P' / None(skip) -----
def s_fav_win(gap, res):      return 'W' if res=="FAVWIN" else 'L'
def s_fav_dc(gap, res):       return 'W' if res in ("FAVWIN","DRAW") else 'L'   # double chance
def s_fav_dnb(gap, res):      return 'P' if res=="DRAW" else ('W' if res=="FAVWIN" else 'L')  # draw-no-bet
def s_bigfav_win(gap, res):   return None if gap<20 else ('W' if res=="FAVWIN" else 'L')
def s_closefav_win(gap, res): return None if gap>=8 else ('W' if res=="FAVWIN" else 'L')  # gap 1-7
def s_dog_win(gap, res):      return 'W' if res=="FAVLOSS" else 'L'            # bet the underdog
def s_dog_dc(gap, res):       return 'W' if res in ("FAVLOSS","DRAW") else 'L' # underdog win or draw
def s_draw(gap, res):         return 'W' if res=="DRAW" else 'L'              # always bet the draw

STRATS = [
    ("押热门胜(平=输) 基准",      s_fav_win),
    ("押热门 双胜彩(胜或平)",     s_fav_dc),
    ("押热门胜 平局退本(DNB)",    s_fav_dnb),
    ("只买大热门(差>=20)胜",      s_bigfav_win),
    ("只买接近场(差1-7)押热门胜", s_closefav_win),
    ("反买冷门(排名低者)胜",      s_dog_win),
    ("反买冷门 双胜彩(胜或平)",   s_dog_dc),
    ("全押平局",                  s_draw),
]

def run():
    print("="*78)
    print(f"{'策略':<28}{'下注':>5}{'赢':>5}{'输':>5}{'退':>4}{'命中率':>8}{'净@2.0':>8}{'保本赔率':>9}")
    print("-"*78)
    for name, fn in STRATS:
        won=lost=push=0
        for _,gap,res in ALL:
            o = fn(gap,res)
            if o is None: continue
            if o=='W': won+=1
            elif o=='L': lost+=1
            else: push+=1
        dec = won+lost
        hit = won/dec*100 if dec else 0
        be = dec/won if won else float('inf')
        print(f"{name:<28}{won+lost+push:>5}{won:>5}{lost:>5}{push:>4}{hit:>7.1f}%{won-lost:>+8d}{be:>9.3f}")
    print("="*78)

# ---------------- market-efficiency reality check ----------------
def market_check():
    # empirical W/D/L for the favorite, bucketed by ranking gap
    bins = [(1,3),(4,7),(8,14),(15,24),(25,200)]
    def bin_of(g):
        for lo,hi in bins:
            if lo<=g<=hi: return (lo,hi)
    freq = {b:[0,0,0,0] for b in bins}  # win,draw,loss,total
    for _,gap,res in ALL:
        b=bin_of(gap); freq[b][3]+=1
        freq[b][0]+= res=="FAVWIN"; freq[b][1]+= res=="DRAW"; freq[b][2]+= res=="FAVLOSS"
    MARGIN=1.06   # 6% bookmaker overround
    print("\n按排名差分桶的经验概率(热门 胜/平/负) 及据此构造的含抽水市场赔率(margin 6%):")
    print(f"{'gap':<10}{'场数':>5}{'胜%':>7}{'平%':>7}{'负%':>7}{'胜赔':>7}{'平赔':>7}{'负赔':>7}")
    odds={}; probs={}
    for b in bins:
        w,d,l,n=freq[b]
        pw,pd,pl=w/n,d/n,l/n
        probs[b]=(pw,pd,pl)
        ow,od,ol=1/(pw*MARGIN),1/(pd*MARGIN),1/(pl*MARGIN)
        odds[b]=(ow,od,ol)
        print(f"{str(b):<10}{n:>5}{pw*100:>6.0f}%{pd*100:>6.0f}%{pl*100:>6.0f}%{ow:>7.2f}{od:>7.2f}{ol:>7.2f}")

    # realized ROI of each strategy against these modeled market odds
    print("\n用上述含抽水市场赔率，各策略的真实期望ROI(每场押1单位):")
    for name, fn in STRATS:
        staked=ret=0.0
        for _,gap,res in ALL:
            o=fn(gap,res)
            if o is None: continue
            b=bin_of(gap); ow,od,ol=odds[b]; pw,pd,pl=probs[b]
            staked+=1
            if o=='P':
                ret+=1; continue
            # determine payout if the bet hits, given strategy type
            if fn in (s_fav_win,s_bigfav_win,s_closefav_win):
                price=ow; hit=(res=="FAVWIN")
            elif fn is s_fav_dnb:
                # draw-no-bet priced as its own market (draw stake refunded)
                price=1/((pw/(pw+pl))*MARGIN); hit=(res=="FAVWIN")
            elif fn is s_fav_dc:
                # double chance pays like 1/(pw+pd); combine two outcomes
                price=1/((1/ow+1/od)); hit=(res in ("FAVWIN","DRAW"))
            elif fn is s_dog_win:
                price=ol; hit=(res=="FAVLOSS")
            elif fn is s_dog_dc:
                price=1/((1/ol+1/od)); hit=(res in ("FAVLOSS","DRAW"))
            elif fn is s_draw:
                price=od; hit=(res=="DRAW")
            ret += price if hit else 0
        roi=(ret-staked)/staked*100
        print(f"  {name:<28} ROI {roi:>+6.1f}%")

if __name__=="__main__":
    run()
    market_check()
