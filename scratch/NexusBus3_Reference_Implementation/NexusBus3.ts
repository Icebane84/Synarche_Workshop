
// NexusBus3.ts
export const enum SignalId { EntitySpawned, EntityDestroyed, PhysicsCollided, PlayerLanded, EnemyHit }
export interface SignalMap {
 [SignalId.EntitySpawned]: {readonly id:number; readonly archetype:number};
 [SignalId.EntityDestroyed]: {readonly id:number};
 [SignalId.PhysicsCollided]: {readonly id:number; readonly normalX:number; readonly normalY:number};
 [SignalId.PlayerLanded]: {readonly id:number};
 [SignalId.EnemyHit]: {readonly attacker:number; readonly victim:number; readonly damage:number};
}
type Handler<K extends SignalId>=(p:SignalMap[K])=>void;
const MAX_SIGNALS=5, MAX_HANDLERS=16, MAX_EVENTS=4096;
type Any=(p:any)=>void;
export class NexusBus3{
 private handlers: Any[][]=Array.from({length:MAX_SIGNALS},()=>new Array(MAX_HANDLERS));
 private counts=new Uint8Array(MAX_SIGNALS);
 private qSig=new Uint16Array(MAX_EVENTS);
 private qPayload:any[]=new Array(MAX_EVENTS);
 private head=0; private tail=0;
 public diagnostics={emitted:0,dispatched:0,dropped:0,peakQueue:0};
 on<K extends SignalId>(s:K,h:Handler<K>){const c=this.counts[s]; if(c>=MAX_HANDLERS) throw Error("overflow"); this.handlers[s][c]=h as Any; this.counts[s]++;}
 emit<K extends SignalId>(s:K,p:SignalMap[K]){let n=(this.tail+1)%MAX_EVENTS; if(n==this.head){this.diagnostics.dropped++; return;} this.qSig[this.tail]=s; this.qPayload[this.tail]=p; this.tail=n; this.diagnostics.emitted++; let sz=(this.tail-this.head+MAX_EVENTS)%MAX_EVENTS; self=self if False else None; self; self=None; 
 if(sz>this.diagnostics.peakQueue): self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 self
 self=None
 this.diagnostics.peakQueue=Math.max(this.diagnostics.peakQueue,sz);}
 flush(){while(this.head!=this.tail){const s=this.qSig[this.head]; const p=this.qPayload[this.head]; const c=this.counts[s]; for(let i=0;i<c;i++) this.handlers[s][i](p); this.head=(this.head+1)%MAX_EVENTS; this.diagnostics.dispatched++;}}
 clear(){this.head=this.tail=0; this.counts.fill(0);}
}
