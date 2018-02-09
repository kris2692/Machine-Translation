#Name: Krishna Sreenivas
#Student ID: 800984436

import sys
import string

#variables to hold english,spanish and langauge pairs
eng_word_sentences  = []
words_english = []
spanish_word_sentences  = []

#function to create 1 to 1 combination of english and spanish sentences
def es_en_sentences(eng_word_sentences, spanish_word_sentences):
  tuples = []
  for index in range(len(eng_word_sentences)):
    temp = (eng_word_sentences[index], spanish_word_sentences[index])
    tuples.append(temp) #appending the 1 to 1 combination to a list
  return tuples

words_spanish = []
es_en_tuples = [] 

#calculating uniform probabilities of words
def uniform_prob(words_spanish, potential_candidates):
  translation_probabilities = {}
  for w in words_spanish: #for each candidate word in spanish obtain the corresponding potential candidate
    candidate = potential_candidates[w]
    if (len(candidate)==0):
      print(w, candidate)
    uniform_probability = 1.0 / len(candidate) #calculate the uniform probability of that candidate
    uniform_word_probabilities = dict( [(w, uniform_probability) for w in candidate] )
    translation_probabilities[w] = uniform_word_probabilities #store the uniform word probabilities as a value to a dictionary with spanish word as key
  return translation_probabilities

#variables to hold potential candidate set and translation probabilities    
potential_candidates = {}
translation_probabilities   = {} 

#loading corpuses and creating dictionaries
def creating_dictionary(filename):
  language_dictionary  = []
  language_words = []
  #stripping new line characters from a line and appending it to a list
  file = open(filename, 'r',encoding='Latin-1')
  for sent in file.readlines():
    language_dictionary.append( sent.rstrip() )
    language_words = language_words + sent.split()
  file.close()
  #creating unique vocabulary of words
  language_words = list( set(language_words) )
  return language_dictionary, language_words

#writing the translated texts to a file
def output_translation(spanish_word_sentences,translation_probabilities):
  file = open('translation_ibm.txt', 'w',encoding='Latin-1') #specifying the encoding mechanism as Latin-1
  print("Writing to file")
  for sent in spanish_word_sentences:
    translated_eng_sentence = ""
    for w in sent.split(): #splitting the sentences in to word 
      eng_word = translation_probabilities[w] #storing the probabilities based on word
      temp = sorted(iter(eng_word.items()), key=lambda key_value_pair: (key_value_pair[1],key_value_pair[0]))
      temp.reverse() #sorting in decreasing order
      (best_candidate, value) = temp[0] #since the list is in descresing order, the first index gives the best word based on  probability value
      translated_eng_sentence+=best_candidate+" "
    file.write(translated_eng_sentence+"\n")

def gradient_descent(es_en_tuples,count_sentences,translation_probabilities,words_spanish,potential_candidates):
  flag = False #variables to control iterations
  grad_descent_val = 0
  while not(flag):
    conditional_prob_occurrence,spanish_word_probability = reset_count(words_spanish, potential_candidates) #resetting the probability occurrences to 0
    for (en_sent, es_sent) in es_en_tuples:
      en_sent_split = en_sent.split() #splitting the 1 to 1 combination of language sentences 
      es_sent_split = es_sent.split()
      for eng_sent in en_sent_split:
        count_sentences[eng_sent] = 0 #initial count set to 0
        for esp_sent in es_sent_split: 
          esp_probability = translation_probabilities[esp_sent] #obtaining the translation probabilities based on spanish sentences
          if (eng_sent not in esp_probability):
            continue
          count_sentences[eng_sent] += esp_probability[eng_sent]
        for esp_sent in es_sent_split:
          if (eng_sent not in translation_probabilities[esp_sent]):
            continue
          conditional_prob_occurrence[esp_sent][eng_sent] += translation_probabilities[esp_sent][eng_sent] / count_sentences[eng_sent] #calculating conditional probability counts
          spanish_word_probability[esp_sent] += translation_probabilities[esp_sent][eng_sent] / count_sentences[eng_sent]
    for esp_sent in words_spanish:
      esp_candidate = potential_candidates[esp_sent]
      for eng_sent in esp_candidate: #claculating the intermediate translation probabilities 
        translation_probabilities[esp_sent][eng_sent] = conditional_prob_occurrence[esp_sent][eng_sent] / spanish_word_probability[esp_sent]
    if (grad_descent_val>=10): #iterating 10 times to get finer probability values
      flag = True
    grad_descent_val += 1 #incrementing loop counter by 1
    
#variables to hold conditional probability, spanish word probability based on the count and variable to count sentences
conditional_prob_occurrence = {} 
spanish_word_probability  = {} 
count_sentences  = {}

#Creating a list of potential candidate words based on the corresponding spanish words
def word_prob(words_spanish, spanish_word_sentences, eng_word_sentences):
  potential_candidates = {} #dictionary to hold potential translations based on english word
  for w in words_spanish:
    candidate_words = [] #list to hold candidate translations
    for line in spanish_word_sentences:
      if w in line: #checking if a spanish word is occurring in a spanish sentence
        candidate_sent = eng_word_sentences[ spanish_word_sentences.index(line) ] #storing the corresponding english word based on spanish word
        candidate_words = candidate_words + candidate_sent.split()
    candidate_words = list( set(candidate_words) ) #creating unique vocab of candidate words
    potential_candidates[w] = candidate_words #assigning the candidate list of words as a value to spanish word
  return potential_candidates

#function to reset the count of occurrences for the purpose of gradient descent 
def reset_count(words_spanish, potential_candidates):
  conditional_prob_occurrence = {}
  spanish_word_probability = {}
  for w in words_spanish:
    candidate = potential_candidates[w]#obtain the corresponding candidate 
    reset = dict( [(w, 0) for w in candidate] ) #reset the count of the word to 0
    conditional_prob_occurrence[w] = reset
    spanish_word_probability[w] = 0
  return conditional_prob_occurrence,spanish_word_probability


#main function to call corresponding functions
def main(es_en_tuples,potential_candidates,translation_probabilities,count_sentences):
  print("Please wait....")
  eng_word_sentences, words_english = creating_dictionary( sys.argv[1] )
  spanish_word_sentences, words_spanish = creating_dictionary( sys.argv[2] )
  es_en_tuples = es_en_sentences(eng_word_sentences, spanish_word_sentences)
  print("Processing....")
  potential_candidates = word_prob(words_spanish, spanish_word_sentences, eng_word_sentences)
  translation_probabilities = uniform_prob(words_spanish, potential_candidates)
  print("Gradient descent value set to 10")
  gradient_descent(es_en_tuples,count_sentences,translation_probabilities,words_spanish,potential_candidates)
  output_translation(spanish_word_sentences,translation_probabilities)

#args = sys.argv
main(es_en_tuples,potential_candidates,translation_probabilities,count_sentences)
print("Translation dumped to file 'translation_ibm.txt'")