import { useState } from 'react';
import axios from 'axios';

export default function RoomManager({ onCreate }) {
  const [name, setName] = useState('');

  const handleCreate = async () => {
    const res = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/rooms`, { name });
    onCreate(res.data);
  };

  return (
    <div>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Room name" />
      <button onClick={handleCreate}>Create Room</button>
    </div>
  );
}
