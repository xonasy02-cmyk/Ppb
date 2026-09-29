def make_project(id, name, ticker, asset, target_sol, target, progress, mode, status, pnl, cycle, volume, hours, color, icon):
    amount = round(target*progress/100, 4)
    history = [{'cycle':n,'amount':target,'asset':asset if mode=='SHARE' else ticker,'status':'SHARED' if mode=='SHARE' else 'BURNED'} for n in range(cycle-1,0,-1)]
    return dict(id=id,name=name,ticker=ticker,asset=asset,target_sol=target_sol,asset_target=target,asset_amount=amount,progress=progress,mode=mode,carry_status=status,carry_pnl=pnl,carry_added=max(pnl,0),cycle=cycle,volume=volume,fastest_hours=hours,color=color,icon=icon,history=history,data_mode='illustrative',description=f'A little {name.lower()} energy. A whole lot of possibility. Trading activity fills this Bag, one cycle at a time.')

PROJECTS = [
    make_project('dog','Good Dog','DOG','DOGE',10,1000000,74.2,'SHARE','Active',1.37,3,2400000,2.4,'#f3ddaa','dog'),
    make_project('cat','Paper Cat','CAT','SOL',5,5,31,'BURN','Idle',-0.12,2,840000,5.1,'#e3dded','cat'),
    make_project('ape','Bag Ape','APE','USDC',20,3000,92,'SHARE','Active',2.84,6,1800000,1.8,'#d9e4cc','ape'),
    make_project('bonk','Bonk in a Bag','BONK','BONK',8,80000000,58,'SHARE','Active',0.82,4,1260000,3.2,'#f1c9b6','bonk'),
    make_project('pepe','Packed Pepe','PEPE','SHIB',12,160000000,46,'BURN','Idle',0.24,5,680000,4.6,'#dbe7d2','pepe'),
    make_project('wif','Dog with a Bag','WIF','SOL',15,15,86,'SHARE','Active',1.92,3,960000,2.1,'#e8dcc7','wif'),
]
VAULTS = [{'asset':'DOGE','amount':42800,'color':'#e8c86d'},{'asset':'SOL','amount':18.42,'color':'#c9c0df'},{'asset':'USDC','amount':3240,'color':'#accade'},{'asset':'BONK','amount':12500000,'color':'#e5b19b'}]