def manhattan_distance(data_point1, data_point2):
    a = abs(data_point1['TMAX'] - data_point2['TMAX']) + abs(data_point1['PRCP']-data_point2['PRCP']) + abs(data_point1['TMIN']-data_point2['TMIN'])
    return float(a)


def read_dataset(filename):
    data_list = []
    f = open(filename, "r")
    for line in f:
        datadict = {}
        split_string = line.split()     #split the string to get the value according to each key
        datadict['DATE'] = split_string[0]
        datadict['TMAX'] = float(split_string[2])       #transfer the data type to float
        datadict['PRCP'] = float(split_string[1])       #transfer the data type to float
        datadict['TMIN'] = float(split_string[3])       #transfer the data type to float
        datadict['RAIN'] = split_string[4]
        data_list.append(datadict)
    return data_list


def majority_vote(nearest_neighbors):
    true_count = 0;
    for i in nearest_neighbors:
        if i['RAIN'] == 'TRUE':
            true_count += 1
    if true_count >= len(nearest_neighbors)/2:
        return 'TRUE'
    else:
        return 'FALSE'


def k_nearest_neighbors(filename, test_point, k, year_interval):
    test_year = int(test_point['DATE'].split('-')[0])       #transfer the data type to int
    data_set = read_dataset(filename)
    correct_year=[]
    for item in data_set:       #get the year of all dictionaries
        year = int(item['DATE'].split('-')[0])
        if test_year - year_interval < year < test_year + year_interval:        #if the year information satisfy year interval, add corresponding dictionaries to a new list
            correct_year.append(item)
    for item in correct_year:       #get the manhattan distance  between all points and test_point
        distance = manhattan_distance(item, test_point)
        item['distance'] = distance
    # lambda function for sorting derived from
    # https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/
    new_list = sorted(correct_year, key=lambda i:i['distance'])[0:k]
    if new_list == []:      #if there is no valid neighbors, default to return TRUE
        return "TRUE"
    else:
        return majority_vote(new_list)





