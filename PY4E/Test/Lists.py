
def main():
    infile_name = 'dic.txt' # file that needs to be read from
    d = read_dictionary(infile_name) # reads the file which returns a dictionary
    reversed_d = invert_dict(d) # reverses the dictionary and return the reversed dictionary
    outfile_name='inverted_dict.txt' # file that needs to be updated with the reversed dictionary
    write_to_file(reversed_d,outfile_name) # writes dictionary to the file


def read_dictionary(filename):
    dictionary = {}
    with open(filename,'r') as f:
        for line in f.readlines():
            if len(line.split()) == 0: continue     # Skip line if blank
            line = line.strip().split(':')          # Splitting between keys and values
            key = line[0].strip()                   
            values = line[1:]
            dictionary[key]=values[0].replace(" ", "").split(",")   # Getting all values
    return dictionary

# inverts the dictionary and returns the reversed dictionary
def invert_dict(d):
    inverse = dict()
    for key in d:
        vals = d[key]
        for val in vals:
            if val not in inverse:
                inverse[val] = [key]
            else:
                inverse[val].append(key)
    return inverse


# takes in a dictionary and the filename and writes the dictionary to that file
def write_to_file(inverted_dictionary,filename):
    with open(filename,'w') as outfile:
        for key,value in inverted_dictionary.items():
            outfile.write('\'{0}\': \'{1}\'\n'.format(key,value))
    print('{} inverted successfully.'.format('inverted_dic.txt'))


if __name__ == "__main__":
    main()