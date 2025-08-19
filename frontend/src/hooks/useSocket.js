import { useEffect, useRef } from 'react';
import io from 'socket.io-client';

export function useSocket(url = process.env.VITE_BACKEND_URL) {
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = io(url, { transports: ['websocket'] });

    return () => {
      if (socketRef.current) socketRef.current.disconnect();
    };
  }, [url]);

  return socketRef.current;
}
