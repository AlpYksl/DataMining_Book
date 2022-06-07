import math
from flask import Flask,render_template,request
import pickle
import numpy as np


popularity_df = pickle.load(open('popularity.pkl','rb'))
final = pickle.load(open('final.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similar_scores = pickle.load(open('similar_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html',
                           book_name = list(popularity_df['Book-Title'].values),
                           author=list(popularity_df['Book-Author'].values),
                           image=list(popularity_df['Image-URL-M'].values),
                           votes=list(popularity_df['number_ratings'].values),
                           rating=list(np.round(popularity_df['average_rating'].values,2))
                           )

@app.route('/predict')
def recommend_ui():
    return render_template('predict.html')

@app.route('/predict_books',methods=['post'])
def recommend():
    data = []
    user_input = request.form.get('user_input')
    array = np.where(final.index == user_input)
    print(array)
    if array[0] != None:
        similar_items = sorted(list(enumerate(similar_scores[array[0][0]])), key=lambda x: x[1], reverse=True)[1:10]
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == final.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            data.append(item)

    return render_template('predict.html',books=data)

if __name__ == '__main__':
    app.run(debug=True)