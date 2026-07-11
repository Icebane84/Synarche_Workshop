
import {NexusBus3,SignalId} from "./NexusBus3";
const bus=new NexusBus3();
bus.on(SignalId.EnemyHit,()=>{});
const t=Date.now();
for(let f=0;f<600;f++){for(let i=0;i<1000;i++)bus.emit(SignalId.EnemyHit,{attacker:1,victim:2,damage:3});bus.flush();}
console.log("Elapsed(ms)",Date.now()-t,bus.diagnostics);
