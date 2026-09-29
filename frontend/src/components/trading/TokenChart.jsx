import {useEffect,useRef,useState} from 'react';
import {createChart,CandlestickSeries,HistogramSeries,LineSeries,ColorType} from 'lightweight-charts';
import {Maximize2,ChartCandlestick} from 'lucide-react';
import {api} from '../../lib/api';

export const TokenChart=({project:p})=>{
 const host=useRef(null),chartRef=useRef(null);const[timeframe,setTimeframe]=useState('15m'),[metric,setMetric]=useState('price'),[type,setType]=useState('candles'),[data,setData]=useState(null),[error,setError]=useState(false),[loading,setLoading]=useState(true),[retry,setRetry]=useState(0),[hover,setHover]=useState(null);
 useEffect(()=>{let active=true;setLoading(true);setHover(null);api.get(`/market/${p.id}/candles`,{params:{timeframe}}).then(r=>{if(active){setData(r.data);setError(false);}}).catch(()=>active&&setError(true)).finally(()=>active&&setLoading(false));return()=>{active=false;};},[p.id,timeframe,retry]);
 useEffect(()=>{
  if(!data||!host.current)return;
  const chart=createChart(host.current,{autoSize:true,localization:{locale:'en-US'},layout:{background:{type:ColorType.Solid,color:'#fffcf5'},textColor:'#918674',fontFamily:'DM Sans',fontSize:10,attributionLogo:true},grid:{vertLines:{color:'#eee8da'},horzLines:{color:'#eee8da'}},rightPriceScale:{borderColor:'#e2dac7',scaleMargins:{top:.08,bottom:.24}},timeScale:{borderColor:'#e2dac7',timeVisible:true,secondsVisible:false,rightOffset:4},crosshair:{mode:0,vertLine:{color:'#a8997c',labelBackgroundColor:'#5d5343'},horzLine:{color:'#a8997c',labelBackgroundColor:'#5d5343'}},handleScroll:{mouseWheel:false,pressedMouseMove:true,horzTouchDrag:true,vertTouchDrag:false},handleScale:{mouseWheel:true,pinch:true,axisPressedMouseMove:true}});
  chartRef.current=chart;const multiplier=metric==='mcap'?p.supply:1;
  const priceFormat=metric==='mcap'?{type:'volume'}:{type:'price',precision:8,minMove:.00000001};
  const series=type==='candles'?chart.addSeries(CandlestickSeries,{upColor:'#688e6b',downColor:'#c17865',borderVisible:false,wickUpColor:'#688e6b',wickDownColor:'#c17865',priceFormat}):chart.addSeries(LineSeries,{color:'#7c8d53',lineWidth:2,priceFormat});
  series.setData(data.candles.map(c=>type==='candles'?{time:c.time,open:c.open*multiplier,high:c.high*multiplier,low:c.low*multiplier,close:c.close*multiplier}:{time:c.time,value:c.close*multiplier}));
  const volume=chart.addSeries(HistogramSeries,{priceFormat:{type:'volume'},priceScaleId:'volume'});
  volume.priceScale().applyOptions({scaleMargins:{top:.83,bottom:0}});
  volume.setData(data.candles.map(c=>({time:c.time,value:c.volume,color:c.close>=c.open?'#bccdb388':'#ddbaad88'})));
  chart.timeScale().fitContent();chart.subscribeCrosshairMove(param=>{const c=data.candles.find(c=>c.time===param.time);setHover(c||null);});
  return()=>{chartRef.current=null;chart.remove();};
 },[data,metric,type,p.supply]);
 const current=hover||data?.candles?.at(-1);const number=n=>n?.toFixed(7);
 return <section className="token-chart-panel" data-testid="token-chart-panel">
  <div className="chart-heading"><div><ChartCandlestick size={16}/><strong>{p.ticker}/SOL</strong><span>Pump.fun / PF</span></div><div className="chart-metric-switch">{[['price','Price'],['mcap','Market cap']].map(([id,name])=><button key={id} onClick={()=>setMetric(id)} aria-pressed={metric===id} data-testid={`chart-metric-${id}`}>{name}</button>)}</div></div>
  <div className="chart-toolbar"><div className="chart-timeframes">{['1m','5m','15m','1h','4h'].map(tf=><button key={tf} onClick={()=>setTimeframe(tf)} className={timeframe===tf?'selected':''} data-testid={`chart-timeframe-${tf}`}>{tf}</button>)}</div><select aria-label="Chart type" value={type} onChange={e=>setType(e.target.value)} data-testid="chart-type"><option value="candles">Candles</option><option value="line">Line</option></select><button onClick={()=>chartRef.current?.timeScale().fitContent()} className="icon-button" aria-label="Fit chart to data" data-testid="chart-fit"><Maximize2 size={13}/></button></div>
  <div className="chart-ohlc" data-testid="chart-ohlc">{current?<><span>O <b>{number(current.open)}</b></span><span>H <b>{number(current.high)}</b></span><span>L <b>{number(current.low)}</b></span><span>C <b className={current.close>=current.open?'positive':'negative'}>{number(current.close)}</b></span></>:<span>Loading candles...</span>}<small>USD</small></div>
  <div className="chart-stage" data-testid="candlestick-chart" data-lenis-prevent><div ref={host} className="chart-canvas"/>{loading&&<div className="chart-overlay" data-testid="chart-loading">Unpacking the chart...</div>}{error&&<div className="chart-overlay" data-testid="chart-error">Chart unavailable.<button className="text-link" onClick={()=>setRetry(v=>v+1)} data-testid="chart-retry">Try again</button></div>}</div>
  <div className="chart-caption" data-testid="chart-data-notice"><span><i/> ILLUSTRATIVE PRICE HISTORY · NOT LIVE</span><a href="https://www.tradingview.com/" target="_blank" rel="noreferrer" data-testid="chart-attribution">Charts by TradingView</a></div>
 </section>;
};