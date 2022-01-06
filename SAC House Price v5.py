# version 8
# This code will not make sense if you don't know about globals(), classes and tkinter basics
# luckily, they're all pretty straightforward
import csv
import os.path
import sys
import write_csv_file
from tkinter import *

root = Tk()
root.title('House Price Calculator')

# collecting data
try:  # open
    file = write_csv_file.write()
    file.run()
except PermissionError:
    print("Please close raw_data.csv")
    sys.exit()

room_type = ['kitchen', 'living_room', 'bedroom', 'bathroom', 'study', 'laundry', 'dining_room']
current_room = 0

# open up the csv file, make a new list containing prices, recurring
for i in range(len(room_type)):
    with open('raw_data.csv', 'r') as f:
        globals()[f'item_list_{room_type[current_room]}'] = []  # create new lists for each room_type
        globals()[f'recurring_prices_{room_type[current_room]}'] = []
        globals()[f'base_prices_{room_type[current_room]}'] = []
        reader = csv.reader(f)
        for row in reader:
            for elements in row:
                if elements == room_type[current_room]:
                    globals()[f'item_list_{room_type[current_room]}'].append(row[1])
                    globals()[f'recurring_prices_{room_type[current_room]}'].append(float(row[2]))
                    globals()[f'base_prices_{room_type[current_room]}'].append(float(row[3]))
    current_room += 1

rooms = {}  # rooms
total_rec = 0  # total monthly cost
total_base = 0  # total base cost
global packed_rooms
packed_rooms = 0


class Room:  # each new room has a class
    def __init__(self):
        self.price_rec = 0
        self.price_base = 0
        self.objects = []

    def add_app(self, item):  # adds appliance
        self.objects.append(item)

    def list(self, r, a, total_a):  # lists prices, name and recurring prices
        globals()[f'contents_label_{r}{a}'] = Label(root, text='\n'.join(self.objects), wraplength=500).grid(column=6,
                                                                                                             row=total_a + 2)
        globals()[f'recurring_price_label_{r}{a}'] = Label(root, text='$' + '{:,}'.format(
            round(self.price_rec, 2)) + ' per month',
                                                           wraplength=500).grid(column=7,
                                                                                row=total_a + 2 - packed_rooms)
        globals()[f'base_price_label_{r}{a}'] = Label(root, text='$' + '{:,}'.format(round(self.price_base, 2)),
                                                      wraplength=500).grid(column=8, row=total_a + 2 - packed_rooms)

    def compute_price(self, r):  # computes prices
        global total_base, total_rec
        total_rec -= self.price_rec
        total_base -= self.price_base
        self.price_rec = 0
        self.price_base = 0

        for a in range(len(self.objects)):
            self.price_rec += globals()[f'recurring_prices_{r}'][globals()[f'item_list_{r}'].index(self.objects[a])]
        for k in range(len(self.objects)):
            self.price_base += globals()[f'base_prices_{r}'][globals()[f'item_list_{r}'].index(self.objects[k])]

        total_rec += self.price_rec
        total_base += self.price_base


def display_total():  # displays the totals
    global total_base, total_rec, total_rec_label, total_base_label
    try:
        total_rec_label.destroy()
        total_base_label.destroy()
    except NameError:
        pass
    total_rec_label = Label(root, text='Total monthly bills: ' + '$' + '{:,}'.format(round(total_rec, 2)),
                            font=('BahnSchrift', 12))
    total_rec_label.grid(column=6, row=len(rooms) + 2 - packed_rooms)
    total_base_label = Label(root, text='Total initial costs: ' + '$' + '{:,}'.format(round(total_base, 2)),
                             font=('BahnSchrift', 12))
    total_base_label.grid(column=8, row=len(rooms) + 2 - packed_rooms)


def new_app(r, a, total_a):  # edits the appliances in the room
    global total_base, total_rec
    if 'Pick an appliance to add' not in globals()[f'{r}_var{a}'].get():
        rooms[f'{r}{a}'].add_app(item=globals()[f'{r}_var{a}'].get())
        rooms[f'{r}{a}'].compute_price(r)
        rooms[f'{r}{a}'].list(r, a, total_a)
        display_total()


def new_room(r):  # creates a new room
    total_a = len(rooms)
    a = 0
    for i in range(len(rooms)):
        try:
            if rooms[f'{r}{a}'] != 0:
                a += 1
        except KeyError:
            pass
    rooms[f'{r}{a}'] = Room()
    globals()[f'{r}_var{a}'] = StringVar(root)
    globals()[f'{r}_var{a}'].set(f"Pick an appliance to add to {r} {a + 1}")
    # print(rooms)
    globals()[f'app_add_{r}{a}'] = Button(root, text=f'Add appliance to {r} {a + 1}',
                                          command=lambda: new_app(r, a, total_a)).grid(column=0,
                                                                                       row=total_a + 2 - packed_rooms,
                                                                                       columnspan=3)
    globals()[f'app_list_{r}{a}'] = OptionMenu(root, globals()[f'{r}_var{a}'], *globals()[f'item_list_{r}']).grid(
        column=3, row=total_a + 2 - packed_rooms, columnspan=3)
    display_total()


def info():  # just info
    info_window = Toplevel()
    info_window.title('Information')
    version = Label(info_window, text="Version 8",
                    font=('Aldhabi', 8)).pack()
    made_by = Label(info_window, text="Programming by Orlando Scalzo\nData sourcing by Mark Crosbee",
                    font=('Sans Serif', 16)).pack()
    info_desc = Label(info_window, text='A scroll bar will not be implemented, sorry!\n\n'
                                        'Use this software to calculate your house price by following these steps\n\n'
                                        '1. Add any room of your choice (you can add as many as you want)\n'
                                        '2. Choose an appliace to add to that room\n'
                                        '3. Click the add appliance button for that room to add the appliace\n'
                                        '4. The price of that individual room should show up adjacent').pack()
    button_desc = Label(info_window, text='\nTHE BUTTON BELOW WILL OPEN UP AN EXCEL FILE\n\n'
                                          'Opening up an Excel file might make the software lag. Any changes\n'
                                          'made to the file will only work if the file is saved and the program\n'
                                          'is restarted\n\n'
                                          'To add any new appliances, pick the start of a new row and\n'
                                          'follow these conventions\n\n'
                                          '[appliance room] | [appliance name] | [recurring cost (bills)] |'
                                          ' [initial cost]\n\nYou cannot add new types of rooms').pack()
    open_excel = Button(info_window, text='List of all appliances and their costs',
                        command=lambda: os.system('raw_data.csv')).pack()


title = Label(root, text='Calculate your house', font=('BahnSchrift', 25)).grid(column=0, row=0, columnspan=1000)
more_info = Button(root, text='Click here for more info\n and how to use!', command=info).grid(row=0, column=9)

for i in range(len(room_type)):  # use globals() to generate variables
    globals()[f'{room_type[i]}_add'] = Button(root, text='Add a ' + room_type[i],
                                              command=lambda ci=i: new_room(r=room_type[ci]))
    # creates a new buttom for each room that calls to create that room upon opening
    globals()[f'{room_type[i]}_add'].grid(row=1, column=i + 1)
    # packs it to grid (this was a bad idea, using,.grid() is the worst

root.resizable(0, 0)
root.mainloop()
