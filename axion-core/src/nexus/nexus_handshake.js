js
/**
 * @nexus/: Hardened Shared Central Engine (v3.1.0)
 * @shield/: Integrated Cryptographic Handshake
 */
const connections = new Map(); // Track ports + Auth status
let stateVector = { syncCount: 0, lastEvent: "BOOT_SUCCESS", securityLevel: "SIVC_ACTIVE" };

const SYSTEMIC_SECRET = "PHOENIX_INIT_VECTOR_001"; // Pre-shared Key

onconnect = (e) => {
  const port = e.ports[0];
  const portId = crypto.randomUUID().slice(0, 8);
  
  // 1. Initial State: UNAUTHORIZED
  connections.set(port, { id: portId, authorized: false });

  port.onmessage = async (msg) => {
    const { type, payload, signature } = msg.data;
    const portData = connections.get(port);

    // 2. Handshake Verification Logic (@shield)
    if (type === 'HANDSHAKE_RESPONSE') {
      const expected = await deriveKey(payload.challenge);
      if (signature === expected) {
        portData.authorized = true;
        port.postMessage({ type: 'AUTH_SUCCESS', payload: stateVector });
      } else {
        port.postMessage({ type: 'AUTH_FAIL', msg: "Invalid Signature" });
        port.close();
      }
      return;
    }

    // 3. Unauthorized Command Blocking
    if (!portData.authorized) return;

    // 4. Authorized @system Logic
    if (type === 'SYNC') stateVector.syncCount++;
    stateVector.lastEvent = type;

    broadcast({ type: 'STATE_UPDATE', payload: { state: stateVector, origin: portData.id } });
  };

  // 5. Issue Challenge
  const challenge = crypto.randomUUID();
  port.postMessage({ type: 'AUTH_CHALLENGE', challenge });
};

async function deriveKey(challenge) {
  const encoder = new TextEncoder();
  const data = encoder.encode(challenge + SYSTEMIC_SECRET);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(hash)));
}

function broadcast(msg) {
  for (const [port, data] of connections) {
    if (data.authorized) port.postMessage(msg);
  }
}