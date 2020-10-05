import os
import math


def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    # TODO: add your code here
    with open(filepath) as f:
        for line in f.readlines():
            if (line.strip() in vocab) and (line.strip() not in bow.keys()):
                bow.update({line.strip(): 1})
            elif (line.strip() in vocab) and (line.strip() in bow.keys()):
                bow.update({line.strip(): bow[line.strip()]+1})
            elif (line.strip() not in vocab) and (None not in bow.keys()):
                bow.update({None: 1})
            elif (line.strip() not in vocab) and (None in bow.keys()):
                bow.update({None: bow[None]+1})
    return bow


def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    dataset = []
    # TODO: add your code here
    t2016 = [x for x in os.listdir(directory + '2016/')]
    t2020 = [x for x in os.listdir(directory + '2020/')]
    for i in t2016:
        dataset.append({'label': '2016', 'bow': create_bow(vocab, directory+'2016/'+i)})
    for i in t2020:
        dataset.append({'label': '2020', 'bow': create_bow(vocab, directory + '2020/' + i)})
    return dataset


def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """
    vocab = []
    tokens = []
    count = []
    # TODO: add your code here
    t2016 = [x for x in os.listdir(directory + '2016/')]
    t2020 = [x for x in os.listdir(directory + '2020/')]
    for i in t2016:
        with open(directory+'2016/'+i, 'r') as f:
            for line in f.readlines():
                if line.strip() not in tokens:
                    tokens.append(line.strip())
                    count.append(1)
                else:
                    count[tokens.index(line.strip())] += 1
    for i in t2020:
        with open(directory+'2020/'+i, 'r') as f:
            for line in f.readlines():
                if line.strip() not in tokens:
                    tokens.append(line.strip())
                    count.append(1)
                else:
                    count[tokens.index(line.strip())] += 1
    for i in range(len(count)):
        if count[i] >= cutoff:
            vocab.append(tokens[i])
    return sorted(vocab)


def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    logprob = {}
    # TODO: add your code here
    count_2016 = 0
    files_total_num = len(training_data)
    for i in training_data:
        if i['label'] == '2016':
            count_2016 += 1
    for i in label_list:
        if i == '2016':
            logprob.update({i: math.log((count_2016 + smooth)/(files_total_num + 2))})
        elif i == '2020':
            logprob.update({i: math.log((files_total_num - count_2016 + smooth) / (files_total_num + 2))})
    return logprob


def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """
    
    smooth = 1 # smoothing factor
    word_prob = {}
    # TODO: add your code here
    for i in vocab:
        word_prob.update({i: 0})
    word_prob.update({None: 0})
    for i in training_data:
        if i['label'] == label:
            for j in i['bow'].keys():
                word_prob.update({j: word_prob[j] + i['bow'][j]})
    total_word_types = len(word_prob)
    total_words = 0
    for i in word_prob.keys():
        total_words += word_prob[i]
    for i in word_prob.keys():
        word_prob.update({i: math.log((word_prob[i] + smooth)/(total_words + total_word_types))})
    return word_prob

    
##################################################################################
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    # TODO: add your code here
    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    log_prior = prior(training_data, ['2020', '2016'])
    log_p2020 = p_word_given_label(vocab, training_data, '2020')
    log_p2016 = p_word_given_label(vocab, training_data, '2016')
    retval.update({'vocabulary': vocab, 'log prior': log_prior, 'log p(w|y=2020)': log_p2020, 'log p(w|y=2016)': log_p2016})
    return retval


def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>, 
             'log p(y=2016|x)': <log probability of 2016 label for the document>, 
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
    # TODO: add your code here
    multi_2020 = model['log prior']['2020']
    multi_2016 = model['log prior']['2016']
    with open(filepath) as f:
        for line in f.readlines():
            if line.strip() in model['vocabulary']:
                multi_2020 += model['log p(w|y=2020)'][line.strip()]
                multi_2016 += model['log p(w|y=2016)'][line.strip()]
            else:
                multi_2020 += model['log p(w|y=2020)'][None]
                multi_2016 += model['log p(w|y=2016)'][None]
    if multi_2016 > multi_2020:
        retval.update({'predicted y': '2016', 'log p(y=2016|x)': multi_2016, 'log p(y=2020|x)': multi_2020})
    elif multi_2016 < multi_2020:
        retval.update({'predicted y': '2020', 'log p(y=2016|x)': multi_2016, 'log p(y=2020|x)': multi_2020})
    return retval


model = train('./corpus/training/', 2)
print(classify(model, './corpus/test/2016/0.txt'))