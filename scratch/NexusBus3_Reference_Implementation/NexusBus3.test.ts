
import {NexusBus3,SignalId} from "./NexusBus3";
const bus=new NexusBus3();
let hit=0;
bus.on(SignalId.PlayerLanded,p=>{if(p.id===1) hit++;});
bus.emit(SignalId.PlayerLanded,{id:1});
bus.flush();
console.assert(hit===1,"dispatch failed");
console.log("Basic tests passed");
