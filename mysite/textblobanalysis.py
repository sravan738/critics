from textblob import TextBlob


class mycomment:

    def __init__(self, comm):
        self.text = comm

    def showRating(self):
        print("Enter some comments:")

        blob = TextBlob(str(self.text))
        blob.tags  # [('The', 'DT'), ('titular', 'JJ'),
        #  ('threat', 'NN'), ('of', 'IN'), ...]

        blob.noun_phrases  # WordList(['titular threat', 'blob',
        #            'ultimate movie monster',
        #            'amoeba-like mass', ...])
        x = 0;
        y = 0
        for sentence in blob.sentences:
            print(sentence.sentiment.polarity)
            x = x + sentence.sentiment.polarity;
            y = y + 1
        # 0.060
        # -0.341
        result = (x / y)
        print("result = ", result)

        blob.translate(to="es")  # 'La amenaza titular de The Blob...'
        return result
