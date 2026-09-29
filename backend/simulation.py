"""Paper trading only: fake SOL, no wallet, no network calls, no actual token mint.

A simulation ID identifies anonymous toy data, not an authenticated account.
One Mongo document stores balances, positions and fills; optimistic updates prevent
concurrent overspending. Idempotent request IDs prevent duplicate executions.
"""
import uuid
from datetime import datetime,timezone
from decimal import Decimal, ROUND_DOWN
from typing import Literal
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field,ConfigDict
from pymongo import ReturnDocument

class Position(BaseModel):
    quantity:float=0
    cost_sol:float=0
    realized_pnl_sol:float=0

class SimTrade(BaseModel):
    id:str
    request_id:str
    project_id:str
    side:Literal['buy','sell']
    input_amount:float
    quantity:float
    sol_amount:float
    price_usd:float
    price_sol:float
    executed_at:str
    realized_pnl_sol:float
    is_simulated:bool=True

class Simulation(BaseModel):
    model_config=ConfigDict(extra='ignore')
    id:str
    balance_sol:float
    initial_balance_sol:float=100
    positions:dict[str,Position]
    trades:list[SimTrade]
    version:int
    created_at:str
    is_simulated:bool=True

class OrderInput(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    project_id:str=Field(min_length=1,max_length=40)
    side:Literal['buy','sell']
    amount:float=Field(gt=0,le=1e15)
    request_id:uuid.UUID

class OrderResult(BaseModel):
    trade:SimTrade
    simulation:Simulation
    is_simulated:bool=True

def decimal(value): return Decimal(str(value))
def truncate(value, places='0.00000001'): return value.quantize(Decimal(places),rounding=ROUND_DOWN)

def create_simulation_router(db):
    router=APIRouter(prefix='/api/simulations')

    @router.post('',response_model=Simulation,status_code=201)
    async def create():
        state=Simulation(id=str(uuid.uuid4()),balance_sol=100,positions={},trades=[],version=0,created_at=datetime.now(timezone.utc).isoformat())
        await db.simulations.insert_one(state.model_dump())
        return state

    async def read(simulation_id):
        state=await db.simulations.find_one({'id':simulation_id},{'_id':0})
        if not state: raise HTTPException(404,'Simulation not found. Start a new practice balance.')
        return state

    @router.get('/{simulation_id}',response_model=Simulation)
    async def get(simulation_id:uuid.UUID):
        return await read(str(simulation_id))

    @router.post('/{simulation_id}/orders',response_model=OrderResult)
    async def order(simulation_id:uuid.UUID,data:OrderInput):
        project=await db.projects.find_one({'id':data.project_id},{'_id':0})
        if not project: raise HTTPException(404,'Token not found')
        sid=str(simulation_id)
        for _ in range(6):
            state=await read(sid)
            for existing in state['trades']:
                if existing['request_id']==str(data.request_id):
                    if existing['project_id']!=data.project_id or existing['side']!=data.side or existing['input_amount']!=data.amount:
                        raise HTTPException(409,'This order ID was already used for a different trade')
                    return OrderResult(trade=existing,simulation=state)
            if len(state['trades'])>=500:
                raise HTTPException(409,'This practice account has reached 500 trades. Start a new simulation.')
            price=decimal(project['price_sol'])
            position=state['positions'].get(data.project_id,{'quantity':0,'cost_sol':0,'realized_pnl_sol':0})
            held,cost=decimal(position['quantity']),decimal(position['cost_sol'])
            balance=decimal(state['balance_sol'])
            amount=decimal(data.amount)
            pnl=Decimal('0')
            if data.side=='buy':
                sol=truncate(amount,'0.000000001')
                if sol<Decimal('0.000001'): raise HTTPException(422,'Minimum simulated buy is 0.000001 SOL')
                if sol>balance: raise HTTPException(422,'Not enough simulated SOL')
                quantity=truncate(sol/price)
                if quantity<=0: raise HTTPException(422,'Trade amount is too small')
                new_held,new_cost=held+quantity,cost+sol
                new_balance=balance-sol
            else:
                quantity=truncate(amount)
                if quantity<=0: raise HTTPException(422,'Enter a token amount greater than zero')
                if quantity>held: raise HTTPException(422,'Not enough simulated tokens to sell')
                if held<=0: raise HTTPException(422,'Buy some simulated tokens before selling')
                sol=truncate(quantity*price,'0.000000001')
                released_cost=cost*quantity/held
                pnl=sol-released_cost
                new_held,new_cost=held-quantity,cost-released_cost
                new_balance=balance+sol
            new_position=Position(quantity=float(new_held),cost_sol=float(new_cost),realized_pnl_sol=float(decimal(position['realized_pnl_sol'])+pnl))
            trade=SimTrade(id=str(uuid.uuid4()),request_id=str(data.request_id),project_id=data.project_id,side=data.side,input_amount=data.amount,quantity=float(quantity),sol_amount=float(sol),price_usd=project['price_usd'],price_sol=float(price),executed_at=datetime.now(timezone.utc).isoformat(),realized_pnl_sol=float(pnl))
            changes={'balance_sol':float(new_balance),'positions':{**state['positions'],data.project_id:new_position.model_dump()},'trades':[trade.model_dump(),*state['trades']],'version':state['version']+1}
            updated=await db.simulations.find_one_and_update({'id':sid,'version':state['version']},{'$set':changes},projection={'_id':0},return_document=ReturnDocument.AFTER)
            if updated: return OrderResult(trade=trade,simulation=updated)
        raise HTTPException(409,'Another trade is being processed. Please retry.')

    @router.delete('/{simulation_id}',status_code=204)
    async def remove(simulation_id:uuid.UUID):
        await db.simulations.delete_one({'id':str(simulation_id)})
    return router