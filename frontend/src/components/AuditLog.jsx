import React from 'react';

export default function AuditLog({ logs }) {
  return (
    <div className="card">
      <h3 style={{ marginBottom: 12 }}>📋 Mission Audit Log</h3>
      <div style={{ maxHeight: 400, overflowY: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #334155', textAlign: 'left' }}>
              <th style={{ padding: '8px 6px' }}>Time</th>
              <th style={{ padding: '8px 6px' }}>User</th>
              <th style={{ padding: '8px 6px' }}>Command</th>
              <th style={{ padding: '8px 6px' }}>Response</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan={4} style={{ padding: 16, textAlign: 'center', color: '#64748b' }}>
                  No logs yet
                </td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.id} style={{ borderBottom: '1px solid #1e293b' }}>
                  <td style={{ padding: '6px', whiteSpace: 'nowrap', color: '#94a3b8' }}>
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td style={{ padding: '6px' }}>{log.username}</td>
                  <td style={{ padding: '6px', fontFamily: 'monospace' }}>{log.command}</td>
                  <td style={{ padding: '6px', fontSize: 11, color: '#94a3b8', maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {log.response}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
