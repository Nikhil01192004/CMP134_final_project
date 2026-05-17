import React, {
  useEffect,
  useState,
  useCallback,
} from 'react';

import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

import {
  getRobotStatus,
  getRobotMap,
  getLogs,
} from '../services/api';

import {
  connectWebSocket,
  disconnectWebSocket,
  subscribeTelemetry,
} from '../services/socket';

import GridMap from '../components/GridMap';
import StatusBar from '../components/StatusBar';
import CommandPanel from '../components/CommandPanel';
import AuditLog from '../components/AuditLog';

export default function Dashboard() {

  const {
    token,
    role,
    username,
    logout,
  } = useAuth();

  const navigate = useNavigate();

  const [status, setStatus] = useState(null);
  const [mapData, setMapData] = useState(null);

  const [robotPosition, setRobotPosition] = useState({
    x: 0,
    y: 0,
  });

  const [logs, setLogs] = useState([]);

  const [signalLost, setSignalLost] = useState(false);
  const [connected, setConnected] = useState(false);

  const fetchData = useCallback(async () => {

    try {

      const [
        statusRes,
        mapRes,
        logsRes,
      ] = await Promise.all([
        getRobotStatus(),
        getRobotMap(),
        getLogs(),
      ]);

      setStatus(statusRes.data);
      setMapData(mapRes.data);

      if (statusRes.data?.position) {
        setRobotPosition(statusRes.data.position);
      }

      setLogs(logsRes.data);

      setSignalLost(false);

    } catch (err) {

      console.error('Dashboard fetch error:', err);

      if (err.response?.status === 401) {
        logout();
        navigate('/login');
      }

      if (err.response?.status === 503) {
        setSignalLost(true);
      }
    }

  }, [logout, navigate]);

  useEffect(() => {

    fetchData();

    connectWebSocket(token);

    const unsub = subscribeTelemetry((data) => {

      console.log('Telemetry:', data);

      if (data.type === 'auth_failed') {

        logout();
        navigate('/login');

      } else if (data.type === 'signal_lost') {

        setSignalLost(true);
        setConnected(false);

      } else if (data.type === 'connected') {

        setSignalLost(false);
        setConnected(true);

      } else {

        setSignalLost(false);
        setConnected(true);

        if (data.position) {
          setRobotPosition(data.position);
        }

        setStatus((prev) => ({
          ...(prev || {}),
          battery:
            data.battery !== undefined
              ? data.battery
              : prev?.battery,

          status:
            data.status || prev?.status,
        }));
      }
    });

    const interval = setInterval(
      fetchData,
      5000
    );

    return () => {
      unsub();
      disconnectWebSocket();
      clearInterval(interval);
    };

  }, [
    token,
    fetchData,
    logout,
    navigate,
  ]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleCommandSent = () => {
    fetchData();
  };

  return (
    <div className="container">

      {/* Header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 20,
        }}
      >

        <h1>🤖 Robot Dashboard</h1>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
          }}
        >

          <span
            className={`badge ${
              role === 'commander'
                ? 'badge-green'
                : 'badge-yellow'
            }`}
          >
            {role?.toUpperCase()}
          </span>

          <span>{username}</span>

          <button
            className="btn-danger"
            onClick={handleLogout}
          >
            Logout
          </button>

        </div>
      </div>

      {/* Signal Lost Banner */}
      {signalLost && (
        <div
          className="signal-lost"
          style={{ marginBottom: 16 }}
        >
          ⚠️ SIGNAL LOST — Reconnecting to robot...
        </div>
      )}

      {/* Dashboard Layout */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 16,
        }}
      >

        {/* Left Side */}
        <div>

          <StatusBar
            status={status}
            connected={connected}
            signalLost={signalLost}
          />

          <GridMap
            mapData={mapData}
            robotPosition={robotPosition}
          />

        </div>

        {/* Right Side */}
        <div>

          {role === 'commander' && (
            <CommandPanel
              onCommandSent={handleCommandSent}
              signalLost={signalLost}
              robotPosition={robotPosition}
              mapData={mapData}
            />
          )}

          <AuditLog logs={logs} />

        </div>

      </div>
    </div>
  );
}