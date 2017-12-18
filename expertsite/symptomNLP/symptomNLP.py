from keras.models import load_model
from keras.preprocessing import sequence
import jieba_tw
import pickle

class STNLP:
    def __init__(self, model_path, token_path, predict_symptom_dict):
        self.model_path = model_path
        self.token_path = token_path
        self.predict_symptom_dict = predict_symptom_dict
        
    def load_train_model(self):
        model = load_model(self.model_path)
        print('load model complete')
        return model

    def load_train_token(self):
        with open(self.token_path, 'rb') as handle:
            token = pickle.load(handle)
        print('load token complete') 
        return token

    def window_cut(self, sentence):
    
        if len(sentence)<=5:
            seg_sen = jieba_tw.cut(sentence, cut_all=False)
            seg_sen_list = []
            seg_sen_list.append(' '.join(seg_sen).rstrip('\n'))
            return seg_sen_list
    
        else:
            count = 0
            win_start = 0
            win_end = 5
            step_move = 2
            window_list = []
        
            while( win_end <= len(sentence) ):
                win_start = 0
                win_end = 5
    
                win_start = win_start + step_move*count
                win_end = win_end + step_move*count
    
                window_sentence = sentence[win_start:win_end]
    
                window_list.append( window_sentence )
    
                count = count +1
        
            return window_list

    
    def predict(self, token, model, sentence):
        
        window_list = self.window_cut(sentence)
        
        win_predict = []
    
        for sen in window_list:
            query = sen
            seg_query = jieba_tw.cut(query, cut_all=False)
            query_line = []
            query_line.append(' '.join(seg_query).rstrip('\n'))

            input_seq = token.texts_to_sequences(query_line) # 轉成數字list

            pad_input_seq = sequence.pad_sequences(input_seq, maxlen=4) # 長度轉為4

            predict = model.predict_classes(pad_input_seq)
            predict_soft = model.predict(pad_input_seq) # 機率分布
    
            # 如果沒超過某個機率不能列入 0.7, 0.8, 0.9
            if max(predict_soft[0])<0.8:
                pass
            else:
                win_predict.append( self.predict_symptom_dict[ predict[0] ] )
        
        win_predict = list(set(win_predict)) # 把重複的symptom刪除
    
        return win_predict