import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function RoomManager() {
  const [name, setName] = useState('');
  const navigate = useNavigate();

  const handleCreate = async () => {
    try {
      const res = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/rooms`,
        { name }
      );
      // Navegar a la sala creada
      navigate(`/room/${res.data.id}`);
    } catch (err) {
      console.error("Error creating room:", err);
    }
  };

  return (
    <div>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Room name"
      />
      <button onClick={handleCreate}>Create Room</button>
    </div>
  );
}
