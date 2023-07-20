import os.path
import pyphen
import random
from pydub import AudioSegment
from pydub.playback import play

dic = pyphen.Pyphen(lang='en_EN')

def file_exists(file_name_start, file_name_end):
    if file_name_end < 10:
        soundname = str(file_name_start) + '_0' +  str( file_name_end) + '.mp3'
    else:
        soundname = str(file_name_start) + '_' +  str( file_name_end) + '.mp3'
    return os.path.exists('./src/r2d2 sound/syllables/' + soundname)

def file_name(file_name_start, file_name_end):
    if file_name_end < 10:
        soundname = str(file_name_start) + '_0' +  str( file_name_end) + '.mp3'
    else:
        soundname = str(file_name_start) + '_' +  str( file_name_end) + '.mp3'
    return './src/r2d2 sound/syllables/' + soundname

def count_num_of_symbol(word, char):
    return len([c for c in word if c == char])

def countLetters(word):
    count = 0
    for x in word:
        if x.isalpha():
            count = count + 1
    return count

syllables = []
column = 0
while(file_exists(column, 0)):
    row = []
    i = 0
    while(file_exists(column, i)):
        row.append(file_name(column, i))
        i += 1
    syllables.append(row)
    column += 1

def add_sound(count):
    while(count > 0):
        if count > 5:
            i = random.randrange(1,5)
        else:
            i = count
        pip_sound.append(syllables[i][random.randrange(0,len(syllables[i])-1)])   
        count -= i

def make_sound(text_to_speach):
    pip_sound = []
    combined = AudioSegment.empty()
    words = text_to_speach.split()
    finished_words = []
    for i in words:
        if i in finished_words:
            pip_sound.append(pip_sound[finished_words.index(i)])
        else:
            count = count_num_of_symbol(dic.inserted(i), '-')
            if countLetters(i) >= 5 or count == 0:
                count += 1

            if count <= 5:
                pip_sound.append(syllables[count][random.randrange(0,len(syllables[count])-1)]) 
            else:
               add_sound(count)
            
            if (count_num_of_symbol(i, ',') > 0 or count_num_of_symbol(i, '.') > 0):
                pip_sound.append(syllables[0][0])
        
        finished_words.append(i)
        
    for i in pip_sound:
        pip = AudioSegment.from_file(i, format="mp3")
        combined += pip
    path = './src/r2d2 sound/output/' + text_to_speach + '.mp3'
    if os.path.exists(path):
        os.remove(path)
    file_handle = combined.export(path, format="mp3")
    

with open('./sound text.txt', "r") as f:
    text = []
    for item in f:
        item = item.replace('\n' , '')
        text.append(item)
    for raw in text:
        make_sound(raw)