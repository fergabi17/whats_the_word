import re

"""
# FUNCTIONS FOR BENFORD'S LAW
"""

def apply_benford(messages, media):
    """
    @messages: array
    @media: array
    @returns: dict
    Calculates the percentage of how many numbers (representing the characters count)
    start with 1, 2, 3.... up to 9.
    """
    benford = {}
    clean_messages = get_clean_messages(messages, media)
    characters = get_chars_in_messages(clean_messages)
    grouped = group_numbers(characters)
    for number in grouped:
        try:
            benford[number] = round(grouped[number] / len(characters), 2)
        except:
            benford[number] = 0
    return benford


def get_clean_messages(messages, media):
    """ 
    @messages: array
    @media: array
    @returns: array
    Deletes the prefix of the messages and saves the messages body as an array,
    excluding mentions to media files and links.
    """
    links_pattern = r'http.+[/s$]'
    clean_messages = []
    for message in messages:
        find_prefix = re.findall(r'\[?\d{2}\/\d{2}\/\d{4}\,?\s.*\d{2}\:\d{2}\:?.+?\:', message)
        if len(find_prefix) > 0:
            message = re.sub(r'\[?\d{2}\/\d{2}\/\d{4}\,?\s.*\d{2}\:\d{2}\:?.+?\:\s?', '', message)
            for item in media:
                message = re.sub(fr'[\<\(]?\b{item}\b[\>\)]?', '', message)
            if len(message) > 0:
                message = re.sub(r'http.+[/s$]', '', message)
                clean_messages.append(message)
    return clean_messages


def get_chars_in_messages(clean_messages):
    """
    @messages_body: array
    @returns: array of int
    Checks the number of characters in each message
    and returns an array with the results
    """
    messages_chars = []
    for message in clean_messages:
        messages_chars.append(len(message))
        
    return messages_chars


def group_numbers(array_of_chars):
    """
    @array_of_chars: array
    @returns: dict
    Takes an array containing the quantity of characters for each message.
    Groups them by their first digit.
    """
    result = {
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

    for char_number in array_of_chars:
        for number in result:
            if str(char_number)[0] == number:
                    result[number] = result[number] + 1

    return result
