import os
import csv

def get_outputs_data(directory):
    # Retrieve all .fuzz files in the directory and sort them in ascending order
    fuzz_files = [f for f in os.listdir(directory) if f.endswith('.fuzz')]
    fuzz_files.sort(key=lambda x: int(x.split('.')[0]))

    data_collection = {}

    # Read data from each file as a CSV or plain text otherwise and store it in the dictionary
    for filename in fuzz_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, newline='') as f:
            try:
                reader = csv.reader(f)
                data = '\n'.join([', '.join(row) for row in reader if any(cell.strip() for cell in row)])
            except csv.Error:
                f.seek(0)
                data = f.read().strip()
 
        if data:
            data_collection[filename] = data

    return data_collection

# Test the functionality of get outputs
def main():
    # Test the function with the demo directory
    directory = 'outputs/demo'

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    data = get_outputs_data(directory)
    if data:
        for filename, rows in data.items():
            print(f"Processing {filename}:")
            for row in rows:
                print(', '.join(row))
            print("\n" + " " * 10)
    else:
        print("No data found in .fuzz files.")

    # Test the function with the demo coverage directory
    directory = 'outputs/demo_coverage_cvc5'

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    data = get_outputs_data(directory)
    if data:
        for filename, rows in data.items():
            print(f"Processing {filename}:")
            for row in rows:
                print(', '.join(row))
            print("\n" + " " * 10)
    else:
        print("No data found in .fuzz files.")    

if __name__ == "__main__":
    main()
