import multiprocessing
import time

def sample(n):
    for i in range(10000 * n):
        print(i)

if __name__ == '__main__':
    # Start foo as a process
    p = multiprocessing.Process(target=sample, name="sample", args=(100,))
    p.start()

    # Wait maximum 4 seconds for foo
    p.join(4) #join([timeout in seconds])

    # If thread is active
    if p.is_alive():
        print("sample is running, kill it")
        # Terminate foo
        p.terminate()
        p.join() # check source!
    else:
        print("just on time")