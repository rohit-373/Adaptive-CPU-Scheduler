class Process:
    def __init__(self, pid, arrival, burst, priority, ptype):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.priority = priority
        self.ptype = ptype
        self.start=None
        self.completion=0
        self.waiting=0
        self.turnaround=0


base_processes = [
    ("P1",0,8,1,"real-time"),
    ("P2",1,5,3,"interactive"),
    ("P3",2,12,5,"batch"),
    ("P4",3,4,2,"real-time"),
    ("P5",4,6,4,"interactive"),
]


def clone():
    return [Process(*p) for p in base_processes]


# FCFS
def run_fcfs():
    procs=clone()
    t=0

    for p in sorted(procs,key=lambda x:x.arrival):
        if t<p.arrival:
            t=p.arrival

        p.start=t
        t+=p.burst
        p.completion=t
        p.turnaround=p.completion-p.arrival
        p.waiting=p.turnaround-p.burst

    return procs


# RR
def run_rr(q=3):
    procs=clone()
    ready=[]
    done=[]
    added=set()
    t=0

    while len(done)<len(procs):

        for p in procs:
            if p.arrival<=t and p.pid not in added:
                ready.append(p)
                added.add(p.pid)
        
        if not ready:
            t+=1
            continue

        cur=ready.pop(0)

        if cur.start is None:
            cur.start=t

        run=min(q,cur.remaining)

        for _ in range(run):
            t+=1
            cur.remaining-=1

            for p in procs:
                if p.arrival<=t and p.pid not in added:
                    ready.append(p)
                    added.add(p.pid)

        if cur.remaining==0:
            cur.completion=t
            cur.turnaround=cur.completion-cur.arrival
            cur.waiting=cur.turnaround-cur.burst
            if cur not in done:
                done.append(cur)
        else:
            ready.append(cur)

    return done


# HYBRID
def run_hybrid():

    procs=clone()
    ready=[]
    done=[]
    timeline=[]
    added=set()
    t=0
    MAX_TIME=1000

    while len(done)<len(procs) and t<MAX_TIME:

        for p in procs:
            if p.arrival<=t and p.pid not in added:
                ready.append(p)
                added.add(p.pid)

        if not ready:
            t += 1
            continue

        for p in ready:
            p.priority=max(1,p.priority-0.1)

        bursts=[p.remaining for p in ready]
        avg=sum(bursts)/len(bursts)
        realtime=any(p.ptype=="real-time" for p in ready)

        if realtime:
            ready.sort(key=lambda x:x.priority)
            cur=ready.pop(0)
            run=1

        elif avg<=6:
            ready.sort(key=lambda x:x.remaining)
            cur=ready.pop(0)
            run=1

        else:
            cur=ready.pop(0)
            run=min(3,cur.remaining)

        if cur.start is None:
            cur.start=t

        for _ in range(run):
            timeline.append((t,cur.pid))
            t+=1
            cur.remaining-=1

        if cur.remaining==0:
            cur.completion=t
            cur.turnaround=cur.completion-cur.arrival
            cur.waiting=cur.turnaround-cur.burst
            if cur not in done:
                done.append(cur)
        else:
            ready.append(cur)

    util=(len(timeline)/t)*100
    return done,util,timeline


# PRINT
def print_table(title, arr, util=None):
    print("\n==========",title,"==========")
    print("PID\tAT\tBT\tCT\tTAT\tWT")

    tw=tt=0
    for p in sorted(arr,key=lambda x:x.pid):
        print(p.pid,p.arrival,p.burst,p.completion,p.turnaround,p.waiting,sep="\t")
        tw+=p.waiting
        tt+=p.turnaround

    n=len(arr)
    print("\nAverage Waiting Time:",round(tw/n,2))
    print("Average Turnaround Time:",round(tt/n,2))

    if util is not None:
        print("CPU Utilization:",round(util,2),"%")

def print_gantt(timeline):
    print("\nGantt Chart:\n")

    cell=5
    bar=""
    times=f"{timeline[0][0]:<{cell}}"

    for t,p in timeline:
        bar+=f"|{p:^{cell-1}}"
        times+=f"{t+1:<{cell}}"

    bar+="|"
    print(bar)
    print(times)


# RUN
fcfs=run_fcfs()
rr=run_rr()
hyb,util,timeline=run_hybrid()

print_table("FCFS",fcfs)
print_table("Round Robin",rr)
print_table("Adaptive Hybrid",hyb,util)
print_gantt(timeline)
