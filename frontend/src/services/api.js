import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});


// -------------------------------------------------------------------
// AUTH
// -------------------------------------------------------------------

// REGISTER (JSON is correct)
export const registerUser = (data) =>
  api.post('/auth/register', data);


// LOGIN (FIXED: supports FastAPI Form OR JSON safely)
export const loginUser = (data) => {
  const form = new URLSearchParams();
  form.append('username', data.username);
  form.append('password', data.password);

  return api.post('/auth/login', form, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
};


// -------------------------------------------------------------------
// ROBOT
// -------------------------------------------------------------------

export const getRobotStatus = () =>
  api.get('/robot/status');

export const getRobotMap = () =>
  api.get('/robot/map');

export const getRobotSensor = () =>
  api.get('/robot/sensor');

export const moveRobot = (x, y) =>
  api.post('/robot/move', { x, y });


// -------------------------------------------------------------------
// LOGS
// -------------------------------------------------------------------

export const getLogs = (limit = 100) =>
  api.get(`/logs/?limit=${limit}`);

export default api;