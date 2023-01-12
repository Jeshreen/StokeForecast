from project.data_models import FormData
import pickle
import pandas as pd
import numpy as np
from numpy import dstack
from sklearn.preprocessing import MinMaxScaler

def process_entity(entity: FormData):
    print("process_entity - start")
    model = call_model(entity)
    val = get_prediction(model,entity.daterange)
    print("predictions")
    print(val)
    print("process_entity - end")


def call_model(entity: FormData):
    ''' if you want to read from csv '''
    model = pickle.load(open('/Users/balraj/Documents/MSC/Project/SourceCode/stockforecast/skeleton_python_flask/finalModel_fold1.dat',"rb"))
    return model
    

def data_splitA():
    dataframe = pd.read_csv('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/Data.csv')

    input_features = list(dataframe)[2:12]

    sample_input = dataframe[input_features]

    return sample_input

def data_splitB():
    dataframe = pd.read_csv('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/Data.csv')

    input_features = list(dataframe)[3:12]

    sample_input = dataframe[input_features]

    return sample_input

def stacked_predictionASPI(data):
    all_models = list()

    # load model
    #model1 = load_model('model1.h5',custom_objects=dependencies)
    #all_models.append(model1)
    #model2 = load_model('model2.h5',custom_objects=dependencies)
    #all_models.append(model2)
    model3 = pickle.load(open('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/lgb_fold1.dat',"rb"))
    all_models.append(model3)
    model4 = pickle.load(open('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/xgb_fold1.dat',"rb"))
    all_models.append(model4)

    stackX = None

    for model in all_models:
        predictions = model.predict(data)
        yhat = predictions.reshape(predictions.shape[0],1)
		# stack predictions into [rows, members, probabilities]
        if stackX is None:		
            stackX = yhat #
        else:
            stackX = dstack((stackX, yhat))
	 
	# flatten predictions to [rows, members x probabilities]
    stackX = stackX.reshape((stackX.shape[0], stackX.shape[1]*stackX.shape[2]))

    model = pickle.load(open('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/finalModel_fold1.dat',"rb"))
    forecast = model.predict(stackX)

    return forecast

def stacked_predictionSP(data):
    all_models = list()

    # load model
    #model1 = load_model('model1.h5',custom_objects=dependencies)
    #all_models.append(model1)
    #model2 = load_model('model2.h5',custom_objects=dependencies)
    #all_models.append(model2)
    model3 = pickle.load(open('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/lgbS_fold1.dat',"rb"))
    all_models.append(model3)
    model4 = pickle.load(open('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/xgbS_fold1.dat',"rb"))
    all_models.append(model4)

    stackX = None

    for model in all_models:
        predictions = model.predict(data)
        yhat = predictions.reshape(predictions.shape[0],1)
		# stack predictions into [rows, members, probabilities]
        if stackX is None:		
            stackX = yhat #
        else:
            stackX = dstack((stackX, yhat))
	 
	# flatten predictions to [rows, members x probabilities]
    stackX = stackX.reshape((stackX.shape[0], stackX.shape[1]*stackX.shape[2]))

    model = pickle.load(open('/Users/balraj/Documents/MSC/Project/SourceCode/skeleton_python_flask1/skeleton_python_flask/finalModelS_fold1.dat',"rb"))
    forecast = model.predict(stackX)

    return forecast

def get_prediction(date_range: FormData):
    dataA = data_splitA()
    dataS = data_splitB()

    stock_dates = pd.to_datetime(dataA['Date'])

    forecast_days = 30
    forecast_dates = pd.date_range(list(stock_dates)[-1], periods=forecast_days, freq='1d').tolist()

    forecastA = stacked_predictionASPI(dataA[-forecast_days:])
    forecastB = stacked_predictionSP(dataS[-forecast_days:])

    forecast_graph_dates = []
    for time_i in forecast_dates:
        forecast_graph_dates.append(time_i.date())

    df_forecast = pd.DataFrame({'Date':np.array(forecast_graph_dates), 'ASPI':forecastA, 'S&PSL20':forecastB})
    df_forecast['Date']=pd.to_datetime(df_forecast['Date'])

    return df_forecast