"""Deterministic, clearly labeled market fixtures. Never a live price feed."""
import math
import random
from datetime import datetime, timezone, timedelta
from functools import lru_cache
from typing import Literal
from fastapi import APIRouter, HTTPException

METRICS = {
 'dog': (0.00428,3812,284000,18.42,100,73),
 'cat': (0.0000734,834,21600,-5.13,100,49),
 'ape': (0.00182,2601,147800,32.71,100,94),
 'bonk': (0.0000316,642,9400,8.64,63,18),
 'pepe': (0.000164,1297,42700,-2.81,100,62),
 'wif': (0.000291,1842,68300,12.35,100,31),
}

def market_fields(project_id):
    price, holders, liquidity, change, bonding, age_hours = METRICS[project_id]
    now=datetime.now(timezone.utc).replace(second=0,microsecond=0)
    return dict(price_usd=price,price_sol=price/150,sol_price_usd=150,market_cap=price*1_000_000_000,
        fdv=price*1_000_000_000,supply=1_000_000_000,holders=holders,liquidity=liquidity,
        change_5m=round(change/21,2),change_1h=round(change/6,2),change_6h=round(change/2.4,2),change_24h=change,
        bonding_progress=bonding,market_status='Graduated' if bonding==100 else 'Bonding',
        market_snapshot=int(now.timestamp()),created_at=(now-timedelta(hours=age_hours)).isoformat(),
        mint_address=None,protocol='Pump.fun / PF')

@lru_cache(maxsize=12)
def minute_candles(project_id, price, change, snapshot, volume):
    rng=random.Random(f'paperbag-market-{project_id}')
    count=7*24*60
    values=[]
    start=price*.56
    day_start=price/(1+change/100)
    previous=start
    for i in range(count):
        if i<count-1440:
            t=i/(count-1440)
            trend=start+(day_start-start)*t
        else:
            t=(i-(count-1440))/1439
            trend=day_start+(price-day_start)*t
        noise=math.sin(i*.063)*.018+math.sin(i*.017)*.03+rng.uniform(-.006,.006)
        # Price endpoints are fixed so all chart intervals agree with the quote.
        close=trend*(1+noise)
        if i==count-1441: close=day_start
        if i==count-1: close=price
        high=max(previous,close)*(1+rng.uniform(.001,.009))
        low=min(previous,close)*(1-rng.uniform(.001,.009))
        values.append(dict(time=snapshot-(count-1-i)*60,open=round(previous,12),high=round(high,12),low=round(low,12),close=round(close,12),volume=round(volume/1440*rng.uniform(.3,1.7),2)))
        previous=close
    # Last 24h volume matches the displayed market metric.
    last_total=sum(c['volume'] for c in values[-1440:])
    for c in values[-1440:]: c['volume']=round(c['volume']*volume/last_total,2)
    return values

def chart_data(project, timeframe):
    minutes={'1m':1,'5m':5,'15m':15,'1h':60,'4h':240}[timeframe]
    base=minute_candles(project['id'],project['price_usd'],project['change_24h'],project['market_snapshot'],project['volume'])
    grouped=[]
    for start in range(0,len(base),minutes):
        chunk=base[start:start+minutes]
        grouped.append(dict(time=chunk[0]['time'],open=chunk[0]['open'],high=max(x['high'] for x in chunk),low=min(x['low'] for x in chunk),close=chunk[-1]['close'],volume=round(sum(x['volume'] for x in chunk),2)))
    return grouped[-120:]

def create_market_router(db):
    router=APIRouter(prefix='/api/market')
    async def get_project(project_id):
        p=await db.projects.find_one({'id':project_id},{'_id':0})
        if not p: raise HTTPException(404,'Token not found')
        return p

    @router.get('/{project_id}/candles')
    async def candles(project_id:str,timeframe:Literal['1m','5m','15m','1h','4h']='15m'):
        p=await get_project(project_id)
        return {'candles':chart_data(p,timeframe),'timeframe':timeframe,'snapshot':p['market_snapshot'],'data_mode':'illustrative','quote':'USD'}

    @router.get('/{project_id}/trades')
    async def trades(project_id:str):
        p=await get_project(project_id)
        rng=random.Random('trades-'+project_id)
        items=[]
        for i in range(24):
            sol=round(rng.uniform(.04,4.2),3)
            items.append({'id':f'sample-{project_id}-{i}','side':'buy' if rng.random()>.4 else 'sell','sol_amount':sol,'quantity':round(sol/p['price_sol'],3),'price_usd':p['price_usd'],'trader':f'Sample trader {rng.randint(101,999)}','executed_at':datetime.fromtimestamp(p['market_snapshot']-i*47,timezone.utc).isoformat(),'is_simulated':True})
        return {'items':items,'data_mode':'illustrative'}

    @router.get('/{project_id}/holders')
    async def holders(project_id:str):
        p=await get_project(project_id)
        distribution=[4.8,3.7,2.9,2.4,1.9,1.7,1.4,1.2,.9,.8]
        return {'total':p['holders'],'items':[{'rank':i+1,'label':f'Sample holder {i+1:03}','percentage':weight,'quantity':p['supply']*weight/100,'value_usd':p['market_cap']*weight/100} for i,weight in enumerate(distribution)],'data_mode':'illustrative'}
    return router