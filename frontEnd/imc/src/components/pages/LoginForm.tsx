import React, { useState } from 'react';
import axios from 'axios';
import { Container, Form, Button, Alert, Spinner } from 'react-bootstrap';
import './LoginForm.css'; // Import custom CSS

const getCsrfToken = () => {
  const token = document.querySelector('meta[name="csrf-token"]');
  return token ? token.getAttribute('content') : '';
};

interface LoginFormProps {
  onLogin: (userData: { email: string; userType: string }) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

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
        onLogin({ email, userType: response.data.userType });
      } else {
        setError('Invalid email or password');
      }
    } catch (err) {
      setLoading(false);
      setError('Login failed');
    }
  };

  return (
    <Container className="mt-5 login-container">
      <div className="login-header">
        <h2>Login to your account</h2>
        <p>Enter your details to login.</p>
      </div>
      <Form onSubmit={handleLogin}>
        <Form.Group controlId="formEmail">
          <Form.Label className="text-center d-block">Email</Form.Label>
          <Form.Control
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            className="input-field"
          />
        </Form.Group>
        <Form.Group controlId="formPassword" className="mt-3">
          <Form.Label className="text-center d-block">Password</Form.Label>
          <Form.Control
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            className="input-field"
          />
        </Form.Group>
        <div className="mt-3 d-grid">
          {loading ? (
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          ) : (
            <Button type="submit" className="btn-lg">Login</Button>
          )}
        </div>
      </Form>
      {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
    </Container>
  );
};

export default LoginForm;
