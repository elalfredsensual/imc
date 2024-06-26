import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router } from 'react-router-dom';
import LoginForm from './components/pages/LoginForm';
import LoggedInApp from './components/pages/LoggedInApp';

function App() {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);
  const [userInfo, setUserInfo] = useState<{ email: string; userType: string } | null>(null);

  useEffect(() => {
    const storedUserInfo = localStorage.getItem('userInfo');
    if (storedUserInfo) {
      setUserInfo(JSON.parse(storedUserInfo));
      setLoggedIn(true);
    }
  }, []);

  const handleLogin = (userData: { email: string; userType: string }) => {
    setLoggedIn(true);
    setUserInfo(userData);
    localStorage.setItem('userInfo', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setLoggedIn(false);
    setUserInfo(null);
    localStorage.removeItem('userInfo');
  };

  return (
    <Router>
      {!loggedIn ? (
        <LoginForm onLogin={handleLogin} />
      ) : (
        <LoggedInApp handleLogout={handleLogout} userInfo={userInfo} />
      )}
    </Router>
  );
}

export default App;
