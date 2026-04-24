/**
 * @nexus/: Shared Central Engine (v3.0.0)
 * Persistent State Orchestrator for the Multi-Nexus.
 */
const connections = [];
let stateVector = {
  themeHue: 210,
  syncCount: 0,
  lastEvent: "INITIALIZED"
};

/**
 * @system/: Causal Synthesis Loop
 * $V_{Pulse} \leftrightarrow V_{Lore} \rightarrow TMR_{Event}$
 */
const evaluateTMR = (state) => {
  if (state.syncCount >= 10 && state.lastEvent !== 'TMR_UPGRADE') {
    state.lastEvent = 'TMR_UPGRADE';
    state.criticality = 'PHOENIX_LEVEL';
    return true;
  }
  return false;
};

onconnect = (e) => {
  const port = e.ports[0];
  connections.push(port);

  port.onmessage = (msg) => {
    const { type, payload, origin } = msg.data;

    // @system/: Handle client disconnect to prevent memory leaks
    if (type === 'DISCONNECT') {
      const index = connections.indexOf(port);
      if (index > -1) connections.splice(index, 1);
      return;
    }

    // @system/: Update Central State
    if (type === 'SYNC') stateVector.syncCount++;
    if (type === 'THEME' && payload !== undefined) stateVector.themeHue = payload.hue;
    stateVector.lastEvent = type;

    // @system/: Correlate Pulse with Lore
    const tmrTriggered = evaluateTMR(stateVector);

    // @atlas/: Synchronize all connected Nexus points
    connections.forEach(p => {
      p.postMessage({
        type: tmrTriggered ? 'TMR_EVENT' : 'STATE_UPDATE',
        payload: { 
          state: stateVector, 
          origin, 
          tmr: tmrTriggered ? "AOP-PGPS-UPGRADE-ALPHA" : null,
          timestamp: Date.now() 
        }
      });
    });
  };

  // Immediate handshake on connection
  port.postMessage({ type: 'HANDSHAKE', payload: stateVector });
};

/**
 * @nexus/: Hardened Shared Central Engine (v3.2.0)
 * @archive/: SELT Ledger Compression Protocol
 */
const ARCHIVE_LIMIT = 1000;
let systemicLedger = []; // Persistent SELT Repository

onconnect = (e) => {
  const port = e.ports[0];
  // ... [Previous Handshake Logic] ...

  port.onmessage = async (msg) => {
    const { type, payload } = msg.data;

    // 1. Operational Logic
    if (type === 'SYNC') {
      const entry = Archive.createEntry('STATE_SYNC', 'SUCCESS');
      Archive.store(entry);
    }

    // 2. Transmit Archive Summary to Nexus
    port.postMessage({ 
      type: 'ARCHIVE_SUMMARY', 
      payload: { count: systemicLedger.length, lastEntry: systemicLedger[0] } 
    });
  };
};

const Archive = {
  createEntry: (event, status) => ({
    id: crypto.randomUUID().slice(0, 8),
    ts: Date.now(),
    ev: event,
    st: status
  }),

  /**
   * @system/: Ledger Compression Engine
   * Reduces JSON footprint by mapping repetitive keys.
   */
  store: (entry) => {
    systemicLedger.unshift(entry);
    
    // Maintain Systemic Boundaries (FIFO)
    if (systemicLedger.length > ARCHIVE_LIMIT) {
      systemicLedger.pop();
    }

    // Persistence with Compression
    const compressed = btoa(JSON.stringify(systemicLedger));
    localStorage.setItem('syn_compressed_ledger', compressed);
  }
};