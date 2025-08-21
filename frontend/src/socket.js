// src/socket.js
import { io } from "socket.io-client";

const isProd = import.meta.env.PROD;
const BACKEND_URL = isProd
  ? "https://videolink-backend.onrender.com"
  : "http://localhost:10000";

const socket = io(BACKEND_URL, {
  path: "/socket.io",       // coincide con tu backend
  transports: ["websocket"], // solo WebSocket
  withCredentials: true,
  autoConnect: false,        // conectar manualmente
});

// Funciones de conexión
export const connectSocket = () => socket.connect();
export const disconnectSocket = () => socket.disconnect();

// Funciones de room/WebRTC
export const joinRoom = (roomId) => socket.emit("join_room", { room_id: roomId });
export const sendOffer = (data) => socket.emit("offer", data);
export const sendAnswer = (data) => socket.emit("answer", data);
export const sendIceCandidate = (data) => socket.emit("ice_candidate", data);

// Listeners
export const onOffer = (callback) => socket.on("offer", callback);
export const onAnswer = (callback) => socket.on("answer", callback);
export const onIceCandidate = (callback) => socket.on("ice-candidate", callback);
export const onConnect = (callback) => socket.on("connect", callback);
export const onDisconnect = (callback) => socket.on("disconnect", callback);

export default socket;
