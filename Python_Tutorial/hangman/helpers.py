from data import *
import pickle
import os.path


def updateScoreFile(name, score):
    scores = {name: score}
    if os.path.exists(scoresFileName):
        with open(scoresFileName, "rb") as file:
            myPickler = pickle.Unpickler(file)
            scores = myPickler.load()
        if name in scores:
            scores[name] += score
        else:
            scores.update({name: score})
        with open(scoresFileName, "wb") as file:
            myPickler = pickle.Pickler(file)
            myPickler.dump(scores)
    else:
        with open(scoresFileName, "wb") as file:
            myPickler = pickle.Pickler(file)
            myPickler.dump(scores)
    print("Scores:")
    print(scores)
