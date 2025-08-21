import { useEffect, useState } from "react";
import { io } from "socket.io-client";

export function useSocket() {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Conectar al backend
    const s = io(import.meta.env.VITE_BACKEND_URL, {
      transports: ["websocket"], // fuerza WebSocket
      autoConnect: true,
    });

    setSocket(s);

    // Limpiar conexión al desmontar
    return () => {
      s.disconnect();
    };
  }, []);

  return socket;
}
