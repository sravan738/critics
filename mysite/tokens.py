import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Utilities:
    ones = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine"
    }
    tens = {
        1: "ten",
        2: "twenty",
        3: "thirty",
        4: "forty",
        5: "fifty",
        6: "sixity",
        7: "seventy",
        8: "eighty",
        9: "ninty"
    }
    hundred = "hundred"
    thousand = "thousand"

    numbers = {
        0: "ones",
        1: "tens",
        2: "hundred",
        3: "thousand",
        4: "thousand",
        5: "lakhs",
        6: "lakhs"
    }

    def convert_int_to_text(self, text):
        # 100 -> one hundred , 456 -> four hundred fifty six
        # Doesn't display zero
        # 456 -> list(text) -> [4,5,6] -> [-1::-1] -> [6,5,4] -> [(0,6),(1,5),(2,4)]
        # 400 -> list(text) -> [4, 0, 0] -> [-1::-1] -> [0, 0, 4] -> [(0, 0), (1, 0), (2, 4)]

        return_text = []
        for i, num in enumerate(list(text)[::-1]):
            if not int(num) == 0:
                if i in [2, 3, 5]:
                    return_text.insert(0, self.numbers[i])
                    return_text.insert(0, self.ones.get(int(num)))
                elif i in [4, 6]:
                    return_text.insert(0, self.numbers[i])
                    return_text.insert(0, self.tens.get(int(num)))
                else:
                    return_text.insert(0, getattr(self, self.numbers[i]).get(int(num)))
        return " ".join(return_text)

    @classmethod
    def negation(cls, input_text):
        # input text is of form List[String]
        negation_text = []
        for word in input_text:
            if word.endswith("n't"):
                negation_text.extend([word[:-3], "not"])
            else:
                negation_text.append(word)
        return negation_text

    @staticmethod
    def isheader(text):
        try:
            if text.index(" "):
                return True
            else:
                return False
        except Exception as e:
            return False


def casing_the_characters(input_text):
    return_text = []
    for text in input_text:
        try:
            if text.isnumeric():
                return_text.append(Utilities().convert_int_to_text(text))
            else:
                return_text.append(text)
        except Exception as e:
            pass
    return return_text


columns_to_take = ["review"]
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def csv_wrapper(func):
    def csv_inner_function(*args, **kwargs):
        # Reading from file
        input_data = args[0]
        # with open('/Users/sravan/pycharmprojects/kumar.csv', 'r') as f:
        #     csv_reader = csv.reader(f)
        #     input_data.extend([line for line in csv_reader])

        # modifications
        index_to_capture = next(
            iter([list_index for list_index, value in enumerate(input_data[0]) if value in columns_to_take]), None)
        input_data = [rows[index_to_capture] for rows in input_data]
        kwargs["input_data"] = input_data[1:]

        inner_result, positive, negative = func(*args, **kwargs)

        # Writing to file
        with open('/Users/sravan/pycharmprojects/new_srav.csv', 'w')as new_file:
            csv_writer = csv.writer(new_file)
            inner_result = [["review", "label"]] + inner_result
            for line in inner_result:
                csv_writer.writerow(line)
        return {"positive": positive, "negative": negative, "result":inner_result}

    return csv_inner_function


def semantic_analyser(input_text):
    sia = SentimentIntensityAnalyzer()
    score_map = sia.polarity_scores(input_text)
    if score_map["pos"] > score_map["neg"]:
        return [input_text, "positive"]
    else:
        return [input_text, "negative"]

    # d = {"neg": 0.0, "neu": 0.661, "compound": 0.6249, "pos": 0.339}
    # for semantic, value in score_map.items():
    #     if value == max(score_map.values()):
    #          return [input_text, semantic]
    # return [input_text, "neu"]


@csv_wrapper
def normalization(*args, **kwargs):
    input_data= kwargs["input_data"]
    outer_result = []
    positive, negative = (0, 0)
    print(input_data)
    for line in input_data:
        # Tokenisation
        step1 = line.lower().split(" ") if Utilities.isheader(line) else [line.lower()]

        # Removing stop words
        step2 = [text for text in step1 if text not in stop_words]

        # formating_data = map(lambda x: ", ".join([text for text in x.lower().split(" ") if text not in stop_words]), line)

        # Character casing
        step3 = casing_the_characters(step2)

        # Negation
        step4 = Utilities.negation(step3)

        # Combine data
        step5 = " ".join(step4)
        step6 = semantic_analyser(step5)
        if step6[1] == "positive":
            positive = positive + 1
        else:
            negative = negative + 1

        outer_result.append(step6)
    return (outer_result, positive, negative)

if __name__ == '__main__':
    result = normalization()
    print(result)
