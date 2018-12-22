# Загрузчик комиксов xkcd в группу VK

Добавляет пост со случайным комиксом на стену в группу вк

## Требования
  
  * python3
  * Сделать группу вк, в которой вы будете выкладывать комиксы
  * [Сделать](https://vk.com/apps?act=manage) приложение для этой группы
  * получить ключ приложения, токен
  	* дать разрешения для photos, wall, communities
  	* ключ находится в настройках приложения
  	* для получения токена требуется в адресной строке ввести запрос:
	```
	https://oauth.vk.com/authorize?client_id=<client_id>&display=page&scope=photos,groups,wall,offline&response_type=token&v=<api_version>
	```
  	* добавить в файл .env в корне папки:
  	```
  	api_version=<например 5.92>
  	group_id=<ид группы>
  	client_id=<ид приложения>
  	access_token=<ваш токен>
  	```
  * установка зависимостей pip -m requirements.txt

## Пример

```$: python main.py```
номер комикса добавляется в posted.txt для избежания повторов

## Цель проекта
Код написан в учебных целях. Учебный курс для веб-разработчиков - [dvmn.org](https://dvmn.org)