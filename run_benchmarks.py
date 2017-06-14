import subprocess as sub
import threading
import time



class TimeoutThread(threading.Thread):

    def __init__(self, launch_thread):
        threading.Thread.__init__(self)
        self.launch_thread = launch_thread

    def run(self):
        self.launch_thread.join(self.launch_thread.timeout)

        if self.launch_thread.is_alive():
            self.launch_thread.p.terminate()
            self.launch_thread.join()

class RunCmd(threading.Thread):
    """
        Taken from https://stackoverflow.com/questions/4158502/python-kill-or-terminate-subprocess-when-timeout
    """

    def __init__(self, cmd, timeout, out):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
        self.out = out

    def run(self):
        self.p = sub.Popen(self.cmd, stdout=file)
        self.p.wait()

    def Run(self):
        self.start()
        TimeoutThread(self).start()



TIMEOUT = 10 * 60
SEPARATOR = "########################################################################"

problems = list(range(1, 4))

methods = {
    1 : "breadth_first_search",
    2 : "breadth_first_tree_search",
    3 : "depth_first_graph_search",
    4 : "depth_limited_search",
    5 : "uniform_cost_search",
    6 : "recursive_best_first_search_h_1",
    7 : "greedy_best_first_graph_search_h_1",
    8 : "astar_search_h_1",
    9 : "astar_search_h_ignore_preconditions",
    10 : "astar_search_h_pg_levelsum"
}


for problem in problems:
    processes = []
    for method_num, method in methods.items():
        bash_ex = ["python", "run_search.py", "-p", str(problem), "-s", str(method_num)]
        print("Running", bash_ex)

        filename = "{0}/{1}/{2}.out".format("benchmark_data", problem, method)
        file = open(filename, "w")
        file.write(SEPARATOR + "\n" + str(method) + "\n" + SEPARATOR + "\n")
        file.flush()


        cmd = RunCmd(bash_ex, TIMEOUT, file)
        cmd.Run()

        processes.append(cmd)

    print("\n\n\n\n\n")

    i = 0
    time = 0
    while i < len(processes):
        process = processes[i]
        print("Waiting for ", process.cmd, "time spent ", time)

        if hasattr(process, "p"):
            process.p.wait()
            i += 1
            time = 0
        else:
            time.sleep(10)
            time += 10

    print("\n\n\n\n\n")