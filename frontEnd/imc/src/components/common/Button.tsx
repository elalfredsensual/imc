import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Button.css'; // Import styles for the button

interface ButtonProps {
  text: string;
  to: string;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({ text, to, onClick }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const isActive = location.pathname === to;

  const handleClick = () => {
    if (onClick) {
      onClick();
    }
    navigate(to);
  };

  return (
    <button onClick={handleClick} className={`nav-button ${isActive ? 'active' : ''}`}>
      {text}
    </button>
  );
};

export { Button };
