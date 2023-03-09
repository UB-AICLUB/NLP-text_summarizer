import bs4 as bs
import urllib.request
import re
import nltk
import heapq

nltk.download('punkt')
nltk.download('stopwords')

"""
Text Summarization steps:
1.Obtain Data
2.Text Preprocessing
3.Convert paragraphs to sentences
4.Tokenizing the sentences
5.Find weighted frequency of occurrence
6.Replace words by weighted frequency in sentences
7.Sort sentences in descending order of weights
8.Summarizing the Article
"""
link = input('link: ')

scraped_data = urllib.request.urlopen(link)
article = scraped_data.read()
parsed_article = bs.BeautifulSoup(article,'lxml')
paragraphs = parsed_article.find_all('p')
article_text = ""
for p in paragraphs:
    article_text += p.text

# print(article_text)

# preprocess
# Removing Square Brackets
article_text = re.sub(r'[[0-9]*]', ' ', article_text)

# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )

# convert to sentances
sentence_list = nltk.sent_tokenize(article_text)

# Finding weighted frequencies of occurrence
stopwords = nltk.corpus.stopwords.words('english')
word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

# Calculate sentence scores
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]


summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)
print(summary)