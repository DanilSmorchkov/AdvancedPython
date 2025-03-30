import multiprocessing as mp
import sys
import time
import codecs
from threading import Thread
from queue import Queue, Empty


def process_a(queue_a, queue_b):
    internal_queue = Queue()

    def receive():
        while True:
            try:
                msg = queue_a.get()
                processed_msg = msg.lower()
                internal_queue.put(processed_msg)
            except:
                break

    receiver_thread = Thread(target=receive)
    receiver_thread.start()

    while True:
        try:
            msg = internal_queue.get_nowait()
            queue_b.put(msg)
            time.sleep(5)
        except Empty:
            pass


def process_b(queue_b, queue_main):
    while True:
        msg = queue_b.get()
        encoded_msg = codecs.encode(msg, 'rot13')
        current_time = time.strftime('%H:%M:%S')
        print(f"[{current_time}] Process B: {encoded_msg}")
        queue_main.put(encoded_msg)


def main():
    queue_a = mp.Queue()
    queue_b = mp.Queue()
    queue_main = mp.Queue()

    a = mp.Process(target=process_a, args=(queue_a, queue_b))
    b = mp.Process(target=process_b, args=(queue_b, queue_main))
    a.start()
    b.start()

    def stdin_reader():
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            queue_a.put(line)

    stdin_thread = Thread(target=stdin_reader)
    stdin_thread.start()

    def main_receiver():
        while True:
            msg = queue_main.get()
            current_time = time.strftime('%H:%M:%S')
            print(f"[{current_time}] Main received: {msg}")

    main_receiver_thread = Thread(target=main_receiver)
    main_receiver_thread.start()

    try:
        a.join()
        b.join()
    except KeyboardInterrupt:
        a.terminate()
        b.terminate()


if __name__ == '__main__':
    main()