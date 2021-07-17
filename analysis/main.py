"""
directory that store the file pytorch_model.bin is important
path is that directory. Other mdels can also be used almost in the same way.
labels are downloaded in originals script. But i just made it into a list of three elements. 
"""

from analysis.data_retrieve import data_retrieve_caller_sentiment
from analysis.dbcode import insert_sentiment_data
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from scipy.special import softmax
import pandas as pd


def summary_out_db(text, encoded_input, output, scores, ranking):
	pass

def preprocess(text):
    new_text = []

    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)




def sentiment_analysis(keyword):
	path ="xpression_project\\models\\twitter-roberta-base-sentiment"
	labels=['negative', 'neutral', 'positive']
	count = 0
	
	tokenizer = AutoTokenizer.from_pretrained(path)
	model = AutoModelForSequenceClassification.from_pretrained(path)
	start_date = ""
	end_date = ""
	batch = data_retrieve_caller_sentiment(start_date, end_date, keyword)
	total_msg = len(batch)
	out_list = []
	for tweet in batch:
		count=count+1
		print(count ,"-message is>>>",tweet["data"]["text"],"\n.........................")
		text=tweet["data"]["text"]
		if(text == ""):
			print("null tweet......................")
		else:
			cleaned_text = preprocess(text)
			encoded_input = tokenizer(cleaned_text, return_tensors='pt')
			output = model(**encoded_input)
			scores = output[0][0].detach().numpy()
			scores = softmax(scores)

			
			v = {
        			"_id": tweet["_id"],
        			"sentiment_data":
            			{
                			"cleaned_text": cleaned_text,
                			"scores": {
                						'negative':str(scores[0]),
                						'neutral':str(scores[1]),
                						'positive':str(scores[2])
                					}
            			}
    			}
			status = insert_sentiment_data(v)
			print(status)

	return 0
# key = input(">>>>>")
# sentiment_analysis(key)

