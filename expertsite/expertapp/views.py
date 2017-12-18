from django.shortcuts import render
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from expertEngine import herbologySystem as hs
import os
import json
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from expertsite.settings import PROJECT_ROOT
import jieba_tw
from symptomNLP import symptomNLP

# 載入 STNLP
model_path = os.path.join(PROJECT_ROOT, 'train_models/1218_1064_model.h5')
token_path = os.path.join(PROJECT_ROOT, 'train_models/1218_1064_token.pickle')
predict_symptom_dict = {0: '火大', 1: '咳嗽', 2: '高血壓', 3: '胃潰瘍', 4: '痰', 5: '風濕', 6: '筋骨痛',
                        7: '胃痛', 8: '腎臟病', 9: '發炎', 10: '腸胃不順', 11: '水腫', 12: '糖尿病',
                        13: '肝炎', 14: '中暑'}

stnlp = symptomNLP.STNLP(model_path, token_path, predict_symptom_dict)
model = stnlp.load_train_model()
token = stnlp.load_train_token()

# prerun model
STNLP_prerun = stnlp.predict(token, model, '預運行模組')


def index(request):
    return render(request, 'index.html')

def user(request):
    return render(request, 'user.html')

def admin(request):
    return render(request, 'admin.html')

@csrf_exempt
def list_database_ajax(request):

    path = os.path.join(PROJECT_ROOT, 'knowledgeBase.json')
    es = hs.expertSystem(path)

    if request.is_ajax():
        database = es.read_database()

        med_list = []
        sym_list = []
        for db in database:
            med_list.append(db['medicine'])
            sym_list.append(db['symptom'])

        back = {'med_list': med_list,
                'sym_list': sym_list}

    return JsonResponse(back)



@csrf_exempt
def user_symptom_ajax(request):

    path = os.path.join(PROJECT_ROOT, 'knowledgeBase.json')
    p = hs.person(path)

    if request.is_ajax():
        post = request.POST
        user_symptom = post.get('user_symptom')

        # STNLP
        STNLP_predict = stnlp.predict(token, model, user_symptom)

        predict = p.match(STNLP_predict)

        if predict==[]:
            back = {'predict_sym': STNLP_predict,
                    'predict': 'none'}

            return JsonResponse(back)

        elif len(predict)==1:
            back= {'predict_sym': STNLP_predict,
                   'predict': predict }

            return JsonResponse(back)

        else:
            comparison_symptom = p.get_differ(predict, STNLP_predict)
            back = {'predict_sym': STNLP_predict,
                    'predict': predict,
                    'comparison_symptom': comparison_symptom }

            return JsonResponse(back)
            # return render(request, 'user.html', back)

        # back = {'predict': predict }



@csrf_exempt
def admin_add_ajax(request):

    path = os.path.join(PROJECT_ROOT, 'knowledgeBase.json')
    d = hs.doctor(path)

    if request.is_ajax():
        post = request.POST
        medicine = post.get('add_medicine_name')
        symptom = post.get('add_medicine_symptom')

        try:
            d.add_knowledge(medicine, symptom)
            back = {'medicine': medicine,
                    'status': 'success'}
        except:
            back = {'status': 'error'}

    return JsonResponse(back)

@csrf_exempt
def admin_del_ajax(request):

    path = os.path.join(PROJECT_ROOT, 'knowledgeBase.json')
    d = hs.doctor(path)

    if request.is_ajax():
        post = request.POST
        medicine = post.get('del_medicine_name')

        try:
            del_count = d.del_knowledge(medicine)

            if( del_count > 0):
                back = {'medicine': medicine,
                        'status': 'success'}
            elif( del_count == 0 ):
                back = {'medicine': medicine,
                        'status': 'error'}
        except:
            back = {'status': 'error'}

    return JsonResponse(back)