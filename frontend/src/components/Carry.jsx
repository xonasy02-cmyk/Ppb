import {useEffect,useState} from 'react';
import {motion,AnimatePresence,useReducedMotion} from 'framer-motion';
import {ArrowUpRight,ArrowRight,Pause,Play,ScanLine} from 'lucide-react';
import {Reveal,TokenAvatar} from './BagArt';

const nodes=[
 {id:'dog',ticker:'DOG',icon:'dog',color:'#f3ddaa',volume:'$2.4M'},
 {id:'cat',ticker:'CAT',icon:'cat',color:'#e3dded',volume:'$840K'},
 {id:'ape',ticker:'APE',icon:'ape',color:'#d9e4cc',volume:'$1.8M'},
 {id:'bonk',ticker:'BONK',icon:'bonk',color:'#f1c9b6',volume:'$1.3M'}
];
const phases=[['Looking for activity...','Scanning the ecosystem'],['Working on $DOG','Following activity. Not hype.'],['Buy. Carry. Sell.','Closing the example trade'],['+0.82 SOL realized','Added to DOGE Bag'],['Back to work.','A little more in the Bag.']];

export const Carry=({onOpen})=>{
 const[phase,setPhase]=useState(0),[paused,setPaused]=useState(false);
 const reduced=useReducedMotion();
 useEffect(()=>{
  if(paused||reduced)return;
  const t=setInterval(()=>setPhase(p=>(p+1)%5),3000);
  return()=>clearInterval(t);
 },[paused,reduced]);

 return <section id="carry" className="section page-width" data-testid="carry-section">
  <Reveal className="carry-section-inner">
   <div className="carry-copy">
    <span className="eyebrow"><i className="status-dot"/> A LITTLE HELP. A LITTLE CARRY.</span>
    <h2 data-testid="carry-heading">MEET<br/><span>CARRY.</span><span className="carry-asterisk">✳</span></h2>
    <p className="carry-lead" data-testid="carry-tagline">Working for the ecosystem.<br/>One Bag at a time.</p>
    <p data-testid="carry-description">Carry puts Paperbag revenue to work across active projects. More activity can mean more Carry. Only realized profit makes it back into a project's Bag.</p>
    <a className="text-link light" href="#economy" data-testid="carry-how-link">See how it connects <ArrowRight size={16}/></a>
    <div className="carry-disclaimer" data-testid="carry-risk">Carry takes risk. Profit isn't promised.<br/>Your Bag is never guaranteed to fill.</div>
   </div>
   <div className="carry-map-wrap">
    <div className="map-heading"><span className="eyebrow">CARRY AT WORK</span><span className="small-label">ILLUSTRATIVE SEQUENCE</span><button aria-label={paused?'Play Carry animation':'Pause Carry animation'} aria-pressed={paused} onClick={()=>setPaused(!paused)} data-testid="carry-pause" className="icon-button">{paused?<Play size={14}/>:<Pause size={14}/>}</button></div>
    <div className={`carry-map phase-${phase} ${paused||reduced?'is-paused':''}`}>
     <svg className="map-lines" viewBox="0 0 500 330" preserveAspectRatio="none" aria-hidden="true">
      <path d="M100 70 250 165 400 70M250 165 100 270M250 165 400 270"/>
      <circle className="carry-trail-dot" cx="250" cy="165" r="4" fill="#a38c58"/>
     </svg>
     {nodes.map((p,i)=><button key={p.id} className={`project-node node-${i} ${phase>0&&phase<4&&i===0?'node-active':''}`} data-testid={`carry-node-${p.id}`} onClick={()=>onOpen(p.id)}><TokenAvatar project={p} small/><strong>${p.ticker}</strong><small>{p.volume} vol.</small>{i===0&&phase===3&&<motion.span className="profit-drop" initial={{y:-15,opacity:0}} animate={{y:0,opacity:1}}>+0.82 SOL</motion.span>}</button>)}
     <motion.div className="carry-character" animate={{x:phase===1||phase===2?-48:0,y:phase===1||phase===2?-35:0,rotate:phase===1?-8:0}} transition={{duration:1.5,ease:'easeInOut'}}>
      <div className="scan-ring"/><img src="/bag-mark.svg" alt="Carry, Paperbag's little ecosystem helper"/><span>CARRY <ScanLine size={11}/></span>
     </motion.div>
     <div className="map-note hand-note">always on the lookout ↗</div>
    </div>
    <AnimatePresence mode="wait"><motion.div key={phase} className="carry-status" initial={{opacity:0,y:7}} animate={{opacity:1,y:0}} exit={{opacity:0}} data-testid="carry-animation-status"><span className="status-dot"/><div><b>{phases[phase][0]}</b><small>{phases[phase][1]}</small></div><ArrowUpRight size={18}/></motion.div></AnimatePresence>
   </div>
  </Reveal>
 </section>;
};