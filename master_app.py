import streamlit as st
import cv2
import numpy as np
import socket
import struct
import pickle
import threading
import time

st.set_page_config(page_title="LuminaGrid Master", layout="wide")
st.title("🌐 LuminaGrid: Parallel DX Processor")

worker_ports = st.sidebar.multiselect("Active Worker Ports", [5001, 5002, 5003], default=[5001, 5002])
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])

def worker_thread(port, chunk, results, index):
    try:
        # Create a new socket for each thread
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5) # 5 second timeout
        s.connect(('127.0.0.1', port))
        
        # Compress and Send
        _, encoded = cv2.imencode('.jpg', chunk)
        data = pickle.dumps(encoded)
        s.sendall(struct.pack("Q", len(data)) + data)
        
        # Receive result
        payload_size = struct.calcsize("Q")
        header = b""
        while len(header) < payload_size:
            header += s.recv(payload_size - len(header))
        
        res_size = struct.unpack("Q", header)[0]
        res_data = b""
        while len(res_data) < res_size:
            res_data += s.recv(4096)
            
        result_encoded = pickle.loads(res_data)
        results[index] = cv2.imdecode(result_encoded, 0)
        s.close()
    except Exception as e:
        print(f"Port {port} failed: {e}")
        results[index] = None

if uploaded_file and st.button("🚀 Run Parallel Processing"):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    chunks = np.array_split(img, len(worker_ports))
    threads = []
    results = [None] * len(worker_ports)

    for i, port in enumerate(worker_ports):
        t = threading.Thread(target=worker_thread, args=(port, chunks[i], results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Reassemble
    if all(r is not None for r in results):
        final_img = np.vstack(results)
        st.image(final_img, caption="Processed Result")
        st.success("Success!")
    else:
        st.error("Connection Error: Check if all Workers are running in their terminals.")