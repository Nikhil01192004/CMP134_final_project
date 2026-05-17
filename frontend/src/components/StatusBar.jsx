import React from 'react';

export default function StatusBar({ status, connected, signalLost }) {
  const battery = status?.battery ?? '—';
  const robotStatus = status?.status ?? 'Unknown';
  const batteryLow = typeof battery === 'number' && battery < 20;

  return (
    <div className="card">
      <h3 style={{ marginBottom: 12 }}>📊 Robot Status</h3>
      <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
        {/* Battery */}
        <div>
          <div style={{ fontSize: 12, color: '#94a3b8' }}>Battery</div>
          <div style={{ fontSize: 22, fontWeight: 700, color: batteryLow ? '#ef4444' : '#4ade80' }}>
            {typeof battery === 'number' ? `${battery}%` : battery}
          </div>
          {batteryLow && (
            <div style={{ color: '#ef4444', fontSize: 12, fontWeight: 600 }}>⚠️ LOW BATTERY</div>
          )}
        </div>

        {/* Status */}
        <div>
          <div style={{ fontSize: 12, color: '#94a3b8' }}>Status</div>
          <div style={{ fontSize: 16, fontWeight: 600 }}>{robotStatus}</div>
        </div>

        {/* Connection */}
        <div>
          <div style={{ fontSize: 12, color: '#94a3b8' }}>Connection</div>
          <span className={`badge ${signalLost ? 'badge-red' : connected ? 'badge-green' : 'badge-yellow'}`}>
            {signalLost ? 'SIGNAL LOST' : connected ? 'CONNECTED' : 'CONNECTING...'}
          </span>
        </div>
      </div>
    </div>
  );
}
