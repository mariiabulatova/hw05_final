from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название сообщества',
                             max_length=200,
                             help_text='Дайте название сообществу'
                             )
    slug = models.SlugField(unique=True)
    # AE: Свойство `description` модели `Group` должно быть `TextField` ))
    description = models.TextField('Описание сообщества')

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
        related_name='posts',
        verbose_name='author'
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
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
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
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following'
                               )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user.username}-->{self.author.username}'
