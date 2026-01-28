# LuminaGrid-DX
LuminaGrid DX is a high-performance system designed to handle CPU-intensive image transformations by distributing workloads across a network of worker nodes.Built with Python Sockets and OpenCV, it demonstrates horizontal scaling and fault-tolerant system design.

# 🚀 Key Features

    Parallel Execution: Uses Python's threading to communicate with multiple workers simultaneously, reducing total processing time by up to 60%.

    Data Optimization: Implements JPEG compression for socket transfers, minimizing network overhead.

    Fault Tolerance: Built-in error handling to detect and report offline or crashed worker nodes without crashing the Master UI.

    Professional UI: A sleek Streamlit dashboard for real-time monitoring and control.

# 🏗️ System Architecture

The project follows a Master-Worker (Centralized) architecture:

    Master (Streamlit): Decomposes the image into horizontal segments and manages the distribution queue.

    Workers (TCP Sockets): Independent nodes that process image "chunks" using OpenCV Canny Edge Detection.

    Reassembly: The Master stitches the processed results back into a single high-resolution output.

# 🛠️ Tech Stack
Category	Technology
Language	Python 3.9+
Networking	Socket Programming (TCP/IP)
Concurrency	Multithreading
Computer Vision	OpenCV (cv2)
Dashboard	Streamlit
Data Handling	NumPy, Pickle
📸 Demo & Error Handling
Success Case

When all workers are active, the image is processed in parallel and reassembled instantly. (Insert your Success screenshot here)
Fault Tolerance (Unsuccessful Case)

If a node is unreachable, the system gracefully handles the timeout and notifies the user. (Insert your Processing Failed screenshot here)
🏁 Getting Started
1. Install Requirements
Bash

pip install streamlit opencv-python numpy Pillow

2. Start Worker Nodes

Open multiple terminals to simulate different machines:
Bash

# Terminal 1
python worker_node.py --port 5001

# Terminal 2
python worker_node.py --port 5002

3. Launch Master Dashboard
Bash

streamlit run master_app.py

# 📈 Optimization & Lessons Learned

As a Knowledge Engineering student, this project allowed me to explore:

    Communication vs. Computation: Distributed systems are most efficient when the processing task is significantly larger than the time taken to send data (Serialization).

    Bottleneck Identification: Initial versions used raw pixel arrays; implementing JPEG compression before pickle serialization was the key to making the system feel "instant."
