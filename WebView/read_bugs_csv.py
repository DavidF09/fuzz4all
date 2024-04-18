import csv 

def get_bug_cvs_data(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    final_data = []
    contains_data = False

    for i in range(0, len(data)):
        contains_data = False
        for j in range(0, len(data[i])):
            if (len(data[i][j]) != 0):
                contains_data = True
                break
        
        if contains_data:
            final_data.append(data[i])
    return final_data

# This is to test if the above read function read the info from the csv accurately
def main():
    data = get_bug_cvs_data('bugs/clang.csv')
    for i in range(0, len(data)):
        print(data[i])

if __name__ == "__main__":
    main()