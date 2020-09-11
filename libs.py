import re
import json
import pymongo
import math
from collections import Counter
from bson.objectid import ObjectId

import benford_law


def get_data_from_whats(file_content):
    """""
    @file_content: string
    @returns: dict
    Runs several funcions on the file content and returns
    a dictionary with data about the chat.
    """
    prefixes = get_prefixes(file_content)
    period = get_period(prefixes)
    messages = get_messages(file_content)
    messages_body = get_messages_body(messages)
    
    longest_word = get_longest_word(messages_body)
    popular_words = get_popular_words(messages_body)
    word_combinations = get_word_combinations(messages_body) 

    word_1_dates = get_word_info(popular_words[0][0], messages)
    word_2_dates = get_word_info(popular_words[1][0], messages)
    word_3_dates = get_word_info(popular_words[2][0], messages)
    
    word_seq_1_dates = get_word_info(word_combinations[0][0], messages)
    word_seq_2_dates = get_word_info(word_combinations[1][0], messages)
    word_seq_3_dates = get_word_info(word_combinations[2][0], messages)
    
    words_result = {
        "messages": len(prefixes),
        "participants": get_participants(prefixes),
        "period": period,
        "period_length": get_period_length(period),
        "links": get_links(messages),
        "media": get_media(messages),
        
        "words": get_popular_words(messages_body),
        "word_1_result": get_monthly_frequency(word_1_dates),
        "word_2_result": get_monthly_frequency(word_2_dates),
        "word_3_result": get_monthly_frequency(word_3_dates),
        
        "longest_word": longest_word,
        "longest_word_dates": get_word_info(longest_word, messages),
        
        "word_combinations": word_combinations,
        "word_seq_1_result": get_monthly_frequency(word_seq_1_dates),
        "word_seq_2_result": get_monthly_frequency(word_seq_2_dates),
        "word_seq_3_result": get_monthly_frequency(word_seq_3_dates),
        
        "benford": benford_law.apply_benford(messages, media)
    }      

    return words_result


ignored_words = [
    "http.+",
    # EN
    "i\'m",
    "am",
    "your",
    "i",
    "to",
    "be",
    "the",
    "and",
    "with",
    "on",
    "that",
    "how",
    "what",
    "in",
    "it",
    "you",
    "for",
    "if",
    "is",
    "are",
    "my",
    "but",
    "of",
    "we",
    "will",
    "have",
    "at",
    "this",
    "he",
    "she",
    "was",
    "one",
    "or",
    "not",
    "can",
    # PT
    "o",
    "a",
    "os",
    "as",
    "e",
    "um",
    "uma",
    "até",
    "com",
    "de",
    "do",
    "da",
    "desde",
    "em",
    "entre",
    "para",
    "por",
    "sem",
    "sob",
    "que",
    "pra",
    "me",
    "te",
    "se",
    "é",
    "eu",
    "meu",
    "minha",
    "mas",
    "voce",
    "vc",
    "no",
    "na",
    "vai",
    "ta",
    "tem",
    "foi",
    "esse",
    "isso",
    "ou",
    "tá",
    "aí",
    "ele",
    "ela",
    "nao",
    "não",
    "sim",
    # FR
    "la",
    "le",
    "les",
    "et",
    "sur",
    "je",
    "ça",
    "tu",
    "pour",
    "ne",
    "pas",
    "mais",
    "bien",
    "vous",
    "est",
    "un",
    "c'est",
    "avec",
    "suis",
    "si",
    "va",
    "ma",
    "ce",
    "en",
    "moi",
    "il",
    "au",
    "du",
    "j'ai"
]

media = [
    "\w+\somitted",
    "\w+\sattached",
    
    "imagem ocultada",
    "imagem anexada",
    "figurinha omitida",
    "vídeo omitido",
    "vídeo anexado",
    "arquivo anexado",
    "arquivo de mídia oculto",
    "áudio ocultado",
]

def process_ignored_words(ignored):
    """
    """
    user_ignored = re.findall(r'\w+', ignored)
    if len(user_ignored) > 0:
        for word in user_ignored:
            ignored_words.append(word.lower())
    return user_ignored


def get_prefixes(messages):
    """
    @messages: string
    @returns: array
    Gets the prefixes for all messages sent in the following format:
    07/07/2019, 18:34 - Participant Name:
    Returns an array with all entries
    """
    prefixes = re.findall(r'\[?\d{2}\/\d{2}\/\d{4}\,?\s\d{2}\:\d{2}\:?.+?\:',
                          messages)

    return prefixes


def get_participants(prefixes):
    """
    @prefixes: array
    @returns: array
    Extracts the name of the participant for every message prefix.
    Returns a list with all names, skipping duplicates.
    """
    participants_names = []
    for prefix in prefixes:
        name = get_participant_name(prefix)
        participants_names.append(name)
    return Counter(participants_names).most_common()


def get_participant_name(prefix):
    """
    @prefix: string
    @returns: string
    It extracts the name of a participant
    from a string containing a prefix.
    """
    name = re.findall(r'[\-\]]\s.+?\:', prefix)
    return re.sub(r'^[\]-]\s', '', name[0]).replace(':', '')


def get_date(prefix):
    """
    @message: string
    @returns: string
    Extracts the date from a string containing a prefix.
    """
    try:
        return re.findall(r'\d{2}\/\d{2}\/\d{4}', prefix)[0]
    except:
        return ""


def get_period(prefixes):
    """
    @prefixes: array
    @returns: tuple
    Returns the start and the end date of messages in the file
    """
    start_date = get_date(prefixes[0])
    end_date = get_date(prefixes[len(prefixes) - 1])
    return (start_date, end_date)


def get_period_length(period):
    """
    @period: string
    @returns: int
    Extracts the number of months in a given period
    """
    end_date = {"year": int(period[1][6:10]), "month": int(period[1][3:5])}
    start_date = {"year": int(period[0][6:10]), "month": int(period[0][3:5])}

    return (end_date["year"] - start_date["year"]) * 12 + (end_date["month"] -
                                                           start_date["month"])


def get_messages_body(messages):
    """ 
    @messages: array
    @returns: string
    Deletes all prefixes, returning the body of all
    messages as a string.
    """
    messages_body = ""
    for message in messages:
        new_message = re.sub(r'\[?\d{2}\/\d{2}\/\d{4}\,?\s\d{2}\:\d{2}\:?.+?\:', '\n',
                            message)
        messages_body = messages_body + new_message
        
    return messages_body


def get_popular_words(messages_body):
    """
    @messages_body: string
    @returns: array of tuples
    Extracts the most popular words in the body of the messages, 
    ignoring common words.
    Returns an array of tuples, containing the word and how
    many times it appeared
    """
    ignored = media + ignored_words
    for word in ignored:
        messages_body = re.sub(fr'\b{word}\b(?!\')', "", messages_body)
    all_words = re.findall(r'\w+\'?\w+', messages_body)

    if len(all_words) > 10:
        return Counter(all_words).most_common(10)
    else:
        return Counter(all_words).most_common(len(all_words))


def get_longest_word(messages_body):
    """
    @messages_body: string
    @returns: string
    Returns the longest word found in the messages body
    """
    messages_body = re.sub(r'http.+', "", messages_body)
    words = re.findall(r'[\w\']+', messages_body)
    return max(words, key=len)


def get_word_info(word, messages):
    """ 
    @word: string
    @messages: array
    @returns: array of tuples
    Gets the date and the participant that said the word in the messages.
    """
    word_info = []
    messages_with_word = []
    
    for message in messages:
        word_in_message = re.findall(rf'\b{word}\b', message)
        if len(word_in_message ) > 0:
            for word_appearance in word_in_message:
                messages_with_word.append(message)
                
            # if word in prefix desconsider
            word_in_prefix = get_prefixes(message)
            words_found_in_prefix = re.findall(rf'\b{word}\b', word_in_prefix[0])
            if len(words_found_in_prefix) > 0: 
                for word in words_found_in_prefix:
                    del messages_with_word[-1]
            

    for message in messages_with_word:
        word_info.append((get_date(message), get_participant_name(message)))

    return word_info


def get_monthly_frequency(word_info):
    """
    @word_info: array of tuples
    @returns: dict
    Creates a dictionary with the frequency a word was used each month.
    """
    date_string = r'\d\d\/\d\d\d\d$'
    result = {}

    for info in word_info:
        current_date = re.findall(date_string, info[0])[0]
        if current_date in result:
            result[current_date] = result[current_date] + 1
        else:
            result[current_date] = 1
    return result


def get_messages(file_content):
    """
    @file_content: string
    @returns: array
    Breaks the full file content in an array of messages
    """
    # Clean the new lines in the same message
    clean_messages = re.sub(r'[\n\r](?!(\[?\d\d\/\d\d\/\d\d\d\d|\u200e))', ' ',
                            file_content)

    return re.findall(r'\d{2}\/\d{2}\/\d{4}\,?\s\d{2}\:\d{2}\:?.+?\:.+',
                      clean_messages)


def get_links(messages):
    """
    @messages: array
    @returns: array
    Counts all links sent by every chat participant
    """
    links_pattern = r'http.+[/s$]'
    links_messages = []
    for message in messages:
        links = re.findall(links_pattern, message)
        if (len(links) > 0):
            link_sender = get_participant_name(message)
            links_messages.append(link_sender)
    return Counter(links_messages).most_common()


def get_media(messages):
    """
    @messages: array
    @returns: array
    Counts all media sent by every chat participant
    """
    media_messages = []
    for message in messages:
        for item in media:
            medias = re.findall(fr'\b{item}\b', message)
            if (len(medias) > 0):
                media_sender = get_participant_name(message)
                media_messages.append(media_sender)
    return Counter(media_messages).most_common()


def get_word_combinations(messages_body):
    """
    @messages_body: array
    @returns: array of tuples
    Extracts the most popular combination of 3 words in the body of the messages.
    Returns an array of tuples, containing the word sequence and how
    many times it appeared
    """
    for word in media:
        messages_body = re.sub(fr'\b{word}\b(?!\')', "", messages_body)
    all_words_combinations = re.findall(r'\b[\w\-\']+\s[\w\-\']+\s[\w\-\']+', messages_body)

    return Counter(all_words_combinations).most_common(5)


def get_global_results(inputs):
    """
    @inputs: inputs obj from the database
    @returns: dict
    Process data along all the inputs
    from the database and returns the most commom
    """
    #inputs = inputs.find()
    global_results = {
        'benford': get_global_benford(inputs.find()),
        'count': inputs.find().count(),
        'words': get_global_words(inputs.find())
    }
    return global_results

def get_global_words(inputs):
    """
    @inputs: cursor
    @returns: array of tuples
    Gathers all the most common words among all 
    inputs and returns the 20 most commom from them
    """
    all_words = []
    for the_input in inputs:
        for word_tuple in the_input["words"]:
            all_words.append(word_tuple[0])
    return Counter(all_words).most_common(20)


def get_global_benford(inputs):
    """
    @inputs: cursor
    @returns: array of tuples
    Gathers all the most common words among all 
    inputs and returns the 20 most commom from them
    """
    global_benford = {
        '1':0,
        '2':0,
        '3':0,
        '4':0,
        '5':0,
        '6':0,
        '7':0,
        '8':0,
        '9':0
    }
    for the_input in inputs:
        for digit in the_input['benford']:
            global_benford[digit] = global_benford[digit] + the_input['benford'][digit]
        
    for digit in global_benford:
        global_benford[digit] = math.floor(global_benford[digit] * 100 / inputs.count())
    
    return global_benford 

