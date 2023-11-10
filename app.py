from flask import Flask, request, jsonify
import sys, json, requests

application = Flask(__name__)


@application.route("/", methods=["GET"])
def hello():
    return "hello"

@application.route("/webhook/", methods=["POST"])
def webhook():
    request_data = request.json
    print(request_data)
    call_back = requests.post(request_data['callback_url'], json={
        "version": "2.0", "template": { "outputs": [{
            "simpleText": {"text": request_data['result']['choices'][0]['message']['content']}
        }]}})
    print(call_back.status_code, call_back.json())
    return 'OK'
@application.route("/question", methods=["POST"])
def call_openai_api():
    user_request = request.json.get('userRequest', {})
    print("hihi", user_request)
    messages = []
    text = '''
     너는 지금부터 사람들의 문해력을 향상시키기 위해 글을 첨삭해줄거야. 
    
    [원문] 머신러닝은 주로 비교적 간단한 모델을 사용합니다. 선형 회귀, 결정 트리, 나이브 베이즈, 서포트 벡터 머신 등이 여기에 속합니다. 이러한 모델은 사전에 정의된 특징을 기반으로 학습하며, 복잡성이 낮습니다. 딥러닝 모델은 신경망을 기반으로 하며, 수십, 수백, 또는 수천만 개의 가중치와 매개변수를 가질 수 있습니다. 이로 인해 딥러닝 모델은 복잡하며 다양한 패턴을 학습할 수 있습니다. 이 모델은 여러 층으로 구성되어 복잡한 비선형 관계를 모델링할 수 있습니다. 머신러닝 모델은 데이터에서 특징을 수동으로 추출하거나 도메인 전문가의 지식을 활용하여 선택합니다. 이러한 특징 엔지니어링은 모델의 성능에 영향을 미칩니다. 딥러닝은 원시 데이터를 입력으로 사용하며, 모델 스스로 필요한 특징을 추출하고 학습합니다. 이는 자동 특징 추출로, 데이터의 다양한 표현을 학습하고 데이터 중심의 학습을 강조합니다. 머신러닝 모델은 상대적으로 적은 양의 데이터로 학습 가능하며, 
    일반적으로 적은 계산 리소스가 필요합니다.딥러닝: 딥러닝은 대규모 데이터셋과 높은 계산 리소스가 필요합니다. 대용량 그래픽 처리장치(GPU) 또는 텐서 처리장치(TPU)를 사용하여 학습을 가속화합니다.
    

[원문]의 글을 사용자 입력 [요약글]이 얼마나 잘 요약했는지 평가할거야.
    사용자의 [요약글] 이 들어오면 다음 글의 요약이 잘 되었는지 첨삭해줘. 

    [첨삭 기준]1. 핵심 어휘를 잘 파악하여 논점의 핵심을 담고 있는가?2. 중심 문장을 찾아 활용했는가? 3. 문맥에 따라 균형감 있게 내용을 요약했는가? 4. 필자의 의도는 왜곡하지 않았는가? 5. 간결하되 내용을 포괄적으로 담고 있는가? 


    [첨삭 기준]에 따라 앞으로 들어오는 input [요약글] 을 [원문] 과 비교해서 평가를 해보고 그 이유를 알려줘.
    '''
    messages.append({'role':'system', 'content':text})
    messages.append({"role": "user", "content": user_request.get('utterance', '')})
    callback_url = user_request.get('callbackUrl')
    try:  # Asyncia 서비스 이용 - http://asyncia.com/
        api = requests.post('https://api.asyncia.com/v1/api/request/', json={
            "apikey": "chat-gpt-key",
            "messages" :messages,
            "userdata": [["callback_url", callback_url]]},
            headers={"apikey":"asyncia-key"}, timeout=2)
        print("==========")
        print(api)
    except requests.exceptions.ReadTimeout:
        pass    
    return jsonify({
      "version" : "2.0",
      "useCallback" : True
    })
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=True)