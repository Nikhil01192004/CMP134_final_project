import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '../services/api';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('viewer');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await registerUser({ username, password, role });
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
      <div className="card" style={{ width: 380 }}>
        <h2 style={{ marginBottom: 20, textAlign: 'center' }}>🤖 Robot Management</h2>
        <h3 style={{ marginBottom: 16, textAlign: 'center' }}>Create Account</h3>
        {error && <div style={{ background: '#7f1d1d', color: '#fca5a5', padding: 10, borderRadius: 6, marginBottom: 12 }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 12 }}>
            <label>Username</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} required minLength={3} />
          </div>
          <div style={{ marginBottom: 12 }}>
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={6} />
          </div>
          <div style={{ marginBottom: 16 }}>
            <label>Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              style={{ width: '100%', padding: '10px 14px', borderRadius: 6, background: '#1e293b', color: '#e0e0e0', border: '1px solid #334155', fontSize: 14 }}
            >
              <option value="viewer">Viewer</option>
              <option value="commander">Commander</option>
            </select>
          </div>
          <button className="btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Creating...' : 'Register'}
          </button>
        </form>
        <p style={{ marginTop: 16, textAlign: 'center' }}>
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  );
}
