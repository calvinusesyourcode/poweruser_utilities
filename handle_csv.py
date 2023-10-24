import csv
import os
import datetime

def convert_and_sort_date(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        for row in rows[1:]:  # Exclude the header row
            date_parts = row[2].split("/")
            
            if len(date_parts) == 3:
                try:
                    month, day, year = date_parts
                    dt = datetime.date(int(year), int(month), int(day))
                    row[2] = dt.strftime('%Y%m%d')
                except ValueError:
                    # Continue processing other rows even if one row has a problematic date
                    continue

    # Sort the rows based on the date column (assuming the date is in the third column)
    header = rows[0]
    sorted_rows = sorted(rows[1:], key=lambda x: datetime.datetime.strptime(x[2], '%Y%m%d'), reverse=True)
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_rows)

def main():
    directory = "csv"
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            full_path = os.path.join(directory, filename)
            convert_and_sort_date(full_path)

if __name__ == "__main__":
    main()
