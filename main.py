from flask import Flask, request
from flask_restful import Api, Resource
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from rapidfuzz import process, fuzz

df1 = pickle.load(open('movie_recommendation.pkl','rb'))
app = Flask(__name__)
api = Api(app)

cm = CountVectorizer().fit_transform(df1['important_feature'])
cs = cosine_similarity(cm)

movie_titles = []
def get_movie_recommendation(title):
    most_similar = process.extractOne(title, df1['title'], scorer=fuzz.WRatio)
    print(most_similar)
    movie_id = df1[df1.title == most_similar[0]]['id'].values[0]
    scores = list(enumerate(cs[movie_id]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # print(most_similar[1])
    if (most_similar[1] == 100.0):
        sorted_scores = sorted_scores[1:]
    # sorted_scores = sorted_scores[1:]
    j = 0
    print('The 7 most recommended Movie/Tv show to watch:')
    for item in sorted_scores:
        movie_title = df1[df1.id == item[0]]['title'].values[0]
        movie_titles.append(movie_title)
        types = df1[df1.id == item[0]]['type'].values[0]
        id = item[0]
        print(j + 1, movie_title + '\t' + types + '\t' + str(id))
        j = j + 1
        if j > 6:
            break

class Users(Resource):
    def get(self):
        data = df1.to_dict('records')
        return {'data': data}, 200
    def post(self):
        name = request.form['name']
        print('data from the client:', name);

        get_movie_recommendation(name)
        return {'data': movie_titles}, 201

api.add_resource(Users, '/users')

# @app.route('/users',methods=['POST'])
# def movie_recommendated():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         print('data from the client:', name);
#
#         get_movie_recommendation(name)
#         return {'data': movie_titles}, 201


if __name__ == '__main__':
    app.run(debug=True)
