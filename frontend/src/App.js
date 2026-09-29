import {useEffect,useState} from 'react';
import {BrowserRouter,Routes,Route,useNavigate,useParams} from 'react-router-dom';
import {MotionConfig} from 'framer-motion';
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';
import {Toaster} from 'sonner';
import {Lock,Wallet,ArrowRight} from 'lucide-react';
import {api} from './lib/api';
import {Header} from './components/Header';
import {Hero} from './components/Hero';
import {HowItWorks} from './components/HowItWorks';
import {BagIndex} from './components/BagIndex';
import {Carry} from './components/Carry';
import {Economy} from './components/Economy';
import {Leaderboard} from './components/Leaderboard';
import {Footer} from './components/Footer';
import {LaunchFlow} from './components/LaunchFlow';
import {ProjectDetail} from './components/ProjectDetail';
import {Dialog,DialogContent,DialogTitle,DialogDescription} from './components/ui/dialog';
import './App.css';
import './sections.css';
import './dialogs.css';

function Home(){
 const[launch,setLaunch]=useState(false),[wallet,setWallet]=useState(false),[data,setData]=useState({}),[error,setError]=useState(false),[retry,setRetry]=useState(0);const navigate=useNavigate();const {id}=useParams();
 useEffect(()=>{if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;const lenis=new Lenis({autoRaf:true,duration:1.1,smoothWheel:true,anchors:{offset:-100}});return()=>lenis.destroy();},[]);
 useEffect(()=>{let active=true;Promise.all([api.get('/overview'),api.get('/global'),api.get('/native')]).then(([overview,global,native])=>{if(active){setData({overview:overview.data,global:global.data,native:native.data});setError(false);}}).catch(()=>active&&setError(true));return()=>{active=false;};},[retry]);
 const openProject=id=>navigate(`/bags/${id}`);
 return <><a href="#main" className="skip-link" data-testid="skip-to-content">Skip to content</a><Header onLaunch={()=>setLaunch(true)} onWallet={()=>setWallet(true)}/><main id="main"><Hero onLaunch={()=>setLaunch(true)}/>{error&&<div className="data-error page-width" data-testid="ecosystem-error">We couldn't load the ecosystem. <button className="text-link" onClick={()=>setRetry(r=>r+1)} data-testid="ecosystem-retry">Try again</button></div>}<HowItWorks overview={data.overview}/><BagIndex onOpen={openProject}/><Carry onOpen={openProject}/><Economy global={data.global} native={data.native}/><Leaderboard onOpen={openProject}/><Footer onLaunch={()=>setLaunch(true)}/></main><LaunchFlow open={launch} onClose={()=>setLaunch(false)}/><ProjectDetail id={id} onClose={()=>navigate('/')}/><Dialog open={wallet} onOpenChange={setWallet}><DialogContent className="paper-dialog wallet-dialog" data-testid="wallet-dialog" data-lenis-prevent><span className="wallet-illustration"><Wallet size={33}/></span><DialogTitle data-testid="wallet-modal-heading">Your wallet. Your call.</DialogTitle><DialogDescription data-testid="wallet-modal-copy">Wallet connections will open with live Pump.fun launches. For now, you can pack an idea without connecting or signing anything.</DialogDescription><div className="preview-box" data-testid="wallet-unavailable"><Lock size={16}/> No live connection. No funds move.</div><button className="button primary full" data-testid="wallet-create-draft" onClick={()=>{setWallet(false);setLaunch(true);}}>Start a token draft <ArrowRight size={16}/></button></DialogContent></Dialog><Toaster position="bottom-right" toastOptions={{style:{background:'#faf7ed',color:'#2c2923',border:'1px solid #d8d0bc',fontFamily:'DM Sans'}}}/></>;
}
export default function App(){return <MotionConfig reducedMotion="user"><BrowserRouter><Routes><Route path="/" element={<Home/>}/><Route path="/bags/:id" element={<Home/>}/><Route path="*" element={<Home/>}/></Routes></BrowserRouter></MotionConfig>;}