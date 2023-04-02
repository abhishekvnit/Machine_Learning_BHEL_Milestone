import numpy as np
from flask import Flask, request, jsonify, render_template, send_file, Response
import pickle
import math
import pandas as pd
import seaborn as sns
import io
import base64
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvass
# import base64
# fig,ax= plt.subplots(figsize=(6,6))
# ax= sns.set_style(style='darkgrid')
app = Flask(__name__)
model = pickle.load(open('BHEL_Milestone_predicter.pkl','rb'))
model2 = pickle.load(open('BHEL_Milestone_predicter_BESAct.pkl','rb'))

data= pd.read_excel('Milestones.xlsx')
@app.route('/')
def home():
    # img = io.BytesIO()
          
    # sns.catplot(y = "BES_Sch_Duration", x = "MW", data = data.sort_values("BES_Sch_Duration", ascending = False), kind="boxen", height = 3, aspect = 3)
    # plt.savefig(img, format='png')

    # img.seek(0)

    
    # plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('index.html')   
     

    
@app.route('/predict', methods=['POST'])
def predict():
    # Storing all form input to array
    int_features  = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0],2)
    img = io.BytesIO()
    sns.catplot(y = "BES_Sch_Duration", x = "MW", data = data.sort_values("BES_Sch_Duration", ascending = False), kind="boxen", height = 3, aspect = 3)

    plt.savefig(img, format='png')

    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('index.html',prediction_text="Predicted BES days from Zero date {}".format(math.floor(output)),plot_url=plot_url)

@app.route('/predict2', methods=['POST'])
def predict2():
    int_features  = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model2.predict(final_features)
    output = round(prediction[0],2)
    img = io.BytesIO()
    sns.catplot(y = "BES_Act_Duration", x = "MW", data = data.sort_values("BES_Act_Duration", ascending = False), kind="boxen", height = 3, aspect = 3)
    plt.savefig(img, format='png')

    img.seek(0)

    plot_url1 = base64.b64encode(img.getvalue()).decode()
    return render_template('index.html',prediction_text2="Predicted BES actual days from Zero date {}".format(math.floor(output)),plot_url1=plot_url1)




if __name__ == '__main__':
    app.run(debug= True)