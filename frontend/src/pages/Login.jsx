import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { loginUser } from '../services/api';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError('');
    setLoading(true);

    try {
      const res = await loginUser({
        username,
        password,
      });

      login(
        res.data.access_token,
        res.data.role,
        username
      );

      navigate('/');

    } catch (err) {

      console.error('Login error:', err);

      const detail = err?.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(detail[0]?.msg || 'Login failed');
      } else if (typeof detail === 'string') {
        setError(detail);
      } else {
        setError('Login failed');
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
      }}
    >
      <div
        className="card"
        style={{
          width: 380,
          padding: 24,
        }}
      >
        <h2
          style={{
            marginBottom: 20,
            textAlign: 'center',
          }}
        >
          🤖 Robot Management
        </h2>

        <h3
          style={{
            marginBottom: 16,
            textAlign: 'center',
          }}
        >
          Sign In
        </h3>

        {error && (
          <div
            style={{
              background: '#7f1d1d',
              color: '#fca5a5',
              padding: 10,
              borderRadius: 6,
              marginBottom: 12,
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>

          <div style={{ marginBottom: 12 }}>
            <label>Username</label>

            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label>Password</label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            className="btn-primary"
            style={{ width: '100%' }}
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

        </form>

        <p
          style={{
            marginTop: 16,
            textAlign: 'center',
          }}
        >
          No account?{' '}
          <Link to="/register">
            Register
          </Link>
        </p>

      </div>
    </div>
  );
}