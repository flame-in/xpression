
# xPression - Twitter Data Mining and Sentiment Analysis

Final year project at CETKR created using Python and Django.  
Uses pretrained roBERTa model (torch) to predict sentiment labels from tweet text : positive, negative and neutral.  
Data mining procedure makes use of Twitter API -> Tweepy.  
MongoDB + PyMongo to store and retrieve collected tweet data and processed sentiment data.  

HTML/CSS/JS + Chart.js + AnyChart for UI, graphs and wordcloud.

## Installation

Use the given requirements.txt to install prerequisites. 

```bash
pip install requirements.txt
```

## Usage
1) Download the pytorch_model.bin from Huggingface -> [roBERTa-base model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)   
2) Place the file in twitter-roberta-base-sentiment folder
3) Set path to the roBERTa model in main.py  
4) Set up and connect to MongoDB local / cloud in dbcode.py  

In root folder :
```python
python manage.py runserver
```
Django admin can be used to access SQLite user data.

Super user -> Username: admin, Password: admin


## License
[MIT](https://choosealicense.com/licenses/mit/)

### Credits
@esclate  
@dj  
@indu
