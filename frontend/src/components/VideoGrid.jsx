import { useEffect, useRef } from 'react';
import { useSocket } from '../hooks/useSocket';

export default function VideoGrid({ roomId }) {
  const socket = useSocket();
  const localVideoRef = useRef();

  useEffect(() => {
    // Join room
    socket.emit('join_room', { sid: socket.id, room_id: roomId });

    // Get local media
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(stream => {
        if (localVideoRef.current) localVideoRef.current.srcObject = stream;
      });

    // Handle incoming peers
    socket.on('joined', async ({ room }) => {
      console.log(`Joined ${room}`);
    });

    return () => socket.disconnect();
  }, [socket, roomId]);

  return (
    <div className="grid">
      <video ref={localVideoRef} autoPlay muted playsInline />
      {/* Remote videos will be appended via dynamic IDs */}
    </div>
  );
}
