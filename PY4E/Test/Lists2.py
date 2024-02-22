f = open('dic.txt','r')
f_content = f.readlines()
print(f_content)

dictionary={}
def read_dictionary(filename):
    with open('dic.txt','r') as f:
        for line in f.readlines():
            line = line.strip().split(';')
            key = line[0].strip('\'')
            values = [item.strip('\'') for item in line]
            dictionary[key]=values
    return dictionary

# inverts the dictionary and returns the reversed dictionary
def invert_dict(d):
    inverse = dict()
    for key in d:
        val = d[key]
        for list_item in val:
            if list_item not in inverse:
                inverse[list_item] = [key]
            else:
                inverse[list_item].append(key)
    return inverse


# takes in a dictionary and the filename and writes the dictionary to that file
def write_to_file(inverted_dictionary,filename):
    with open('inverted_dict.txt','w') as outfile:
        for key,value in inverted_dictionary.items():
            outfile.write('\'{0}\':[\'{1}\']\n'.format(key,value))
    print('{} inverted successfully.'.format('inverted_dic.txt'))



def main():
    infile_name = 'dic.txt' # file that needs to be read from
    d = read_dictionary(infile_name) # reads the file which returns a dictionary
    reversed_d = invert_dict(d) # reverses the dictionary and return the reversed dictionary
    print(reversed_d) # you can comment this line
    outfile_name='inverted_dict.txt' # file that needs to be updated with the reversed dictionary
    write_to_file(reversed_d,outfile_name) # writes dictionary to the file


main()