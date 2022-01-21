from uuid import uuid4

from django.db import models
from django_fsm import FSMField, transition

from airflow import ProvaiderSearchStatus


class UUIDModel(models.Model):
    uuid = models.UUIDField("UUID идентификатор", default=uuid4, unique=True, editable=False)


class Provider(models.Model):
    name = models.CharField('Название провайдера', max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Провайдер'


class Currency(models.Model):
    data = models.JSONField(
        'Данные курса',
        blank=True,
        null=True
    )


class SearchResult(models.Model):

    class Meta:
        verbose_name = 'Результаты пойска'

    provider = models.ForeignKey(
        Provider,
        max_length=255,
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='results'
    )
    data = models.JSONField(
        'Данные поиска ',
        max_length=10,
        blank=True,
        null=True
    )
    search_id = models.ForeignKey(
        UUIDModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='results'
    )
    status = FSMField(
        ('Статус'),
        default=ProvaiderSearchStatus.PENDING,
        choices=ProvaiderSearchStatus.choices
    )

    @transition(
        field=status,
        source=ProvaiderSearchStatus.PENDING,
        target=ProvaiderSearchStatus.COMPLETED,
    )
    def completed(self, **kwargs):
        pass
