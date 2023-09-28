import csv
from datetime import datetime

io_map = {
    "i":"in",
    "o":"out",
    "c":"comment",
    "d":"done"
}

def punch(io=None, activity=None, time=None):
    if time is None:
        time = datetime.now()
        
    if io is None:
        print("i = in | o = out | c = comment")
        io = input("> ")
        activity = input("> ")
    
    if io in io_map:
        io = io_map[io]

    timestring = time.strftime('%Y-%m-%d__%H-%M-%S')
    data = [timestring, io, activity]

    with open('data/punchcard.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
