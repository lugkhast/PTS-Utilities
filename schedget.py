#!/usr/bin/env python3

# schedget.py

import sys
import csv

def dict_print_sorted(dictToPrint):
    keys = dictToPrint.keys()
    keys.sort()

    for key in keys:
        print(key + ': ' + str(dictToPrint[key]))

def get_rows_from_csv(filename):
    csvRows = []
    with open(filename, 'r') as csvfile:
        responseReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in responseReader:
            csvRows.append(row)

    return csvRows


class ScheduleGrabber:
    def __init__(self, rows):
        self.time_slots = {};
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday']
        self.time_slot_strings = ['0800-0930', '0940-1110', '1120-1250',
                '1300-1430', '1440-1610', '1620-1750', '1800 onwards']

        for day in self.days:
            self.time_slots[day] = {}
            for slotstr in self.time_slot_strings:
                self.time_slots[day][slotstr] = []


        for tutor_info in rows:
            self.extract_tutor_timeslots(self.time_slots, tutor_info)


    def extract_tutor_timeslots(self, time_slots, tutor_info):
        # tutor_info is a row of the spreadsheet
        name = tutor_info[0]

        # For each day
        # Take the time slot info string and split it
        # Add the tutor's name to the array of names for that time slot. If there
        # is no array yet, create one.
        for i in range(1, 7):
            day = self.days[i - 1]
            tutor_availability = tutor_info[i].split(', ')

            if tutor_availability[0] == '':
                # We tried to split an empty string, meaning that the tutor is
                # not available for this day. Move on to the next day.
                continue

            for slot in tutor_availability:
                # Disregard custom availability information, and focus on the
                # time slots
                if slot not in self.time_slot_strings:
                    continue

                tutors = time_slots[day][slot]
                tutors.append(name)

    def print_tutor_availabilities(self):
        for day in self.days: # For each day
            time_slots_for_day = self.time_slots[day]

            print(day)

            for time_slot in self.time_slot_strings: # For each time slot

                # Print the time slot...
                tutors = time_slots_for_day[time_slot]
                print(time_slot, end='\t')

                # ...along with the names of every tutor available for that time
                # slot
                for tutor in tutors:
                    print(tutor, end='; ')
                print()
            print()


def main():
    if len(sys.argv) == 1:
        print('Specify the CSV file name on the command line')
        return 1

    rows = get_rows_from_csv(sys.argv[1])
    scheds = ScheduleGrabber(rows[1:]) # Skip row 0, it's just the headers
    scheds.print_tutor_availabilities();

    return 0


if __name__ == '__main__':
    sys.exit(main())

