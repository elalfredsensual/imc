import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import MainPage from '../layouts/mainPage';
import Quote from './Quote';
import Partners from './Partner';
import HelloWorld from './HelloWorld';

interface LoggedInAppProps {
  handleLogout: () => void;
  userInfo: { email: string; userType: string } | null;
}

const LoggedInApp: React.FC<LoggedInAppProps> = ({ handleLogout, userInfo }) => {
  const navigate = useNavigate();

  return (
    <>
      <div className="logged-in-info">
        Logged in as {userInfo?.email} <button onClick={() => { handleLogout(); navigate('/'); }}>Sign Out</button>
      </div>
      <MainPage>
        <div>
          <Routes>
            <Route path="/quote" element={<Quote />} />
            <Route path="/partners" element={<Partners />} />
          </Routes>
        </div>
      </MainPage>
    </>
  );
};

export default LoggedInApp;
