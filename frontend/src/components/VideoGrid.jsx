import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { useSocket } from "../hooks/useSocket";

export default function VideoGrid() {
  const { id: roomId } = useParams(); // de la ruta /room/:id
  const socket = useSocket();
  const localVideoRef = useRef();
  const [peers, setPeers] = useState({}); // { peerId: MediaStream }

  const peerConnections = useRef({}); // { peerId: RTCPeerConnection }

  useEffect(() => {
    if (!socket) return;

    let localStream;

    const init = async () => {
      // 1. Obtener cámara/micrófono
      localStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });
      if (localVideoRef.current) localVideoRef.current.srcObject = localStream;

      // 2. Unirse al room
      socket.emit("join_room", { room_id: roomId });

      // 3. Cuando alguien más entra
      socket.on("new_peer", async ({ peerId }) => {
        console.log("Nuevo peer:", peerId);
        createOffer(peerId, localStream);
      });

      // 4. Cuando recibo una oferta
      socket.on("offer", async ({ from, offer }) => {
        const pc = createPeerConnection(from, localStream);
        await pc.setRemoteDescription(new RTCSessionDescription(offer));
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        socket.emit("answer", { to: from, answer });
      });

      // 5. Cuando recibo una respuesta
      socket.on("answer", async ({ from, answer }) => {
        const pc = peerConnections.current[from];
        if (pc) await pc.setRemoteDescription(new RTCSessionDescription(answer));
      });

      // 6. ICE Candidates
      socket.on("ice-candidate", async ({ from, candidate }) => {
        const pc = peerConnections.current[from];
        if (pc && candidate) {
          await pc.addIceCandidate(new RTCIceCandidate(candidate));
        }
      });
    };

    const createPeerConnection = (peerId, stream) => {
      const pc = new RTCPeerConnection();

      // Agregar tracks de mi cámara
      stream.getTracks().forEach((track) => pc.addTrack(track, stream));

      // Cuando recibo tracks remotos
      pc.ontrack = (event) => {
        setPeers((prev) => ({
          ...prev,
          [peerId]: event.streams[0],
        }));
      };

      // ICE candidates
      pc.onicecandidate = (event) => {
        if (event.candidate) {
          socket.emit("ice-candidate", {
            to: peerId,
            candidate: event.candidate,
          });
        }
      };

      peerConnections.current[peerId] = pc;
      return pc;
    };

    const createOffer = async (peerId, stream) => {
      const pc = createPeerConnection(peerId, stream);
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);
      socket.emit("offer", { to: peerId, offer });
    };

    init();

    return () => {
      socket.disconnect();
      Object.values(peerConnections.current).forEach((pc) => pc.close());
    };
  }, [socket, roomId]);

  return (
    <div className="grid grid-cols-2 gap-4 p-4">
      {/* Video local */}
      <video
        ref={localVideoRef}
        autoPlay
        muted
        playsInline
        className="rounded-xl border shadow-md"
      />
      {/* Videos remotos */}
      {Object.entries(peers).map(([peerId, stream]) => (
        <video
          key={peerId}
          autoPlay
          playsInline
          className="rounded-xl border shadow-md"
          ref={(videoEl) => {
            if (videoEl) videoEl.srcObject = stream;
          }}
        />
      ))}
    </div>
  );
}
