# LuminaGrid-DX
LuminaGrid DX is a high-performance system designed to handle CPU-intensive image transformations by distributing workloads across a network of worker nodes.Built with Python Sockets and OpenCV, it demonstrates horizontal scaling and fault-tolerant system design.

# 🚀 Key Features

    1.Parallel Execution: Uses Python's threading to communicate with multiple workers simultaneously, reducing total processing time by up to 60%.

    2.Data Optimization: Implements JPEG compression for socket transfers, minimizing network overhead.

    3.Fault Tolerance: Built-in error handling to detect and report offline or crashed worker nodes without crashing the Master UI.

    4.Professional UI: A sleek Streamlit dashboard for real-time monitoring and control.

# 🏗️ System Architecture

The project follows a Master-Worker (Centralized) architecture:

    1.Master (Streamlit): Decomposes the image into horizontal segments and manages the distribution queue.

    2.Workers (TCP Sockets): Independent nodes that process image "chunks" using OpenCV Canny Edge Detection.

    3.Reassembly: The Master stitches the processed results back into a single high-resolution output.

# 🛠️ System Specifications

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Networking** | TCP Sockets | Data transmission between Master and Workers |
| **Processing** | OpenCV 4.x | Image transformation (Canny Edge Detection) |
| **Interface** | Streamlit | Real-time monitoring and control dashboard |
| **Concurrency** | Threading | Parallel socket management |

If a node is unreachable, the system gracefully handles the timeout and notifies the user. 

# 🏁 Getting Started

1. Install Requirements
Bash
```
pip install streamlit opencv-python numpy Pillow
```
2. Start Worker Nodes
Open multiple terminals to simulate different machines:
Bash
```
# Terminal 1
python worker_node.py --port 5001

# Terminal 2
python worker_node.py --port 5002
```
3. Launch Master Dashboard
Bash
```
streamlit run master_app.py
```
# 📈 Optimization & Lessons Learned

As a Knowledge Engineering student, this project allowed me to explore:

    1.Communication vs. Computation: Distributed systems are most efficient when the processing task is significantly larger than the time taken to send data (Serialization).

    2.Bottleneck Identification: Initial versions used raw pixel arrays; implementing JPEG compression before pickle serialization was the key to making the system feel "instant."
