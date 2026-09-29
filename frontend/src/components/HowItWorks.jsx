import {useEffect,useState} from 'react';
import {motion,AnimatePresence,useReducedMotion} from 'framer-motion';
import {ArrowRight} from 'lucide-react';
import {BagArt,Reveal} from './BagArt';
import {compact} from '../lib/api';
const stages=['Launch','Trade','Fill the Bag','Open the Bag','Reset'];
export const HowItWorks=({overview})=>{
 const[stage,setStage]=useState(0);const reduced=useReducedMotion();
 useEffect(()=>{if(reduced)return;const timer=setInterval(()=>setStage(s=>(s+1)%5),2400);return()=>clearInterval(timer);},[reduced]);
 return <>
  <div className="stats-strip page-width" data-testid="ecosystem-overview">
   <span className="stats-caption">A LITTLE ECOSYSTEM.<br/><strong>A LOT TO CARRY.</strong><small>Illustrative preview</small></span>
   {[['Projects packing',overview?.projects?.toString().padStart(2,'0')],['Bags opened',overview?.bags_opened],['Ecosystem volume',overview?`$${compact(overview.volume)}`:null],['Carry added',overview?`${overview.carry_profit} SOL`:null]].map(([label,value],i)=><div className="stat" key={label} data-testid={`overview-stat-${i}`}><strong>{value??'—'}</strong><span>{label}</span></div>)}
  </div>
  <section className="section page-width how-section" id="how-it-works" data-testid="how-it-works">
   <Reveal className="how-copy"><span className="eyebrow">SIMPLE BY DESIGN</span><h2 data-testid="how-heading">Not just a token.<br/>A Bag that gives back.</h2><p data-testid="how-description">Trading activity fills your Bag. When it's full, it opens. Good things go to your holders. Then we do it all again.</p><span className="hand-note" data-testid="how-note">fill it. open it. do it again.</span></Reveal>
   <Reveal className="cycle-panel">
    <div className="cycle-visual"><div className="cycle-orbit"/>
     <BagArt progress={[0,25,74,100,0][stage]} open={stage===3} animate/>
     {stage===3&&<div className="opening-coins">{['◎','Ð','✳'].map((c,i)=><motion.span key={i} initial={{opacity:0,y:30,x:0}} animate={{opacity:[0,1,0],y:-75,x:(i-1)*70}} transition={{duration:2,delay:i*.2}}>{c}</motion.span>)}</div>}
     <AnimatePresence mode="wait"><motion.div key={stage} className="cycle-status" initial={{opacity:0,y:5}} animate={{opacity:1,y:0}} exit={{opacity:0}} data-testid="cycle-animation-status"><i className="status-dot"/>{['A new idea. An empty Bag.','Packed with activity.','Your Bag is filling.','Bag full. Sharing the good stuff.','A fresh Bag. A new cycle.'][stage]}</motion.div></AnimatePresence>
    </div>
    <div className="cycle-steps" data-testid="cycle-steps">{stages.map((s,i)=><button className={stage===i?'active':''} key={s} onClick={()=>setStage(i)} data-testid={`cycle-step-${i}`}><span>0{i+1}</span>{s}{i<4&&<ArrowRight size={11}/>}</button>)}</div>
   </Reveal>
  </section>
 </>;
};