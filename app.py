from flask import Flask, render_template, url_for, request
import pickle
import responses, functions
import numpy as np

# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True

app = Flask(__name__)

# loading the model from pickle
virtual_agent_model = pickle.load(open('covid19_virtual_agent.pickle','rb'))
#loading the vectorizer from pickle
vectorizer = pickle.load(open('cv_vector.pickle','rb'))

@app.route('/', methods=['POST', 'GET'])
def home():

    content = {'question':'','confidence':'','response_title':'','response_content':''}
    content['infected_count'] = functions.getInfectedCount()
    content['recovered_count'] = functions.getCuredCount()
    content['death_count'] = functions.getDeathCount()
    content['mortality_rate'] = functions.getMortalityRate()
    content['recovery_rate'] = functions.getRecoveryRate()


    if request.method == 'POST':
        question = request.form['question']  #get question from form

        print(question)
        content['question'] = question
        question = functions.check(question)
        print('corrected question: ' + question)
        qtn = vectorizer.transform([question])  #transform to a vector
        qtn = qtn.toarray()  #transform to array
        prediction = virtual_agent_model.predict(qtn)
        print("confidence: " + str(np.amax(prediction[0])))
        content['confidence'] = str(np.amax(prediction[0]))
        print(responses.class_names[np.argmax(prediction[0])])
        content['response_title'] = responses.class_names[np.argmax(prediction[0])]
        content['response_content'] = responses.class_responses[np.argmax(prediction[0])]

    return render_template('index.html', content=content)


if __name__ == '__main__':
    app.run(debug=False, threaded=False)