import React, { useState } from 'react';
import axios from 'axios';

const getCsrfToken = () => {
  const token = document.querySelector('meta[name="csrf-token"]');
  return token ? token.getAttribute('content') : '';
};

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState<{ email: string; userType: string } | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/login/',
        { email, password },
        {
          headers: {
            'X-CSRFToken': getCsrfToken(),
          },
        }
      );

      setLoading(false);

      if (response.data.status === 'success') {
        setLoggedIn(true);
        setUserInfo({ email, userType: response.data.userType });
      } else {
        setError('Invalid email or password');
      }
    } catch (err) {
      setLoading(false);
      setError('Login failed');
    }
  };

  const handleSignOut = () => {
    setLoggedIn(false);
    setUserInfo(null);
  };

  if (loggedIn && userInfo) {
    return (
      <div>
        <p>Logged in as {userInfo.email} ({userInfo.userType})</p>
        <button onClick={handleSignOut}>Sign Out</button>
      </div>
    );
  }

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <button type="submit">Login</button>
        )}
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default LoginForm;
