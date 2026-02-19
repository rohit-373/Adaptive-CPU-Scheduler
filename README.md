# 📌 Adaptive Hybrid CPU Scheduler

An intelligent CPU scheduling simulator that dynamically switches between multiple scheduling algorithms to efficiently handle mixed workloads in a multiprogramming environment.

The scheduler combines Priority Scheduling, Shortest Job First (SJF), and Round Robin (RR) to improve responsiveness, reduce starvation, and maintain high CPU utilization.

## 🚀 Features
- Hybrid scheduling approach (Priority + SJF + Round Robin)
- Process type awareness (real-time, interactive, batch)
- Dynamic algorithm switching based on workload
- Priority aging to prevent starvation
- Gantt chart visualization
- Performance comparison with FCFS and Round Robin
- Metrics calculation:
  - Average Waiting Time
  - Average Turnaround Time
  - CPU Utilization

## 🧠 Scheduling Strategy
The scheduler adapts using the following logic:
- Real-time processes → Priority scheduling
- Interactive processes → Round Robin
- Batch processes → Shortest Job First
- Burst patterns & arrival rate → Dynamic switching
- Long waiting processes → Priority aging
This ensures fairness, responsiveness, and efficiency.

## 📊 Output
The program generates:
- Process table (AT, BT, CT, TAT, WT)
- Average Waiting Time
- Average Turnaround Time
- CPU Utilization
- Gantt chart showing execution timeline

## ⚙️ How to Run
Requirements: Python 3.x

```python
python main.py
```

## 📁 Project Structure
- main.py          → Scheduler simulation
- README.md        → Documentation

## 🎯 Learning Outcomes
- Understanding CPU scheduling algorithms
- Context switching behavior
- Hybrid scheduling design
- Starvation prevention using aging
- Performance evaluation of schedulers
