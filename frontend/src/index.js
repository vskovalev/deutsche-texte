import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Определяем базовый URL API в зависимости от среды
const API_URL = process.env.NODE_ENV === 'production' 
  ? process.env.REACT_APP_API_URL || 'http://backend:8000' 
  : 'http://localhost:8000';

// Делаем глобально доступным (для удобства в компонентах)
window.API_URL = API_URL;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Измеряем производительность (опционально)
reportWebVitals();