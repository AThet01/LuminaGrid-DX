import socket
import cv2
import pickle
import struct
import argparse

def run_worker(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"✅ Worker active on port {port}. Ready for Master...")

    while True:
        conn, addr = server.accept()
        try:
            # 1. Receive size header
            payload_size = struct.calcsize("Q")
            data = b""
            while len(data) < payload_size:
                packet = conn.recv(4096)
                if not packet: break
                data += packet
            
            if not data: continue

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            # 2. Receive the actual image bytes
            while len(data) < msg_size:
                data += conn.recv(4096)
            
            frame_data = data[:msg_size]
            
            # 3. Process
            encoded_chunk = pickle.loads(frame_data)
            chunk = cv2.imdecode(encoded_chunk, 1)
            processed = cv2.Canny(chunk, 100, 200) # Task
            
            # 4. Send back compressed result
            _, result_encoded = cv2.imencode('.jpg', processed)
            result_data = pickle.dumps(result_encoded)
            conn.sendall(struct.pack("Q", len(result_data)) + result_data)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            conn.close() # Clean up after each task

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()
    run_worker(args.port)