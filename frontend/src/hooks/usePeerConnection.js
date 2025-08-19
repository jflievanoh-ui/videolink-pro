import { useEffect, useState } from 'react';

const ICE_SERVERS = [
  { urls: "stun:stun.l.google.com:19302" },
  // Add TURN if you host one
];

export function usePeerConnection(socket) {
  const [peerConnections, setPCs] = useState({}); // sid -> RTCPeerConnection

  const createConnection = async (remoteSid, isInitiator) => {
    const pc = new RTCPeerConnection({ iceServers: ICE_SERVERS });

    pc.onicecandidate = ({ candidate }) => {
      if (!candidate) return;
      socket.emit('ice_candidate', { sid: remoteSid, payload: { candidate } });
    };

    // Handle remote tracks
    pc.ontrack = (e) => {
      const stream = e.streams[0];
      // Attach to <video> element by ID or ref
      document.getElementById(`remote-${remoteSid}`).srcObject = stream;
    };

    setPCs(prev => ({ ...prev, [remoteSid]: pc }));

    if (isInitiator) {
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);
      socket.emit('offer', { sid: remoteSid, payload: { sdp: pc.localDescription } });
    }
  };

  // Cleanup
  useEffect(() => () => Object.values(peerConnections).forEach(pc => pc.close()), [peerConnections]);

  return { peerConnections, createConnection };
}
