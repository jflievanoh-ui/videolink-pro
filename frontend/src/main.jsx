// src/main.jsx

import React from 'react';
import { createRoot } from 'react-dom/client';

import App from './App';

// Import global CSS (if you have any)
// import './index.css';   // <-- uncomment if you created an index.css file

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
