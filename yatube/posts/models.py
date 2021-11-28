from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название сообщества',
                             max_length=200,
                             help_text='Дайте название сообществу'
                             )
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание сообщества',
                                   max_length=2000)

    class Meta:
        pass

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'post text',
        help_text='enter post text'
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',  # нет в теории, почему?
        # verbose_name='Автор' # добавилось из теории
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='group',
        help_text='Выберите группу'
    )
    # Поле для картинки (необязательное)
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',  # директорию,для загрузки пользовательских файлов
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'  # добавилось из теории
        verbose_name_plural = 'Посты'  # добавилось из теории

    def __str__(self):  # для отображения объектов в интерфейсе администратора
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'date published',
        auto_now_add=True
    )


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower'
                             # verbose_name='подписчик'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following'
                               # verbose_name='автор'
                               )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user.username}-->{self.author.username}'
