import os
import sys
from collections import Counter
from pprint import pprint
import nltk
from nltk.corpus import stopwords
import string

def read_file(src):
    with open(src, "r") as fp:
        return fp.readlines()

def get_msgs(contents):
    people = {
        "+61 424 993 883": "Ben", 
        "Oddball": "Dad",
        "Flower": "Ben",
        "Massive Water Dragon": "Mum",
        "Lani Peasant": "Lani",
        "sam": "Sam",
    }
    msgs = {
        "Ben": [],
        "Dad": [],
        "Mum": [],
        "Lani": [],
        "Sam": [],
    }

    for line in contents:
        line = line.replace("\n", " ")
        line = line.split(" - ")
        try: 
            # left side is date and time
            lfs = line[0].split(",")
            date = lfs[0].strip()
            time = lfs[1].strip()
            # right side is sender and message
            rhs = line[1].split(":")
            sender = people[rhs[0].strip()]
            msg = rhs[1].strip().lower()
            # group by person
            msgs[sender].append(msg.lower())
        except IndexError:
            # new line message just needs to be added to the last sender and message
            msgs[sender][-1] += f" {line}"
        except KeyError:
            msgs[sender][-1] += f" {line}"
    return msgs

def get_total(msgs):
    total = 0
    for msgs_list in msgs.values():
        total += len(msgs_list)
    return total

def get_number_of_times_word_said_by(msgs, person, word):
    count = 0
    for msg in msgs[person]:
        count += msg.count(word)
    return count


def who_said_x_the_most(msgs, word):
    most = ["", 0]
    for person in msgs:
        count = get_number_of_times_word_said_by(msgs, person, word)
        if count > most[1]:
            most = [person, count]
    return most[0], most[1]


def get_top_words_per_person(msgs):
    res = {}
    s = set(stopwords.words('english'))
    for sender, msg_list in msgs.items():
        words = []
        for msg in msg_list:
            words.extend(msg.split())
        # cant be bothered doing lambda filter list
        final_words = []
        for word in words:
            if word not in s and word not in string.punctuation and word != "<media" and word != "omitted>" and word != "i'm" and word != "]" and word != "[" and word != "']" and word != "['" and word != '"]':
                final_words.append(word)
        res[sender] = Counter(final_words).most_common(30)
    return res
    

def how_many_not_in_dict(msgs, dictionary):
    for sender, msg_list in msgs.items():
        count = 0
        words = []
        for msg in msg_list:
            words.extend(msg.split())
        for word in words:
            if word not in dictionary:
                count += 1
        print(f"{sender} wrote {count} words that weren't in the dictionary!")

def average(msgs):
    for sender, msg_list in msgs.items():
        total = 0
        for msg in msg_list:
            total += len(msg)
        av = total/len(msg_list)
        print(f"{sender}'s average length message was {av:.2f} words!")


def how_many_times_did_the_whole_family_say(msgs, word):
    count = 0
    for msgs_list in msgs.values():
        for msg in msgs_list:
            count += msg.count(word)
    return count


def main():
    contents = read_file("chat.txt")
    msgs = get_msgs(contents)
    total = get_total(msgs)

    with open("/usr/share/dict/web2", "r") as fp:
        dictionary = fp.readlines()
        for i, word in enumerate(dictionary):
            dictionary[i] = word.strip().lower()
        dictionary = set(dictionary)

    print(f"""
Total messages sent: {total}

Ben sent: {len(msgs['Ben'])}
Dad sent: {len(msgs['Dad'])}
Mum sent: {len(msgs['Mum'])}
Lani sent: {len(msgs['Lani'])}
Sam sent: {len(msgs['Sam'])}

Who said 'greve' the most? {who_said_x_the_most(msgs, 'greve')} times.
Who said 'stella' the most? {who_said_x_the_most(msgs, 'stella')} times.
Who said 'fat' the most? {who_said_x_the_most(msgs, 'fat')} times.
Who said 'dad' the most? {who_said_x_the_most(msgs, 'dad')} times.
Who said 'idiot' the most? {who_said_x_the_most(msgs, 'idiot')} times.

Who said 'chilli' the most? {who_said_x_the_most(msgs, 'chilli')} times.
Who said 'dad' the most? {who_said_x_the_most(msgs, 'dad')} times.
Who said 'ben' the most? {who_said_x_the_most(msgs, 'ben')} times.
Who said 'lani' the most? {who_said_x_the_most(msgs, 'lani')} times.
Who said 'sam' the most? {who_said_x_the_most(msgs, 'sam')} times.
Who said 'mum' the most? {who_said_x_the_most(msgs, 'mum')} times.

How many times did the whole family say 'copy'? {how_many_times_did_the_whole_family_say(msgs, 'copy')}
How many times did the whole family say 'chilli'? {how_many_times_did_the_whole_family_say(msgs, 'chilli')}
How many times did the whole family say 'fat'? {how_many_times_did_the_whole_family_say(msgs, 'fat')}
How many times did the whole family say 'stupid'? {how_many_times_did_the_whole_family_say(msgs, 'stupid')}
How many times did the whole family say 'stella'? {how_many_times_did_the_whole_family_say(msgs, 'stella')}

How many times did the whole family say 'mum'? {how_many_times_did_the_whole_family_say(msgs, 'mum')}
How many times did the whole family say 'ali'? {how_many_times_did_the_whole_family_say(msgs, 'ali')}

How many times did the whole family say 'canberra'? {how_many_times_did_the_whole_family_say(msgs, 'canberra')}
How many times did the whole family say 'angberra'? {how_many_times_did_the_whole_family_say(msgs, 'angberra')}
How many times did the whole family say 'ang'? {how_many_times_did_the_whole_family_say(msgs, 'ang')}

Who said 'media' the most? {who_said_x_the_most(msgs, 'media')} times.


How many times did the whole family say 'love'? {how_many_times_did_the_whole_family_say(msgs, 'love')}
""")

    how_many_not_in_dict(msgs, dictionary)

    print()

    average(msgs)

    # pprint(get_top_words_per_person(msgs))


if __name__=="__main__":
    sys.exit(main())