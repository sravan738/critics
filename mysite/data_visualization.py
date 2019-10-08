import json
import re
from mysite.tokens import Utilities
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk import pos_tag


class visualize:
    def __init__(self, review):
        self.review = review

    def process(self):
        result = {}
        # step1 Tokenization
        result.update({"tokenization": self.tokenization})

        # step2 Removing stop words
        result.update({"remove_stop_words": self.remove_stop_words})

        # step3 Character casing
        result.update({"character_casing": self.character_casing})

        # step4 Negation
        result.update({"negation": self.negation})

        # step5 Stemming
        result.update({"stemming": self.stemming})

        # step6 POS(parts of speech)-Tagging
        result.update({"pos_tagging": self.pos_tagging})

        # Step 7 Analyser
        result.update({"analyser": self.analyser})

        return result

    @property
    def tokenization(self):
        exclude = "?:!.,;.-_`~+=#()/\|][*' "
        words = self.review.lower().split(" ") if Utilities.isheader(self.review) else [self.review.lower()]
        self.review = [word.strip(exclude) for word in words if word.strip(exclude)]
        return self.review

    @property
    def remove_stop_words(self):
        stop_words = stopwords.words('english')
        stop_words.append('nt')
        self.review = [word for word in self.review if word not in stop_words]
        return self.review

    @property
    def character_casing(self):
        return_text = []
        for text in self.review:
            try:
                if text.isnumeric():
                    return_text.append(Utilities().convert_int_to_text(text))
                else:
                    return_text.append(text)
            except Exception as e:
                pass
        self.review = return_text
        return self.review

    @property
    def negation(self):
        negation_text = []
        for word in self.review:
            if word.endswith("n't"):
                negation_text.extend([word[:-3], "not"])
            else:
                negation_text.append(word)
        self.review = negation_text
        return self.review

    @property
    def stemming(self):
        # stemming using PorterStemmer
        ps = PorterStemmer()
        porter_stemmer_text = [ps.stem(word) for word in self.review]

        # stemming using SnowballStemmer
        ss = SnowballStemmer('english')
        snowball_stemmer_text = [ss.stem(word) for word in self.review]

        # stemming using WordNetLemmatizer
        wnl = WordNetLemmatizer()
        word_net_lemmatizer_stemmer_text = [wnl.lemmatize(word) for word in self.review]

        self.review = word_net_lemmatizer_stemmer_text
        stemming_map = {
            "porter_stemmer_text": porter_stemmer_text,
            "snowball_stemmer_text": snowball_stemmer_text,
            "word_net_lemmatizer_stemmer_text": word_net_lemmatizer_stemmer_text
        }
        return stemming_map

    @property
    def pos_tagging(self):
        pos_tagged_review = {}
        number_of_proper_nouns = 0
        number_of_other_nouns = 0
        number_of_pronouns = 0
        number_of_conjunction = 0
        number_of_present_verb = 0
        number_of_past_verb = 0
        number_of_participle = 0
        number_of_adjective = 0
        number_of_interjection = 0
        tagged_text = []
        for word in self.review:
            tagged_word = pos_tag([word])
            tagged_text.extend(tagged_word)
            pos = tagged_word[0][1]
            if re.match('NNP', pos):
                number_of_proper_nouns += 1
            elif re.match('NN.*', pos):
                number_of_other_nouns += 1
            elif re.match('VBD', pos):
                number_of_past_verb += 1
            elif re.match('VBG', pos):
                number_of_participle += 1
            elif re.match('VB[Z,P]', pos):
                number_of_present_verb += 1
            elif re.match('[W,PR]P', pos):
                number_of_pronouns += 1
            elif re.match('CC', pos):
                number_of_conjunction += 1
            elif re.match('JJ', pos):
                number_of_adjective += 1
            elif re.match('DT', pos):
                number_of_interjection += 1
                
        pos_tagged_review["number_of_proper_nouns"] = number_of_proper_nouns
        pos_tagged_review["number_of_other_nouns"] = number_of_other_nouns
        pos_tagged_review["number_of_pronouns"] = number_of_pronouns
        pos_tagged_review["number_of_conjunction"] = number_of_conjunction
        pos_tagged_review["number_of_present_verb"] = number_of_present_verb
        pos_tagged_review["number_of_past_verb"] = number_of_past_verb
        pos_tagged_review["number_of_participle"] = number_of_participle
        pos_tagged_review["number_of_adjective"] = number_of_adjective
        pos_tagged_review["number_of_interjection"] = number_of_interjection

        self.review = tagged_text
        return {
            "tagged_text": tagged_text,
            "text_assertion": pos_tagged_review
        }

    @property
    def analyser(self):
        return self.review


if __name__ == '__main__':
    text = "Once again Mr. Costner has dragged out a movie for far longer than necessary. Aside from the terrific sea rescue sequences, of which there are very few I just did not care about any of the characters. Most of us have ghosts in the closet, and Costner's character are realized early on, and then forgotten until much later, by which time I did not care. The character we should really care about is a very cocky, overconfident Ashton Kutcher. The problem is he comes off as kid who thinks he's better than anyone else around him and shows no signs of a cluttered closet. His only obstacle appears to be winning over Costner. Finally when we are well past the half way point of this stinker, Costner tells us all about Kutcher's ghosts. We are told why Kutcher is driven to be the best with no prior inkling or foreshadowing. No magic here, it was all I could do to keep from turning it off an hour in."
    visualize_obj = visualize(text)
    result = visualize_obj.process()
    print(json.dumps(result))
