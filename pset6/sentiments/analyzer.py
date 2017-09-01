import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positive = set()
        self.negative = set()
        file = open(positives, "r")
        for line in file:
            if not line.startswith(";"): 
                self.positive.add(line.strip())
        file.close()
        file = open(negatives, "r")
        for line in file:
            if not line.startswith((";" or "")): 
                self.negative.add(line.strip())
        file.close()


    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        score = 0
        for token in tokens:
            if token.lower() in self.positive:
                score = score + 1
            elif token.lower() in self.negative:
                score = score-1
        return score
