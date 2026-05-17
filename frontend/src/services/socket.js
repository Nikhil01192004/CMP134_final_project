/**
 * WebSocket connection manager for live telemetry.
 * Implements Observer pattern — components subscribe to updates.
 */

const WS_URL = `ws://${window.location.host}/ws/telemetry`;

let ws = null;
let reconnectTimer = null;
const listeners = new Set();

function notify(data) {
  listeners.forEach((fn) => fn(data));
}

export function subscribeTelemetry(callback) {
  listeners.add(callback);
  return () => listeners.delete(callback);
}

export function connectWebSocket(token) {
  if (ws && ws.readyState === WebSocket.OPEN) return;

  ws = new WebSocket(`${WS_URL}?token=${token}`);

  ws.onopen = () => {
    console.log('WebSocket connected');
    notify({ type: 'connected' });
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      notify(data);
    } catch {
      console.warn('Invalid WS message', event.data);
    }
  };

  ws.onclose = (event) => {
    // Code 1008 = server rejected the token — don't loop, notify app to re-login
    if (event.code === 1008) {
      console.error('WebSocket auth rejected (1008) — token invalid or expired');
      notify({ type: 'auth_failed' });
      return;
    }
    console.warn('WebSocket closed — reconnecting in 3s');
    notify({ type: 'signal_lost' });
    reconnectTimer = setTimeout(() => connectWebSocket(token), 3000);
  };

  ws.onerror = (err) => {
    console.error('WebSocket error', err);
    ws.close();
  };
}

export function disconnectWebSocket() {
  clearTimeout(reconnectTimer);
  if (ws) ws.close();
  ws = null;
}
