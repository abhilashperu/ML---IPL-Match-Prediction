import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        
        team1 = request.form['team1']
        team2 = request.form['team2']
        toss_winner = request.form['toss_winner']
        venue = request.form['venue']
        toss_decision = int(request.form['toss_decision'])
        
        
        team_encodings = {
    'Mumbai Indians': 1,
    'Kolkata Knight Riders': 2,
    'Royal Challengers Bangalore': 3,
    'Deccan Chargers': 4,
    'Chennai Super Kings': 5,    
    'Rajasthan Royals': 6,
    'Delhi Daredevils': 7,
    'Gujarat Lions': 8,
    'Kings XI Punjab': 9,
    'Sunrisers Hyderabad': 10,
    'Rising Pune Supergiants': 11,
    'Kochi Tuskers Kerala':12,
    'Pune Warriors': 13,
    'Delhi Capitals': 14,
    'Draw': 15
}
        team_encode_dict = {'team1': team_encodings,
                    'team2': team_encodings,
                    'toss_winner': team_encodings,
                    'winner': team_encodings
                    }
        venue_encodings = {'Barabati Stadium':1,
 'Brabourne Stadium':2,
 'Buffalo Park':3,
 'De Beers Diamond Oval':4,
 'Dr DY Patil Sports Academy':5,
 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium':6,
 'Dubai International Cricket Stadium':7,
 'Eden Gardens':8, 
 'Feroz Shah Kotla Ground':9,
 'Green Park':10,
 'Himachal Pradesh Cricket Association Stadium':11,
 'Holkar Cricket Stadium':12,
 'IS Bindra Stadium':13,
 'JSCA International Stadium Complex':14, 
 'Kingsmead':15,
 'M Chinnaswamy Stadium':16,
 'MA Chidambaram Stadium, Chepauk':17,
 'Maharashtra Cricket Association Stadium':18,
 'Nehru Stadium':19,
 'New Wanderers Stadium':20,
 'Newlands':21,
 'OUTsurance Oval':22,
 'Punjab Cricket Association Stadium, Mohali':23,
 'Rajiv Gandhi International Stadium, Uppal':24,
 'Sardar Patel Stadium, Motera':25, 
 'Saurashtra Cricket Association Stadium':26,
 'Sawai Mansingh Stadium':27,
 'Shaheed Veer Narayan Singh International Stadium':28,
 'Sharjah Cricket Stadium':29,
 'Sheikh Zayed Stadium':30,
 "St George's Park":31,
 'Subrata Roy Sahara Stadium':32,
 'SuperSport Park':33,
 'Vidarbha Cricket Association Stadium, Jamtha':34,
 'Wankhede Stadium':35}
        
        
        inp = [team_encode_dict['team1'][team1],team_encode_dict['team2'][team2],team_encode_dict['toss_winner'][toss_winner],venue_encodings[venue],toss_decision]
        inp = np.array(inp).reshape((1, -1))
        prediction = model.predict(inp)
                
        output = list(team_encodings.keys())[list(team_encode_dict['winner'].values()).index(prediction)]
        #if prediction
        if team1 == team2:
            return render_template('index.html', prediction_text="Are you kidding me!!")
        elif toss_winner != team1 and toss_winner != team2:
            return render_template('index.html', prediction_text="Dude! Enough of making fun!!")
        elif output != team2 and output != team1:
           return render_template('index.html', prediction_text="Cannot Predict the winner")
        elif toss_decision != 0 and toss_decision != 1:
           return render_template('index.html', prediction_text="There is only Batting and Fielding")
        else:
            return render_template('index.html', prediction_text="The Winner would be:" + output)
        
    #return render_template('index.html', prediction_text="The Winner would be:" + output)


if __name__ == "__main__":
    app.run(debug=True)