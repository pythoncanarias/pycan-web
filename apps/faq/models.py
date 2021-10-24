from django.db import models


class FAQItem(models.Model):
    '''Preguntas frecuentes'''

    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
