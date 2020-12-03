"""
Author: Harsh Desai
Description: Tokenizer utility class that wraps NLTK tokernizer and adds extra functionality.
"""
# -------------------- NLP libs --------------------- #
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
import string
from pathlib import Path
from collections import defaultdict




class Tokenizer:
    '''
    Tokeizer class lets you perform various forms of tokenizing, so far you can do:
    - Case Norm
    - NLTK Stopwords / Custom Stopword removal
    - Punctuation removal
    - Removing numerical values
    - Porter stemming
    - 5-Stemming
    - WordNet Lemmatizing
    '''

    def __init__(self, config_codes: str = 'u'):
        '''Initialize tokenizer with config codes'''
        self.config_codes = config_codes
        # parse-out config
        self.configs_list = self.config_codes.split('-')
        if not len(self.configs_list) > 0:
            raise ValueError('''
    config code needs to be passed in order to tokenize text.
    For e.g., to apply:
        - Case norm
        - STOPWORDS removal
        - Stemming
        tk = Tokenizer(configs = 'l-s-ps')
    ''')
        self.case_norm = False
        self.remove_stopwords = False
        self.remove_puncts = False
        self.remove_nums = False
        self.porter_stemmer = False
        self.five_stemmer = False
        for config in self.configs_list:
            config = config.lower().strip()
            if config == 'u':
                break
            if config == 'l':
                self.case_norm = True
            if config == 's':
                self.remove_stopwords = True
            if config == 'd':
                self.remove_nums = True
            if config == 'ps':
                self.porter_stemmer = True
            if config == '5s':
                self.five_stemmer = True
            if config == 'pt':
                self.remove_puncts = True
            if config == 'lm':
                self.wordnet_lemmatizer = True
        # init porter stemmer
        self.ps = PorterStemmer()
        # init lemmatizer
        self.lem = WordNetLemmatizer()
        # init pos tag dict
        self.tag_map = defaultdict(lambda : wn.NOUN)
        self.tag_map['J'] = wn.ADJ
        self.tag_map['V'] = wn.VERB
        self.tag_map['R'] = wn.ADV
        # NLTK STOPWORDS
        self.STOPWORDS = set(stopwords.words('english'))
        # punctuation regex
        self.punct_regex = re.compile('^[' + string.punctuation + ']+$')

    def tokenize(self, text: str) -> list:
        '''Converts text into desirable tokens based on config initialized.'''
        # strips out leading and trailing whitespace chars
        text = text.strip()
        # case normalize text
        if self.case_norm:
            text = self._case_norm(text)
        # remove numbers
        if self.remove_nums:
            text = self._remove_nums(text)
        # remove double or more white spaces
        text = re.sub(r'\s{2,}', ' ', text)
        # apply NLTK word tokenizer
        tokens = word_tokenize(text)
        # remove stopwords tokens
        if self.remove_stopwords:
            tokens = self._remove_stopwords(tokens)
        # remove punctuation tokens
        if self.remove_puncts:
            tokens = self._remove_puncts(tokens)
        # apply porter stemmer
        if self.porter_stemmer:
            tokens = self._perform_porter_stemming(tokens)
        # apply 5-stemmer
        if self.five_stemmer:
            tokens = self._perform_five_stemming(tokens)
        # apply wordnet lemmatizer
        if self.wordnet_lemmatizer:
            tokens = self._perform_lemmatizing(tokens)
        return tokens

    def _case_norm(self, text: str) -> str:
        return text.lower()

    def _remove_nums(self, text: str) -> str:
        return re.sub(r'\d+', ' ', text)

    def _remove_stopwords(self, tokens: list) -> list:
        return [token for token in tokens if token not in self.STOPWORDS]

    def _remove_puncts(self, tokens: list) -> list:
        return [token for token in tokens if not self.punct_regex.match(token)]

    def _perform_porter_stemming(self, tokens: list) -> list:
        return [self.ps.stem(token) for token in tokens]

    def _perform_five_stemming(self, tokens: list) -> list:
        return [token[:5] for token in tokens]

    def _perform_lemmatizing(self, tokens: list) -> list:
        return [self.lem.lemmatize(token, self.tag_map[tag[0]]) for token, tag in pos_tag(tokens)]

    def load_stop_words(self, stop_filepath: str, combine_w_nltk: bool = False) -> set:
        """Load custom stop words"""
        stop_filepath = Path(stop_filepath)
        if stop_filepath.exists():
            with open(stop_filepath, 'r', encoding="utf-8") as f:
                stopwords = f.readlines()
            stop_set = set(m.strip() for m in stopwords)
            if combine_w_nltk:
                self.STOPWORDS = self.STOPWORDS.union(stop_set)
            else:
                self.STOPWORDS = stop_set
            print('\tCustom STOPWORDS loaded successfully !(^^)!')
        else:
            raise FileNotFoundError(f"Can't find the stopwords list, check your file path: {stop_filepath}")

    def __str__(self):
        return str(self.__class__) + '\n' + '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

    def __repr__(self):
        return f'Tokenizer(config_codes="{self.config_codes}")'