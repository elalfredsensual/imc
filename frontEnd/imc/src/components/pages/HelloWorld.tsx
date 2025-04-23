import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface HelloWorldResponse {
  message: string;
}

const HelloWorld: React.FC = () => {
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    axios.get<HelloWorldResponse>('http://localhost:8000/api/hello-world/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Hello, World!</h1>
      <p>{message}</p>
    </div>
  );
}

export default HelloWorld;
