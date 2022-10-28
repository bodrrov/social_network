import requests
from .models import TeleSettings

def sendTelegram(tg_text, tg_author, tg_group,tg_image):
    if TeleSettings.objects.get(pk=1):
        settings = TeleSettings.objects.get(pk=1)
        token = str(settings.tg_token)
        chat_id = str(settings.tg_chat)
        text = str(settings.tg_message)
        api = 'https://api.telegram.org/bot'
        files = {'photo': tg_image}
        method = api + token + '/sendMessage'
        url = api + token + '/sendPhoto';

        if text.find('{') and text.find('}') and text.rfind('{') and text.rfind('}'):
            part_1 = text[0:text.find('{')]
            part_2 = text[text.find('}') + 1:text.rfind('{')]
            part_3 = text[text.find('}'):-1]

            text_slice = f" Новый пост: {tg_text}\nАвтор: {tg_author}\nГруппа: {tg_group}"
        else:
             text_slice = text

        try:
            req = requests.post(method, data={
                'chat_id': chat_id,
                'text': text_slice
                })
            req = requests.post(url, files=files, data={'chat_id': 'chat_id'})
        except:
            pass

        finally:
            if req.status_code != 200:
                print('Ошибка отправки!')
            elif req.status_code == 500:
                print('Ошибка 500')
            else:
                print('Всё Ок сообщение отправлено!')
    else:
        pass

def sendImage(tg_image):
    settings = TeleSettings.objects.get(pk=1)
    token = str(settings.tg_token)
    chat_id = str(settings.tg_chat)
    api = 'https://api.telegram.org/bot'
    url = api + token + '/sendPhoto';
    files = {'photo': tg_image}
    data = {'chat_id' : "chat_id"}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)