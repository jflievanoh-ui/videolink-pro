import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RoomManager from './components/RoomManager';
import VideoGrid from './components/VideoGrid';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RoomManager />} />
        <Route path="/room/:id" element={<VideoGrid />} />
      </Routes>
    </BrowserRouter>
  );
}
