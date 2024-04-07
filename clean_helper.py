import re
import pandas as pd

def clean(text):
    # lower case
    text = text.lower()
    # clean html entity (&{char};), emoticon (\\{char}), and @user tweet
    text = re.sub(r'&([^;]+);|\\x[a-z0-9]{2}|\\n|@([a-z0-9]+)\s', ' ', text)
    # clean rt, user
    # add white space before after sentence
    text = " "+text+" "
    text = text.replace(' rt ', ' ').replace(' user ', ' ')
    # clean special char except alphanumeric, whitespace
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # clean multiple whitespace
    text = re.sub(r'\s+', ' ', text)
    # clean whitespace at before/after sentence
    text = re.sub(r'^\s+|\s+$', '', text)
    return text

def word_substitute(text, kamus):
    # add white space before after sentence
    text = " "+text+" "
    # iterate kamus
    for word in kamus:
        # replace slay word
        text = text.replace(" "+word[0]+" ", " "+word[1]+" ")
    
    # clean whitespace at before/after sentence
    text = re.sub(r'^\s+|\s+$', '', text)
    print(text)
    return text

def kamus_alay():
    # read kamus alay and convert to array
    df_kamusalay = pd.read_csv('data/new_kamusalay.csv', header=None, encoding='latin1')
    kamus = [tuple(row) for index, row in df_kamusalay.iterrows()]
    return kamus

def kamus_abusive():
    # read kamus abusive and convert to array
    df_abusive = pd.read_csv('data/abusive.csv', header=None, encoding='latin1')
    kamus = [tuple(row) for index, row in df_abusive.iterrows()]
    return kamus

def total_abusive(text, kamus):
    count = 0
    # iterate kamus
    for word in kamus:
        if word[0] in text:
            count += 1
    return count

def text_abusive_word(text, kamus):
    txt = ' '
    # iterate kamus
    for word in kamus:
        if word[0] in text:
            txt = txt + word[0] + ' '
    txt = re.sub(r'^\s+|\s+$', '', txt)
    return txt

def check_min_outliers(df):
    # Calculate percentile
    p75 = df.quantile(0.75)
    p25 = df.quantile(0.25)
    # Calculate IQR
    iqr = p75 - p25
    
    # "Minimum non-outlier value": 25th percentile - 1.5 * IQR
    min_val = p25 - 1.5*iqr

    if min_val < df.min():
        return "Tidak ada outlier dari sisi batas bawah"
    else:
        return "Ada outlier dari sisi batas bawah"
    
def check_max_outliers(df):
   # Calculate percentile
    p75 = df.quantile(0.75)
    p25 = df.quantile(0.25)
    # Calculate IQR
    iqr = p75 - p25
    
    # "Maximum non-outlier value": 75th percentile + 1.5 * IQR
    max_val = p75 + 1.5*iqr
    
    if max_val > df.max():
        return "Tidak ada outlier dari sisi batas atas"
    else:
        return "Ada outlier dari sisi batas atas"