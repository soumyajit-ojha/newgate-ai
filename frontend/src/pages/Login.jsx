import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Login = () => {
  const navigate = useNavigate();

  const handleSuccess = async (credentialResponse) => {
    try {
      console.log("Google Token:", credentialResponse.credential);
      const res = await api.post('/google', {
        credential: credentialResponse.credential
      });
      localStorage.setItem('access_token', res.data.access_token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/dashboard');
    } catch (error) {
      console.error("Login Failed:", error);
      alert("Login failed! Check console.");
    }
  };

  return (
    <div className="flex-center">
      <div className="glass-card">
        {/* Decorative Icon */}
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✨</div>
        
        <h1>Newgate AI</h1>
        <p className="subtitle">
          Turn your imagination into reality.<br/>
          Sign in to start creating.
        </p>
        
        {/* We wrap the button to make it look clean on dark mode */}
        <div className="google-btn-wrapper">
            <GoogleLogin
                onSuccess={handleSuccess}
                onError={() => console.log('Login Failed')}
                theme="outline" 
                size="large"
                shape="rectangular"
            />
        </div>
      </div>
    </div>
  );
};

export default Login;