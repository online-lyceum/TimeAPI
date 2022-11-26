[Репозиторий проекта](https://github.com/prostoLavr/async_lyceum_api.git)

## Назначение
Данное API предназначено для получения и создания уроков в системе "Лицей в цифре". 
Он позволяет ученикам и учителям смотреть своё расписание, 
учителя также имеют возможность создавать и редактировать расписание.

## Домены
У API есть две версии _stable_ и _dev_, 
стабильная и нестабильная соответственно. 
Если ваше приложение находится на стадии разработки, 
рекомендуется использовать _dev_ версию API. 
_stable_: https://async-api.lava-land.ru 
_dev_: https://test-async-api.lava-land.ru.

## Как работают запросы
Чтобы получить данные из API, необходимо послать GET запрос, 
состоящий из двух частей: домен и URL-путь. 
Запись URL-пути всегда начинается с символа `/`. 
Также у нас принято не писать `/` в конце запроса. 
Например, `https://test-async-api.lava-land.ru/school` вернёт список всех школ.
В данном примере URL-путь это /school. 
Далее для обозначения запроса вместо 
`https://test-async-api.lava-land.ru/school` будет использоваться `/school`. 
А также под терминами URL и адрес будет подразумеваться URL-путь.

Названия URL запросов выбираются на основе REST-API. 
Знать что это такое необязательно. Детальнее почитать об этом можно тут. 
Говоря коротко, это способ именования запросов, 
в котором используется следующая схема. 
`/объект` - чтобы получить список таких объектов. 
И `/объект/уникальный_номер_объекта` - чтобы получить объект с 
заданным в URL уникальным номером. 
В нашей системе принято завершать запрос объектом, а не уникальным номером. 
Например, вот корректный запрос `/school/1/class` - это список классов в школе,
а вот некорректный `/school/1`, последний запрос работать не будет.

Данные в теле запроса (в разных системах встречаются названия body, data или text) передаются в формате JSON. Всегда тело запроса это словарь! Внутри словаря могут быть списки, строки, числа, булевы значения, но тело запроса должно быть словарём.

## Как пользоваться swagger (устарело)
Под этим описанием вы увидете список доступых серверов API. 
В зависимости от сервера, ответ на один и тот же запрос может отличаться. 
ВНИМАНИЕ используйте стабильную версию для проверки ТОЛЬКО GET запросов. 
На тестовой версии можете выполнять любые запросы. 
Чтобы выполнить запрос, откройте содержимое карточки запроса, кликнув на неё, 
далее нажмите "Try it out", введите поля запроса, если это необходимо, 
и кликните по "Execute". После выполения запроса ниже вы увидите команду, 
которая была запущена и под ней ответ от сервера. 
В ответе будут прописаны код (200 - удачный), JSON и заголовки. 
В разделе Responses не перепутайте ответ от сервера (Server response) 
с ответом сгенерированным swagger (Responses). Последний нужен, чтобы увидеть,
как ответ на запрос выглядит в общем виде.