import {useEffect,useState} from 'react';
import {BrowserRouter,Routes,Route,Outlet,Navigate,useNavigate,useParams,useLocation} from 'react-router-dom';
import {MotionConfig} from 'framer-motion';
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';
import {Toaster} from 'sonner';
import {Lock,Wallet,ArrowRight} from 'lucide-react';
import {Header} from './components/Header';
import {Footer} from './components/Footer';
import {Dialog,DialogContent,DialogTitle,DialogDescription} from './components/ui/dialog';
import {HomePage,BagsPage,EcosystemPage,LeaderboardPage,LaunchPage,NotFoundPage} from './pages/SitePages';
import TokenPage from './pages/TokenPage';
import './App.css';
import './sections.css';
import './dialogs.css';
import './market.css';
import './trading.css';

function Layout(){
 const[wallet,setWallet]=useState(false);const navigate=useNavigate();const{pathname,hash}=useLocation();
 useEffect(()=>{
  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // React Router handles cross-page hashes after the destination has mounted.
  // Lenis must not resolve /ecosystem#carry against the page we are leaving.
  const lenis=!reduce&&!pathname.startsWith('/token/')?new Lenis({autoRaf:true,duration:1.05,smoothWheel:true,anchors:false}):null;
  window.scrollTo({top:0,behavior:'instant'});
  const timer=setTimeout(()=>{if(hash){const target=document.getElementById(hash.slice(1));if(target){if(lenis)lenis.scrollTo(target,{offset:-30,immediate:true});else target.scrollIntoView();}}},200);
  return()=>{clearTimeout(timer);lenis?.destroy();};
 },[pathname,hash]);
 return <><a href="#main" className="skip-link" data-testid="skip-to-content">Skip to content</a><Header onWallet={()=>setWallet(true)}/><main id="main"><Outlet/></main><Footer compact={pathname.startsWith('/token/')||pathname==='/launch'}/><Dialog open={wallet} onOpenChange={setWallet}><DialogContent className="paper-dialog wallet-dialog" data-testid="wallet-dialog" data-lenis-prevent><span className="wallet-illustration"><Wallet size={33}/></span><DialogTitle data-testid="wallet-modal-heading">Your wallet. Your call.</DialogTitle><DialogDescription data-testid="wallet-modal-copy">Live wallet connections open with the protocol. For now, explore tokens and try buys and sells with a simulated balance. No wallet or real funds needed.</DialogDescription><div className="preview-box" data-testid="wallet-unavailable"><Lock size={16}/> No live connection. No real funds move.</div><button className="button primary full" data-testid="wallet-explore-trading" onClick={()=>{setWallet(false);navigate('/bags');}}>Explore practice trading <ArrowRight size={16}/></button><button className="text-link" data-testid="wallet-create-draft" onClick={()=>{setWallet(false);navigate('/launch');}}>Or start a token draft <ArrowRight size={14}/></button></DialogContent></Dialog><Toaster position="bottom-right" toastOptions={{style:{background:'#faf7ed',color:'#2c2923',border:'1px solid #d8d0bc',fontFamily:'DM Sans'}}}/></>;
}
const LegacyToken=()=>{const{id}=useParams();return <Navigate to={`/token/${id}`} replace/>;};
export default function App(){return <MotionConfig reducedMotion="user"><BrowserRouter><Routes><Route element={<Layout/>}><Route path="/" element={<HomePage/>}/><Route path="/bags" element={<BagsPage/>}/><Route path="/token/:id" element={<TokenPage/>}/><Route path="/bags/:id" element={<LegacyToken/>}/><Route path="/launch" element={<LaunchPage/>}/><Route path="/ecosystem" element={<EcosystemPage/>}/><Route path="/leaderboard" element={<LeaderboardPage/>}/><Route path="/carry" element={<Navigate to="/ecosystem#carry" replace/>}/><Route path="/global-bag" element={<Navigate to="/ecosystem#global-bag" replace/>}/><Route path="/paperbag" element={<Navigate to="/ecosystem#paperbag" replace/>}/><Route path="*" element={<NotFoundPage/>}/></Route></Routes></BrowserRouter></MotionConfig>;}