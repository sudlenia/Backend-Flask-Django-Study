# Приложение на django
поставить проект и рассмотреть его

https://github.com/ysv-a/django-project-ikit

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

.env.example переименовать в .env
и заполнить:
DEBUG=True
SECRET_KEY=

ключ, можно получить если ввести команду CMD
python -c "import secrets; print(secrets.token_urlsafe(38))"

полученный ключ добавить в SECRET_KEY

в примере
2 подхода, в article используется классика, пишем обработчики под различные запросы
2ой подход, в post, используются классы

эти подходы можно миксовать - разобрать


MISC:

в файле проекта settings.py, в переменной TEMPLATES, указан параметр
"DIRS": [BASE_DIR / "templates"],
это для того чтобы джанго смог увидеть общие шаблоны для всего проекта (т.е в корне проекта, папку templates), по умолчанию джанго ищет все шаблоны в приложениях, в папке templates

для переменных окружения используется библиотека environs - понять смысл

используется для форм, по bootstrap5 (css фреймворк)
crispy_forms
crispy_bootstrap5
(
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
)

pillow - для возможности загружать файлы


В общем в чем идея задачи:

1) установить пример
2) разобрать подходы
3) добавить в приложение blogs: категории, теги, комментарии (про бд поговорим в след. лекции)

Категория: id,name,slug

Тег: id,name,slug

Комментарий: id,body,author,post

Post: id, name, description, featured_image, slug, author, tags, category

то что выделено - это связи.

4) когда просматривается созданная запись post, должна быть возможность оставить комментарии, в документации, есть примеры как это делается, используем подход на основе классов
5) удалить и редактировать post, может только пользователь который создал эту запись, просматривать могут все.

6)
Реализовать вывод постов по категориям и по тегам (сами теги и категории можно создавать в админки)
(если у вас в беке нет админки, то сделать всем самим, т.е CRUD по этим моделям)

7)
в templates/post_list.html - убрать таблицу и вывести блог посты по нормальному (например, сделать карточку): заголовок, описание, изображение, указать категорию и список тегов, автора

8)
подключить WYSIWYG
https://djangopackages.org/grids/g/wysiwyg/
можно выбрать DJANGO-CKEDITOR
т.е при создании post, должен появится редактор (в бд это атрибут description)

9)
подключить свой обработчик 404 ошибок
https://django.fun/docs/django/5.0/ref/urls/#django.conf.urls.handler404

вывод должен быть таким: К сожалению, страница не существует

10)
пагинацию перенести в templates/includes

11)
у постов (тегов и категории) добавить slug, т.е это название поста, транслитом
Новость 1 -> novost-1
поискать плагины, которые это будут делать автоматически или самим написать реализацию

(
BlogDetailView, может искать как по id, так и по полю slug
в классическом представлении, это было бы так:
def article_update(request, slug):
article = Article.objects.get(slug=slug)
)

https://django.fun/docs/django/5.0/ref/class-based-views/generic-display/#detailview

12)
на странице, где выводятся все посты, должен быть поиск, ищем по заголовку или по описанию, поиск по категориям, через select

ПРИМЕР регистрации и аутентификации

https://github.com/ysv-a/django-project-ikit/tree/version3

Ссылки на документацию:

Формы:
https://django.fun/docs/django/5.0/topics/forms/

Создание форм из модели:
https://django.fun/docs/django/5.0/topics/forms/modelforms/

БД:
https://django.fun/docs/django/5.0/topics/db/
https://django.fun/docs/django/5.0/ref/models/

python manage.py makemigrations - анализ моделей и создание миграции
python manage.py migrate - перенос миграции в бд
python manage.py migrate example_app zero - откат миграции
в 1ом аргументе указывается название приложения, во 2ом номер миграции или zero(0)

Маршрутизация:
https://django.fun/docs/django/5.0/topics/http/urls/

Шаблонизатор:
https://django.fun/docs/django/5.0/#the-template-layer

View - 2 подхода - http и class-based
https://django.fun/docs/django/5.0/topics/http/views/
https://django.fun/docs/django/5.0/topics/class-based-views/

Пагинация:
https://django.fun/docs/django/5.0/topics/pagination/

Авторизация\Аутентификация
https://django.fun/docs/django/5.0/topics/auth/default/

пример, как к модели добавить пользователя:
from django.contrib.auth.models import User

class Post(models.Model):
author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")

советую написать базовое приложение по документации:
https://django.fun/docs/django/5.0/#first-steps
тогда многие вопросы отпадут, тестирование пока не смотрим



------


```
def form_valid(self, form):
comment = form.save(commit=False)
comment.article = self.object
comment.author = self.request.user
comment.save()
return super().form_valid(form)
```