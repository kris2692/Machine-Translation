# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:35:27 2017

@author: krish
"""
#Name:Krishna Sreenivas
#Student ID: 800984436

import re
from nltk import UnigramTagger, HiddenMarkovModelTagger
from nltk.corpus import cess_esp
from nltk.corpus import brown

#arrays to hold translated sentences 
sentences=[]
spanish_text=[]
direct_mapping=[]
improved_direct_mapping=[]
manual_translation=[]


#function to load the corpus onto an array
def input_corpus(filename):
	corpus = []
	with open(filename,encoding='utf-8') as f:
		for line in f:
			lines = line.split(":") #splitting the sentences into word
			if (lines):
				corpus.append(lines)
	return corpus

#loading dev and test and merging them
dev_set = input_corpus("spanish_devtrain.txt") 
test_set = input_corpus("spanish_test.txt")
test_set = dev_set + test_set

#loading the dictionary file into a dictionary type
def input_dictionary():
	with open("spanish_dictionary.txt",encoding='utf-8') as file:
		for line in file:
			lines = line.split(":") #splitting lines by spanish words and its corresponding english meanings
			spanish = str(lines[0])
			english = None
			if (len(lines) > 1):
				english = lines[1].strip("\n") #removing newline characters
				temp = english.split(",") #splitting multiple english meanings and creating a list out of them
			dictionary_words[spanish] = temp#appending the above created dictinary as a value to a spanish word present in the dictionary
			for w in temp:
				english_set.add(w) #creating unique vocabulary of english meanings
	return dictionary_words, english_set

#function to tag unigrams present in brown corpus
def tagger_unigram():
	lines = brown.tagged_sents()
	unigram_tags = UnigramTagger(lines)
	return unigram_tags

brown_tags_uni = tagger_unigram()

#function to load the tags and corresponding word into dictionary
def load_spanish_tags():
	tags = None
	if not tags:
		tags = dict()
		file = open("spanish-tags.txt", "r",encoding='utf-8') #loading the file
		for line in file:
			string = line.split(":")
			word = str(string[0]) #splitting them into words and tags
			spanish_tag = str(string[1])
			tags[word] = spanish_tag
		tags = tags
	return tags


#fetching the best candidate word based on the POS tags
def top_english_word(word):
	#Noun tags
    tag_noun = ('NN', 'NNS', 'NNP', 'NNPS', 'NR');
    plural_noun = ('NNS', 'NNPS');
    nom_pronoun_tag = ('PPS', 'PPSS', 'WPS')
    #Verb tags
    verb_present = ('VB','VBG', 'VBP', 'VBZ', 'BEG', 'BEM', 'BER', 'BEZ', 'DO', 'DOZ', 'HV', 'HVG', 'HVZ');
    verb_past = ('VBD', 'VBN', 'BED', 'BEDZ', 'BEN', 'DOD', 'HVD', 'HVN');
    first_verb = ('BED', 'BEDZ', 'BEM', 'BER');
    second_verb = ('BED', 'BER');
    third_verb = ('BED', 'BEDZ', 'BEZ', 'DOZ', 'HVZ', 'VBZ');
    imp_verb = ('BE', 'DO', 'HV', 'VB');
    inf_verb = ('BE', 'DO', 'HV', 'VB');
    verb = ('BED', 'BEDZ','BER', 'BEM', 'BEZ', 'DOZ', 'HVZ', 'VBZ');
    verb_plural_tag = ('BED', 'BER');                  
    gerund_tag = ('BEG', 'HVG', 'VBG');

	#Adjective tags
    adj_tag = ('JJ', 'JJ$', 'JJR', 'JJS', 'JJT');
    conj_tag = ('CC', 'CS', 'ABX', 'DTX');
    es_word = word['originalToken']
    es_tag = word['spanish_POS']
	# Generate the candidate words
    word_list = dictionary_words.get(es_word.lower(), None)
    chosen_en_wrd = None
    if word_list and es_tag:
      es_word_cat = es_tag[0]
		# Iterating to find the best candidate based on tag matching between the 2 langauges
      temp_list = word_list[:]
      for word in word_list:
        
			# If only one word is present in the list then, that word is taken
        if len(temp_list) == 1:
          break
        eng_tag = en_tags.get(word, None)
        if es_word_cat == 'n':
          
				
				# Removing words from candidate list which are not nouns
          if eng_tag not in tag_noun and word in temp_list:
            temp_list.remove(word)
          else:
            plural_tag = es_tag[3]	
            if (plural_tag == 'p'):
						# Removing plural nouns present in the candidate list
              if eng_tag not in plural_noun and word in temp_list:
                temp_list.remove(word)
        elif es_word_cat == 'v':
				
				#Removing gerunds in the list
          if es_tag[2] != 'g':
            
            if eng_tag in gerund_tag and word in temp_list:
              temp_list.remove(word)
				#removing imperative verbs in list
          if es_tag[2] == 'm':
            if eng_tag not in imp_verb and word in temp_list:
              temp_list.remove(word)
				#removing infinitive verbs 
          if es_tag[2] == 'n':
            if eng_tag not in inf_verb and word in temp_list:
              temp_list.remove(word)
				
          tenses_tag = es_tag[3]
          #Removing tenses of words in the candidate list
          if tenses_tag == 'p' or tenses_tag == '0':
             if eng_tag not in verb_present and word in temp_list:	
              temp_list.remove(word)
          if tenses_tag == 'f':
             if eng_tag not in inf_verb and word in temp_list:
              temp_list.remove(word)
          if tenses_tag == 's':
             if eng_tag not in verb_past and word in temp_list:
              temp_list.remove(word)
              
          person_tag = es_tag[4]
          #Removing the verbs based on person tag such as first person verb or third person verb etc
          if person_tag == '1':
            if eng_tag not in first_verb and word in temp_list:
              if word in temp_list: temp_list.remove(word)
          if person_tag == '2':
            if eng_tag not in second_verb and word in temp_list:
              if word in temp_list: temp_list.remove(word)
          if person_tag == '3':
            if eng_tag not in third_verb and word in temp_list:
              if word in temp_list: temp_list.remove(word)
				#Removing singular or plural verbs
          num_tag = es_tag[5]
          if num_tag == 's':
            if eng_tag not in verb and word in temp_list:
              if word in temp_list: temp_list.remove(word)
          else:
            if eng_tag not in verb_plural_tag and word in temp_list:
              temp_list.remove(word)
        elif es_word_cat == 's':
              if word in temp_list: temp_list.remove(word)
        elif es_word_cat == 'a':
				#Removing adjectives from candidate list
          if eng_tag not in adj_tag and word in temp_list:
            temp_list.remove(word)
        elif es_word_cat == 'c':
				#Removing conjunctions from candidate list
          if eng_tag not in conj_tag and word in temp_list:
				#Removing prepositions from candidate list
                if eng_tag != 'IN' and word in temp_list:
                  temp_list.remove(word)
        elif es_word_cat == 'p' and es_tag[5] == 'n':
          
				#Removing nominative pronouns from candidate list
                
          if eng_tag not in nom_pronoun_tag and word in temp_list:
            temp_list.remove(word)
      if chosen_en_wrd == None:
        if len(temp_list) > 0:
          chosen_en_wrd = temp_list[0].strip()
        else:
          chosen_en_wrd = word_list[0]
    elif (es_tag == None) and word_list:
		#if theres no tag, first word from the list is chosen by default
      chosen_en_wrd = word_list[0]
    return chosen_en_wrd

dictionary_words = dict()
english_set = set()

dictionary_words,english_Set = input_dictionary()

#fucntion to create a dictionary of english tags
def english_tag_dict():
	en_dict = dict()
	temp = []
	for w in english_Set:
		temp.append(w)
	tag_word = brown_tags_uni.tag(temp)
	for word_tags in tag_word:
		en_dict[word_tags[0]] = word_tags[1]
	return en_dict

en_tags = english_tag_dict()

#function to fetch spanish words corresponding to a particular english word
def english_spanish(spanish):
	english_words = dictionary_words.get(spanish.lower(), None)
	return english_words
        
#this function performs the direct machine translation of spanish vs english sentences  
def convert_sent(spanish_sent):
	text_translated = [] #list to store translated text
	sent_translated = "" #string to store translated string
	spanish_words = re.compile('(\W+)', re.UNICODE).split(str(spanish_sent)) #splitting the spanish sentences into words

    #mappping english words based on corresponding word
	for word in spanish_words:
		wrds_translated = english_spanish(word)
		if wrds_translated:
			word_translated = wrds_translated[0]
			text_translated.append(word_translated)
		else:
			text_translated.append(word)
   #concatenating translated texts into sentences.         
	for word in text_translated:
		sent_translated = sent_translated + word
	return sent_translated

for translation in test_set:
  spanish = translation[0] #splitting the test set into spanish and english sentences
  english = translation[1]
  translation_dict = []
  improved_translation = "" #variable to hold translated sentences using improved method


	#performing direct translation 
  direct_translation = convert_sent(spanish)

	#performing modified translation 
  sp_words = re.compile('(\W+)', re.UNICODE).split(str(spanish))
  sp_words.pop()
	#preprocessing text for modified translation
  for pos, word in enumerate(sp_words):
    word_dict = dict()
    word_dict['originalToken'] = word
    word_dict['spanish_POS'] = load_spanish_tags().get(word, None)
    if (len(word) > 0):
      if word[0].isupper():	
        word_dict['upper'] = True
      else:
        word_dict['upper'] = False
    else:
      word_dict['upper'] = False
    translation_dict.append(word_dict)
    
  for spanish_word in translation_dict:
    original_word = spanish_word['originalToken']
    modified_word = top_english_word(spanish_word)
    if modified_word:
      spanish_word['translatedToken'] = modified_word
    else:
      spanish_word['translatedToken'] = original_word
  for array in translation_dict:
    converted_array = array['translatedToken']
    improved_translation = improved_translation + converted_array
    
  #storing translated and actual texts into lists  
  spanish_text.append(spanish)
  direct_mapping.append(direct_translation)
  improved_direct_mapping.append(improved_translation)
  manual_translation.append(english)
  
#printing the texts based on category
print("###############Spanish Text###############")
for i in range(len(spanish_text)):
  print(i,":",spanish_text[i])

print("###############Direct Translation###############")
for i in range(len(direct_mapping)):
  print(i,":",direct_mapping[i])
  
print("###############Improved Direct Translation###############")
for i in range(len(improved_direct_mapping)):
  print(i,":",improved_direct_mapping[i])
  
print("###############Manual Translation###############")  
for i in range(len(manual_translation)):
  print(i,":",manual_translation[i])