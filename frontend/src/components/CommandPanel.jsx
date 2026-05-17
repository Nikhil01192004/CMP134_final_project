import React, { useState, useRef } from 'react';
import { moveRobot } from '../services/api';

/** BFS pathfinding on a 21x21 grid. Returns array of {x,y} steps or null if no path. */
function findPath(grid, start, goal) {
  if (!grid || grid.length === 0) return null;
  const key = (x, y) => `${x},${y}`;
  const queue = [{ ...start, path: [] }];
  const visited = new Set([key(start.x, start.y)]);

  while (queue.length > 0) {
    const { x, y, path } = queue.shift();
    if (x === goal.x && y === goal.y) return path;

    for (const [dx, dy] of [[0,-1],[0,1],[-1,0],[1,0]]) {
      const nx = x + dx, ny = y + dy;
      if (nx < 0 || ny < 0 || nx > 20 || ny > 20) continue;
      if (grid[ny] && grid[ny][nx] === 1) continue;
      if (visited.has(key(nx, ny))) continue;
      visited.add(key(nx, ny));
      queue.push({ x: nx, y: ny, path: [...path, { x: nx, y: ny }] });
    }
  }
  return null;
}

export default function CommandPanel({ onCommandSent, signalLost, robotPosition, mapData }) {
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [pathInfo, setPathInfo] = useState('');
  const abortRef = useRef(false);

  const sendMove = async (targetX, targetY) => {
    setError('');
    setResult(null);
    setLoading(true);
    try {
      const res = await moveRobot(targetX, targetY);
      setResult(res.data);
      onCommandSent();
    } catch (err) {
      setError(err.response?.data?.detail || 'Move command failed');
    } finally {
      setLoading(false);
    }
  };

  const handleStep = (dx, dy) => {
    const nx = Math.min(20, Math.max(0, (robotPosition?.x ?? 0) + dx));
    const ny = Math.min(20, Math.max(0, (robotPosition?.y ?? 0) + dy));
    sendMove(nx, ny);
  };

  const handleNavigate = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setPathInfo('');

    const goal = { x: parseInt(x), y: parseInt(y) };
    const start = robotPosition || { x: 0, y: 0 };
    const grid = mapData?.grid;

    if (start.x === goal.x && start.y === goal.y) {
      setError('Robot is already at that position.');
      return;
    }

    if (grid && grid[goal.y] && grid[goal.y][goal.x] === 1) {
      setError('Destination is an obstacle — choose a free cell.');
      return;
    }

    const path = findPath(grid, start, goal);
    if (!path || path.length === 0) {
      setError('No path found — destination is completely blocked by obstacles.');
      return;
    }

    setLoading(true);
    setPathInfo(`Navigating ${path.length} steps...`);
    abortRef.current = false;

    for (const step of path) {
      if (abortRef.current) {
        setPathInfo('Navigation cancelled.');
        break;
      }
      try {
        await moveRobot(step.x, step.y);
        onCommandSent();
        setPathInfo(`Moving... (${step.x}, ${step.y})`);
        await new Promise((r) => setTimeout(r, 400));
      } catch (err) {
        setError(err.response?.data?.detail || 'Move failed mid-path');
        break;
      }
    }

    setLoading(false);
    setPathInfo('');
    if (!abortRef.current) setResult({ arrived: `(${goal.x}, ${goal.y})` });
  };

  const handleCancel = () => { abortRef.current = true; };

  const btnStyle = {
    width: 42, height: 42, fontSize: 18, background: '#334155', color: '#e0e0e0',
    border: '1px solid #475569', borderRadius: 6,
    cursor: loading || signalLost ? 'not-allowed' : 'pointer',
    opacity: loading || signalLost ? 0.5 : 1,
  };

  return (
    <div className="card">
      <h3 style={{ marginBottom: 12 }}>🎮 Command Panel <span className="badge badge-green">COMMANDER</span></h3>

      <div style={{ marginBottom: 14 }}>
        <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 6 }}>Step (1 cell at a time)</div>
        <div style={{ display: 'grid', gridTemplateColumns: '42px 42px 42px', gap: 4, width: 'fit-content', margin: '0 auto' }}>
          <div />
          <button style={btnStyle} disabled={loading || signalLost} onClick={() => handleStep(0, -1)}>↑</button>
          <div />
          <button style={btnStyle} disabled={loading || signalLost} onClick={() => handleStep(-1, 0)}>←</button>
          <button style={{ ...btnStyle, background: '#1e293b', cursor: 'default' }} disabled>·</button>
          <button style={btnStyle} disabled={loading || signalLost} onClick={() => handleStep(1, 0)}>→</button>
          <div />
          <button style={btnStyle} disabled={loading || signalLost} onClick={() => handleStep(0, 1)}>↓</button>
          <div />
        </div>
      </div>

      <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 6 }}>Auto-navigate to destination (avoids obstacles)</div>
      <form onSubmit={handleNavigate}>
        <div style={{ display: 'flex', gap: 10, marginBottom: 12 }}>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: 12, color: '#94a3b8' }}>X (0–20)</label>
            <input type="number" min={0} max={20} value={x} onChange={(e) => setX(e.target.value)} required />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: 12, color: '#94a3b8' }}>Y (0–20)</label>
            <input type="number" min={0} max={20} value={y} onChange={(e) => setY(e.target.value)} required />
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn-primary" style={{ flex: 1 }} disabled={loading || signalLost}>
            {loading ? pathInfo || 'Moving...' : signalLost ? 'Signal Lost' : '🧭 Navigate'}
          </button>
          {loading && (
            <button type="button" onClick={handleCancel} style={{ padding: '0 14px', background: '#7f1d1d', color: '#fca5a5', border: 'none', borderRadius: 6, cursor: 'pointer' }}>Stop</button>
          )}
        </div>
      </form>

      {error && <div style={{ marginTop: 10, background: '#7f1d1d', color: '#fca5a5', padding: 8, borderRadius: 6 }}>{error}</div>}
      {result && !error && (
        <div style={{ marginTop: 10, background: '#14532d', color: '#86efac', padding: 8, borderRadius: 6 }}>
          ✅ Arrived at {result.arrived}
        </div>
      )}
    </div>
  );
}
