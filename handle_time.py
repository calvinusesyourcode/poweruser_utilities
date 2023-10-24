import csv
from datetime import datetime
from collections import deque

io_map = {
    "i":"in",
    "o":"out",
    "c":"comment",
    "d":"done",
    "b":"back"
}

def punch(io=None, activity=None, time=None):
    if time is None:
        time = datetime.now()
        
    if io is None:
        print("\n".join([f"{key} = {io_map[key]}" for key in io_map]))
        print("\n")
        io = input("> ")
    
    if not (io == "o" or io == "b"):
        activity = input("> ")
    
    
    if io in io_map:
        io = io_map[io]

    timestring = time.strftime('%Y-%m-%d__%H-%M-%S')
    data = [timestring, io, activity]

    with open('data/punchcard.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def show_last_n_lines(filename='data/punchcard.csv', n=10):
    with open(filename, 'r') as f:
        last_n_lines = deque(f, maxlen=n)
        for line in last_n_lines:
            print(line.strip()) 