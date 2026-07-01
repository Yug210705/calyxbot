import time
import psutil
import os
import subprocess

def measure_startup():
    print("Measuring FastAPI Cold Start...")
    
    start_time = time.perf_counter()
    
    # Launch uvicorn as a subprocess
    process = subprocess.Popen(
        [r"..\..\backend\.venv\Scripts\python.exe", "-m", "uvicorn", "app.main:app"],
        cwd=r"..\..\backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    startup_time = None
    
    for line in process.stdout:
        if "Application startup complete" in line:
            end_time = time.perf_counter()
            startup_time = (end_time - start_time) * 1000
            break
            
    if startup_time:
        print(f"✅ Cold Start Time: {startup_time:.2f} ms")
        
        # Measure memory
        p = psutil.Process(process.pid)
        mem_info = p.memory_info()
        print(f"✅ Memory Usage (RSS): {mem_info.rss / 1024 / 1024:.2f} MB")
        
        # Measure connections
        conns = p.connections()
        print(f"✅ Open Connections: {len(conns)}")
    else:
        print("❌ Failed to measure startup.")
        
    process.terminate()

if __name__ == "__main__":
    measure_startup()
