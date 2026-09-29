import {useEffect,useState,useCallback} from 'react';
import {api} from './api';
const KEY='paperbag-simulation-id';
let pending=null;
async function restore(){
 const id=localStorage.getItem(KEY);
 if(id){try{return (await api.get(`/simulations/${id}`)).data;}catch(e){if(e.response?.status!==404&&e.response?.status!==422)throw e;localStorage.removeItem(KEY);}}
 const response=await api.post('/simulations');localStorage.setItem(KEY,response.data.id);return response.data;
}
function getSimulation(){if(!pending)pending=restore().finally(()=>{pending=null;});return pending;}
export const useSimulation=()=>{
 const[simulation,setSimulation]=useState(null),[initializing,setInitializing]=useState(true),[error,setError]=useState(false),[attempt,setAttempt]=useState(0);
 useEffect(()=>{let active=true;setInitializing(true);getSimulation().then(s=>{if(active){setSimulation(s);setError(false);}}).catch(()=>active&&setError(true)).finally(()=>active&&setInitializing(false));return()=>{active=false;};},[attempt]);
 const reset=useCallback(async()=>{setInitializing(true);try{const previous=simulation?.id;const r=await api.post('/simulations');localStorage.setItem(KEY,r.data.id);setSimulation(r.data);setError(false);if(previous)await api.delete(`/simulations/${previous}`);}catch{setError(true);}finally{setInitializing(false);}},[simulation?.id]);
 return {simulation,onUpdate:setSimulation,onReset:reset,initializing,simError:error,onRetry:()=>setAttempt(a=>a+1)};
};