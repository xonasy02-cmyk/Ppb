import {useState,useEffect} from 'react';
import {Link,useLocation} from 'react-router-dom';
import {Menu,X,ArrowUpRight,Wallet} from 'lucide-react';
export const Header=({onWallet})=>{
 const[open,setOpen]=useState(false);const location=useLocation();
 useEffect(()=>setOpen(false),[location]);
 const nav=[['Bags','/bags','bags'],['Carry','/ecosystem#carry','carry'],['Global Bag','/ecosystem#global-bag','global-bag'],['Leaderboard','/leaderboard','leaderboard'],['$PAPERBAG','/ecosystem#paperbag','paperbag']];
 return <header className="site-header" data-testid="site-header"><div className="header-inner">
  <Link to="/" className="brand" aria-label="Paperbag home" data-testid="brand-home"><img src="/bag-mark.svg" alt=""/><span>PAPERBAG<small>EVERY TOKEN CARRIES A BAG.</small></span></Link>
  <nav className={open?'main-nav is-open':'main-nav'} aria-label="Main navigation" data-testid="main-navigation"><Link to="/launch" className={location.pathname==='/launch'?'nav-active':''} data-testid="nav-launch">Launch <ArrowUpRight size={13}/></Link>{nav.map(([name,url,id])=><Link to={url} key={id} className={location.pathname+location.hash===url?'nav-active':''} data-testid={`nav-${id}`}>{name}</Link>)}</nav>
  <div className="header-buttons"><button className="button wallet-button" data-testid="connect-wallet" onClick={onWallet}><Wallet size={15}/><span>Connect Wallet</span></button><button className="menu-button" aria-label={open?'Close menu':'Open menu'} aria-expanded={open} onClick={()=>setOpen(!open)} data-testid="mobile-menu-toggle">{open?<X/>:<Menu/>}</button></div>
 </div></header>;
};