import React from 'react';

const GRID_SIZE = 21;

export default function GridMap({ mapData, robotPosition }) {
  const grid = mapData?.grid || [];
  const robotPos = robotPosition || { x: 0, y: 0 };

  return (
    <div className="card">
      <h3 style={{ marginBottom: 12 }}>📍 Grid Map (21×21)</h3>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${GRID_SIZE}, 1fr)`,
          gap: 1,
          aspectRatio: '1',
          background: '#0f172a',
          borderRadius: 8,
          overflow: 'hidden',
        }}
      >
        {Array.from({ length: GRID_SIZE * GRID_SIZE }).map((_, idx) => {
          const col = idx % GRID_SIZE;
          const row = Math.floor(idx / GRID_SIZE);

          const isRobot = col === robotPos.x && row === robotPos.y;
          const isObstacle = grid[row] && grid[row][col] === 1;
          const isCenter = col === 0 && row === 0;

          let bg = '#1e293b';
          let content = '';

          if (isRobot) {
            bg = '#2563eb';
            content = '🤖';
          } else if (isObstacle) {
            bg = '#dc2626';
            content = '⛔';
          } else if (isCenter) {
            bg = '#334155';
          }

          return (
            <div
              key={idx}
              title={`(${col}, ${row})`}
              style={{
                background: bg,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 10,
                aspectRatio: '1',
              }}
            >
              {content}
            </div>
          );
        })}
      </div>
    </div>
  );
}
