import requests, time
from configs.settings import WEBHOOK_LINK

class CaseWebhook():
    
    def send_event_assessment(data=None, hash=None):
        
        try:
            start_time = time.time()

            url = WEBHOOK_LINK
            dados_dict = {key: value for key, value in data.items()}
            dados_dict['hash'] = str(hash)
            response = requests.post(url, json=dados_dict)

            elapsed_time = time.time() - start_time
            tempo_decorrido = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                
            if response.status_code == 200:
                data = {"status": 200, "runtime": tempo_decorrido} 
            else:
                data = {"status": 500, "runtime": tempo_decorrido} 
                
            return data
        
        except Exception as err:
            print("erro...: ", err)
        
