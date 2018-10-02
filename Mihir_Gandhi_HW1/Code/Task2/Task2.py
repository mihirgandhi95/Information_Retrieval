# Import regualr expressions
import re


# GLOBAL VARIABLES
# List to store the links from the 1000 link files, will contain 3000 links
new_list = []

# List to remove duplicates from the links in the new_list,
# checker_list does not have duplicates
checker_list = []

# List to write to take the first 1000 links from the sorted new_list
final_list = []

# List to use to write to the file with the final crawled links
new_final_list = []


def openfiles():

    global new_list
    global checker_list
    global final_list
    global new_final_list

    # Open the three files that we want to merge from their respective folders
    file1 = open('/Users/mihirg/PycharmProjects/assignment1/FolderTime/visiteddictime.txt')
    file2 = open('/Users/mihirg/PycharmProjects/assignment1/FolderCar/visiteddiccar.txt')
    file3 = open('/Users/mihirg/PycharmProjects/assignment1/FolderCarbon/visiteddiccarbon.txt')

    # read the lines from the three files and store the lines in the separate variables
    lines = file1.readlines()
    lines2 = file2.readlines()
    lines3 = file3.readlines()

    # adding the lines from the second and third files to the first file, will filter the first file
    lines.append("\n")
    for line in lines2:
        lines.append(line)

    lines.append("\n")
    for line in lines3:
        lines.append(line)

    # Using regular expressions to filter the links in the files
    regex = re.compile('[1](.)*')
    regex2 = re.compile('[2](.)*')
    regex3 = re.compile('[3](.)*')
    regex4 = re.compile('[4](.)*')
    regex5 = re.compile('[5](.)*')
    regex6 = re.compile('[6](.)*')

        # using the regular expressions to filter the links in the file and add them to the list in order of the depth
    for line in lines:
        if regex.match(line):
            new_list.append(line)

    for line in lines:
        if regex2.match(line):
            new_list.append(line)

    for line in lines:
        if regex3.match(line):
            new_list.append(line)

    for line in lines:
        if regex4.match(line):
            new_list.append(line)

    for line in lines:
        if regex5.match(line):
            new_list.append(line)

    for line in lines:
        if regex6.match(line):
            new_list.append(line)


def generatelist():

    global new_list
    global checker_list
    global final_list
    global new_final_list

    # Loop through the new_list and store the links that are not duplicates
    for x in new_list:
        if x not in checker_list:
            checker_list.append(x)

    # Update the new_list with the duplicates removed
    new_list = checker_list

    # copy the first 1000 links from the sorted new_list to final_list
    final_list = new_list[:1000]

    # loop through the final list and copy those links that do not have different depths but same urls
    for x in final_list:
        if x[2:] not in new_final_list:
            new_final_list.append(x)

    # write to the file
    file = open('/Users/mihirg/PycharmProjects/assignment1/MergedList/mergedlist.txt', 'w')
    for x in new_final_list:
        file.write(x)



def task2():

    # method to open files, read files and then compare lines of files using regular expressions
    openfiles()

    # generate the final list of links that is at most 1000 length and without duplicates of both kinds
    # kind1 -duplicates -  same depth same url
    # kind2 - duplicates - different depth same url
    generatelist()


# Declaring the main function in Python
def main():
    task2()

# Checking if the program is being run by itself or imported from another module
if __name__ == '__main__':
    # print ('This program is being run by itself');
    main()
else:
    print('the program is imported from another module')