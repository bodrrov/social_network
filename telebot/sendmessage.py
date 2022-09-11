import requests
from .models import TeleSettings


def sendTelegram( tg_text, tg_author):
	if TeleSettings.objects.get(pk=1):
		settings = TeleSettings.objects.get(pk=1)
		token = str(settings.tg_token)
		chat_id = str(settings.tg_chat)
		text = str(settings.tg_message)
		api = 'https://api.telegram.org/bot'
		method = api + token + '/sendMessage'

		if text.find('{') and text.find('}') and text.rfind('{') and text.rfind('}'):
			part_1 = text[0:text.find('{')]
			part_2 = text[text.find('}')+1:text.rfind('[')]
			part_3 = text[text.find(']')+1:text.rfind('{')]


			text= tg_text
			author = tg_author

		else:
			text = text
			author = tg_author

		try:
			req = requests.post(method, data={
				'chat_id': chat_id,
				'text': text, 'author': author
				})
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