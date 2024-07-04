# API
по апи, что нужно сделать
установить DRF

https://www.django-rest-framework.org/


1. настроить API сущности blog
на выходе получаем коллекцию постов, а в ней автор, теги, категория

смотрите мой пример

2. если есть ключ в GET include
/api/blogs?include=comments
тогда в сущности post, подгрузить все комментарии

3. получить все комментарии поста
например (это просто пример! делайте как удобно)
/api/comments?filter[post]=1

на выходе получаем все комментарии поста,

или можно так сделать
/api/blogs/1/comments - получили все комментарии поста 1

3. настроить фильтры, т.е поиск, у сущности post
например по имени и по категории
читаем про библиотеку django-filter

4. создание поста, файл загружать не нужно (хотя мб с коробки заработает)
по поводу авторизации, в своем примере я использовал jwt

https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

5. добавить документацию по swagger'у
https://drf-spectacular.readthedocs.io/en/latest/

тут у меня есть примеры
https://github.com/ysv-a/django-project-ikit/tree/version4

и читаем документацию, в разделе API Guide
https://www.django-rest-framework.org/api-guide/requests/


ps. по поводу задачи 2 и 3, это все автоматом решает json-api, но вам это нужно самостоятельно реализовать
ps2. CRUD по остальным сущностям делать не нужно