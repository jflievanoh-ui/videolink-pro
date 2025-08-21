// src/main.jsx

import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css"; // 👈 importa tus estilos de Tailwind

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
