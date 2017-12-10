# version 1.6
# engine

import json
import codecs
import re

class engine(object):
    def __init__(self, database_path):
        self.database_path = database_path
        
    def read_database(self):
        with codecs.open(self.database_path, 'r', 'utf-8') as f:
            database = json.load(f)
            return database
        
    def list_database(self):
        database = self.read_database()
        
        for db in database:
            print(db)
        
    def list_database_feacture(self):
        database = self.read_database()
        
        list_feacture = []
        for db in database:
            for sym in db['feacture']:
                list_feacture.append(sym)
                
        list_feacture = {}.fromkeys(list_feacture).keys()
        
        for li_fea in list_feacture:
            print(li_fea, end=', ')
        
    def set_data(self, label, feacture):
        # feacture為list
        re_feacture = re.split(r"：|。|！|；|、|;|,|\?\s|;\s|,\s", feacture.replace(' ', '')) 
        item = {'label': label, 'feacture':re_feacture}
        return item
        
    def get_differ(self, predict, feacture):
        database = self.read_database()
        re_feacture = re.split(r"：|。|！|；|、|;|,|\?\s|;\s|,\s", feacture.replace(' ', ''))
        
        comparison_feacture = []
        
        # search predict label's feacture
        for label in predict:
            for db in database:
                if label==db['label']:
                    comparison_feacture.append(db['feacture'])
        
        # remove previous same feacture
        for item in comparison_feacture:
            for fea in re_feacture:
                try:
                    item.remove(fea)
                except:
                    print('無需刪除項目')
                    pass
            
        return comparison_feacture
    
    def re_callback(self, predict, feacture):
        comparison_feacture = self.get_differ(predict, feacture)
        
        for i, label in enumerate(predict):
            for j, fea in enumerate(comparison_feacture[i]):
                print('請問您有', fea, '的feacture嗎？ (Yes/No)')
                boolean_feacture = input('feacture：')
                if boolean_feacture=='Yes':
                    print('推薦給您', label)
                    break
                elif i==len(predict)-1 and j==len(comparison_feacture[i])-1 and boolean_feacture=='No':
                    print('推薦給您', predict)
                elif boolean_feacture=='No':
                    continue
            else: continue
            break
            
    def run(self):
        identify = input('請問您的身份是(user/admin)：')
    
        if(identify == 'user'):
            p = user(self.database_path)
        
            p.list_database_feacture()
            feacture = input('請問您的feacture是：')
        
            predict = p.match(feacture)
        
            if( predict==[] ):
                print('沒有這種label呦')
            elif( len(predict)==1 ):
                print('您可能需要', predict)
            else:
                p.re_callback(predict, feacture)
              
        elif(identify == 'admin'):
            d = admin(self.database_path)
        
            intent = input('請問要新增label(0), 還是刪除label(1)：')
        
            if int(intent)==0:
                label = input('請問要新增的label是：')
                feacture = input('適用feacture為：')
                d.add_knowledge(label, feacture)
            elif int(intent)==1:
                label = input('請問要刪除的label名稱是：')
                d.del_knowledge(label)
                
                
class admin(engine):
    def add_knowledge(self, label, feacture):
        database = super().read_database()
        item = super().set_data(label, feacture)
        database.append(item)
        
        try:
            with codecs.open(self.database_path, 'w') as f:
                json.dump(database, f, ensure_ascii=False)
                
            print('成功新增', label, 'Label')
        except e:
            print('寫入失敗', e)
            
    def del_knowledge(self, label):
        database = super().read_database()
        
        re_label = list( re.split(r"：|。|！|；|、|;|,|\?\s|;\s|,\s", label.replace(' ', '')) )
        
        count = 0
        for lab in re_label:
            for i, db in enumerate(database):
                if lab==db['label']:
                    try:
                        database.pop(i)
                        count = count+1
                        print('成功刪除', lab)
                    except e:
                        print('刪除', lab, '錯誤', e)
        try:
            with codecs.open(self.database_path, 'w') as f:
                json.dump(database, f, ensure_ascii=False)
        except e:
            print('寫入失敗', e)

        if count>0:
            print('共刪除', count, '項label')
        elif count==0:
            print('資料庫內沒有你要刪除的label！')

            
class user(engine):
    def match(self, feacture):
        predict = []
        database = super().read_database()
        re_feacture = list( re.split(r"：|。|！|；|、|;|,|\?\s|;\s|,\s", feacture.replace(' ', '')) )
        
        for re_sym in re_feacture:
            for db in database:
                if set(re_feacture).issubset(set(db['feacture'])) and len(re_feacture)>1:
                    predict.append(db['label'])
                    break;
                elif re_sym in db['feacture']:
                    predict.append(db['label'])
        
        predict = list(set(predict))
        
        return predict