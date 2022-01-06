# write the data file
# The way I've used self.__dict__ is the same as globals()
# reading and writing to csv files is incredibly straightforward

class write:
    def __init__(self):
        self.row_type = ['kitchen', 'living_room', 'bedroom', 'bathroom', 'study', 'laundry', 'dining_room']

        # creates a list for each room type
        for i in range(len(self.row_type)):
            self.__dict__[f'appliances_{i}'] = []
            self.__dict__[f'crc_{i}'] = []
            self.__dict__[f'cbc_{i}'] = []

    def run(self):
        import csv
        import os
        a = 0

        try:  # reads the file to lists
            file = open('raw_data.csv', 'r')
            invalid_rooms = []
            with file as f:
                reader = csv.reader(f)
                for row in reader:
                    for i in range(len(self.row_type)):
                        if self.row_type[i] in row[0]:
                            if row[1] not in self.__dict__[f'appliances_{i}']:
                                self.__dict__[f'appliances_{i}'].append(row[1])
                                self.__dict__[f'crc_{i}'].append(row[2])
                                self.__dict__[f'cbc_{i}'].append(row[3])
                        elif row[0] not in self.row_type and row[0] not in invalid_rooms:
                            print(row[0], 'is not a valid room type')
                            invalid_rooms.append(row[0])

            os.remove('raw_data.csv')
            file = open('raw_data.csv', 'x')
            file.close()
        except FileNotFoundError:
            file = open('raw_data.csv', 'x')
            file.close()

        with open('raw_data.csv', 'w', newline='') as f:  # rewrites the file entirely
            writer = csv.writer(f)
            for k in range(len(self.row_type)):
                for i in range(len(self.__dict__[f'appliances_{a}'])):
                    writer.writerow([self.row_type[a],
                                     self.__dict__[f'appliances_{a}'][i],
                                     self.__dict__[f'crc_{a}'][i],
                                     self.__dict__[f'cbc_{a}'][i]])
                a += 1

        # outputs results

        f = open("raw_data.csv", 'r')
        reader = csv.reader(f)
        lines = 0
        for row in reader: lines += 1
        print("File built with", lines, "lines")
