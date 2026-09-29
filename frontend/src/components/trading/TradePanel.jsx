import {useState} from 'react';
import {ArrowDownUp,ArrowUpRight,RotateCcw,FlaskConical,CheckCircle2} from 'lucide-react';
import {api,amount,compact,errorText} from '../../lib/api';
import {toast} from 'sonner';

export const TradePanel=({project:p,simulation,onUpdate,onReset,initializing,simError,onRetry})=>{
 const[side,setSide]=useState('buy'),[value,setValue]=useState('1'),[busy,setBusy]=useState(false),[error,setError]=useState(''),[fill,setFill]=useState(null);
 const position=simulation?.positions?.[p.id];const held=position?.quantity||0;const balance=simulation?.balance_sol||0;
 const numeric=Number(value),valid=Number.isFinite(numeric)&&numeric>0;
 const estimate=valid?(side==='buy'?numeric/p.price_sol:numeric*p.price_sol):0;
 const switchSide=s=>{setSide(s);setValue('');setError('');setFill(null);};
 const submit=async e=>{e.preventDefault();if(!simulation||busy)return;if(!valid){setError('Enter an amount greater than zero.');return;}setBusy(true);setError('');setFill(null);try{const r=await api.post(`/simulations/${simulation.id}/orders`,{project_id:p.id,side,amount:numeric,request_id:crypto.randomUUID()});onUpdate(r.data.simulation);setFill(r.data.trade);setValue('');toast.success(`Simulated ${side} filled. No real funds moved.`);}catch(e){setError(errorText(e));}finally{setBusy(false);}};
 return <section className="trade-panel" id="trade" data-testid="trade-panel"><div className="practice-heading"><FlaskConical size={14}/><strong>PRACTICE TRADING</strong><span>SIMULATION</span></div><div className="trade-side-tabs"><button className={side==='buy'?'selected buy':''} onClick={()=>switchSide('buy')} data-testid="trade-buy-tab">Buy ${p.ticker}</button><button className={side==='sell'?'selected sell':''} onClick={()=>switchSide('sell')} data-testid="trade-sell-tab">Sell ${p.ticker}</button></div>
  <div className="practice-balance" data-testid="simulation-balance"><span>Practice balance</span><strong>{initializing?'Loading...':simulation?`${amount(balance)} SOL`:'Unavailable'}</strong></div>
  {simError&&<div className="trade-error" data-testid="simulation-error">Couldn't load your practice balance.<button className="text-link" onClick={onRetry} data-testid="simulation-retry">Try again</button></div>}
  <form onSubmit={submit} data-testid="trade-form"><label className="trade-input-label" htmlFor="trade-amount">{side==='buy'?'You pay':'You sell'}<span>{side==='sell'?`${compact(held)} ${p.ticker} available`:'Simulated SOL'}</span></label><div className="trade-amount-input"><input id="trade-amount" data-testid="trade-amount" type="number" min="0" step="any" inputMode="decimal" placeholder="0.00" value={value} onChange={e=>{setValue(e.target.value);setError('');setFill(null);}} aria-describedby="trade-disclaimer"/><span>{side==='buy'?'SOL':p.ticker}</span></div>
   <div className="trade-presets">{(side==='buy'?[.1,.5,1,5]:[25,50,75,100]).map(n=><button type="button" key={`${side}-${n}`} data-testid={`trade-preset-${n}`} onClick={()=>{setValue(side==='buy'?String(n):String(n===100?held:Math.floor(held*n/100*1e8)/1e8));setError('');setFill(null);}}>{side==='buy'?`${n} SOL`:`${n}%`}</button>)}</div>
   <div className="trade-receive" data-testid="trade-estimate"><span><ArrowDownUp size={12}/> You receive (est.)</span><strong>{estimate?amount(estimate):'0'} <small>{side==='buy'?p.ticker:'SOL'}</small></strong></div>
   <div className="trade-quote-details" data-testid="trade-quote-details"><div><span>Price</span><span>${p.price_usd.toFixed(7)}</span></div><div><span>Network fees / slippage</span><span>None in simulation</span></div></div>
   {error&&<div className="trade-error" role="alert" data-testid="trade-error">{error}</div>}
   <button type="submit" className={`trade-submit ${side}`} disabled={!simulation||busy||initializing||!valid||(side==='sell'&&held===0)} data-testid="trade-submit">{busy?'Placing practice order...':`Simulate ${side} ${p.ticker}`}<ArrowUpRight size={16}/></button>
  </form>
  {fill&&<div className="trade-fill" role="status" data-testid="trade-success"><CheckCircle2 size={17}/><div><strong>Simulated {fill.side} complete</strong><span>{amount(fill.quantity)} {p.ticker} · {amount(fill.sol_amount)} SOL</span></div></div>}
  <p className="trade-disclaimer" id="trade-disclaimer" data-testid="trade-disclaimer">100 virtual SOL to try the flow. Fixed sample prices. No wallet, real tokens, or real money. Practice trades don't change market data or Bag progress.</p>
  <div className="your-position" data-testid="your-position"><div><strong>Your practice position</strong><span>{p.ticker}</span></div><dl><div><dt>Tokens held</dt><dd data-testid="position-quantity">{amount(held)}</dd></div><div><dt>Value</dt><dd data-testid="position-value">{amount(held*p.price_sol)} SOL</dd></div><div><dt>Total cost</dt><dd data-testid="position-cost">{amount(position?.cost_sol||0)} SOL</dd></div><div><dt>Realized P&L</dt><dd data-testid="position-realized-pnl">{Math.abs(position?.realized_pnl_sol||0)<.00000001?'0':amount(position.realized_pnl_sol)} SOL</dd></div></dl></div>
  <button className="reset-simulation" onClick={()=>{if(window.confirm('Reset your practice balance to 100 SOL? All your simulated positions and trades will be removed.'))onReset();}} disabled={busy||initializing} data-testid="reset-simulation"><RotateCcw size={11}/> Reset practice balance</button>
 </section>;
};