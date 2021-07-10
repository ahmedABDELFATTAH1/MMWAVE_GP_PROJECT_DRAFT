from numpy import negative
from radar_configuration import *


g_model = None
def modele_naive(X_data_train,Y_data_train,X_data_val,Y_data__val,file_name):
    global g_model
    '''
    :param X_data_train:
    :param Y_data_train:
    :param X_data_val:
    :param Y_data__val:
    :return: the trained model
    '''
    if os.path.isfile(file_name):
        model = models.load_model(file_name)
        g_model = model
        return
    shape_input=X_data_train.shape[1]
    model = keras.Sequential()
    model.add(layers.Dense(32,input_dim=shape_input,activation='relu'))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_data_train, Y_data_train, epochs=200, batch_size=32, validation_data=(X_data_val, Y_data__val))
    model.save(file_name)
    g_model=model
    return

    


def get_reading_message(): 
    context = zmq.Context()
    consumer_receiver = context.socket(zmq.SUB)
    consumer_receiver.RCVTIMEO = 1000
    consumer_receiver.setsockopt_string(zmq.SUBSCRIBE, "")    
    consumer_receiver.connect("tcp://127.0.0.1:5558")
    frame = None
    try:
        frame = consumer_receiver.recv_json()   
    except:
        pass
    # print(frame)
    consumer_receiver.close() 
    return frame["FRAME"]


def save_data(x,name):
    """
    saves the x , y , z points of an experiment in an external file

    input: x --> x axis points 
           y --> y axis points
           z --> z axis points
           name --> name of the experiment

    """
    #saves x points in "3D_experements" folder with name of "experiment_name+_x.txt"
    file = open(name+"_x.txt", "a")
    np.savetxt(file, x)
    file.close()

def collect_data(name):
    frames_data = []
    frame = None
    count =0
    for i in range(2000):
        try:
            frame = get_reading_message()
            frames_data.append(frame)
            count +=1
            print(count)
        except:
            print(frame)
    save_data(np.array(frames_data),name)

def load_data(name):
    numbers = np.loadtxt(name+"_x.txt")
    print(numbers)
    return numbers


def format_data(positives,negatives,split_per):
        '''
        :param positives: posivies class data
        :param negatives:  negative class data
        :return: X as training data and Y as labels
        takes the positives
        takes the negatives
        add last value as 1 (true) or 0 (false)
        convert them to a numpy arrays
        shuffle them togather
        return X as data[0:-1] and Y as data[-1]
        '''
        for i in range(len(positives)):
            positives[i].append(1)

        for i in range(len(negatives)):
            negatives[i].append(0)

        data_positives = np.array(positives)
        data_negatives = np.array(negatives)

        data = np.concatenate((data_positives,data_negatives),axis=0)

        np.random.shuffle(data)
        train_len=int(data.shape[0]*split_per)
        return data[0:train_len,0:-1],data[0:train_len,-1],data[train_len:,0:-1],data[train_len:,-1]

def make_prediction(reading):
        result = g_model.predict(np.reshape(reading,(1,len(reading))))>.8
        return result[0][0]

if __name__=="__main__":
    collect_data("face")
    collect_data("body")
    positives = load_data("face")
    negatives = load_data("body")
    x_train,y_train,x_test,y_test = format_data(positives.tolist(),negatives.tolist(),.8)
    file_name = "face_model.h5"
    modele_naive(x_train,y_train,x_test,y_test,file_name)    
    # modele_naive(0,0,0,0)
    # frame = get_reading_message()
    # print(make_prediction(frame))
