from pandas.core.indexes.interval import le
import speech_recognition as sr
from numpy import less_equal
from gtts import gTTS
import pandas as pd
import os


def parseSentencesIntoWords(ListOfSentences, shelterDataDF):

    splitSentences = []

    for sentence in ListOfSentences:

        listOfWords = sentence.split()
        print(listOfWords)
        splitSentences.append(listOfWords)

    matchWordsToKeywords(splitSentences, shelterDataDF)


def obtainKeywordList():

    keywords = ["shelter", "orange", "lee", "county"]

    return keywords


def convertSentencesToWavFiles(returnSentenceList):
    for i in range(0, len(returnSentenceList)):
        mytext = returnSentenceList[i]
        print(mytext)
        language = "en"
        myobj = gTTS(text=mytext, lang=language, slow=False)
        theFile = "response" + str(i) + ".mp3"
        myobj.save(theFile)


def matchWordsToKeywords(splitSentences, shelterDataDF):

    keywords = obtainKeywordList()

    returnSentenceList = []

    returnSentence = ""

    for sentence in splitSentences:

        for i in range(0, len(sentence)):

            if sentence[i] in keywords:

                if sentence[i] == "county":

                    countyName = sentence[i - 1].capitalize()
                    countyName = countyName + " County"
                    # print(countyName)
                    queryCounty = countyName
                    df = pd.DataFrame(shelterDataDF, columns=["county", "label"])
                    containsValues = df[df["county"].str.contains(queryCounty)]
                    # print(containsValues)

                    if len(df[df["county"] == queryCounty]["label"]) > 1:
                        answer = df[df["county"] == queryCounty]["label"].tolist()

                        answerLength = len(answer)
                        counter = 0
                        for item in answer:
                            counter += 1
                            if counter == answerLength:
                                returnSentence = returnSentence + item
                            else:
                                returnSentence = returnSentence + item + " and "

                        returnSentence = (
                            returnSentence.replace(".", "")
                            + " are the shelters in "
                            + countyName
                            + ". Please make your way to one of them carefully."
                        )
                    else:
                        answer = df[df["county"] == queryCounty]["label"].item()
                        returnSentence = returnSentence + answer
                        returnSentence = (
                            returnSentence
                            + " is the only shelter in "
                            + countyName
                            + ". Please make your way there carefully."
                        )

                    returnSentenceList.append(returnSentence)
                    returnSentence = ""
                    break
        else:

            returnSentence = "I'm sorry, I didn't understand that. Make sure to tell me what county you are in."

        if "shelter" not in sentence:

            returnSentence = "Sorry, I can only help you with shelters."

        returnSentenceList.append(returnSentence)

    print(returnSentenceList)
    convertSentencesToWavFiles(returnSentenceList)


def main():

    shelterDataDF = pd.read_csv("shelters.csv")

    speechFiles = []

    speechFiles.append("call0.wav")

    audioConvertedToTextFiles = []

    r = sr.Recognizer()

    for speechFile in speechFiles:

        with sr.AudioFile(speechFile) as source:

            audio_data = r.record(source)

            text = r.recognize_google(audio_data).lower()

            audioConvertedToTextFiles.append(text)

            print(text)

    parseSentencesIntoWords(audioConvertedToTextFiles, shelterDataDF)


if __name__ == "__main__":
    main()
