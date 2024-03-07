from django.db import models

# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    example = models.CharField(max_length=100, blank=True, null=True)
    submission = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    correct_rate = models.FloatField(default=0.0)
    occur_weight = models.FloatField(default=0.0)
    last_correct = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    memory_strength = models.FloatField(default=5)
    objects = models.Manager()
    def __str__(self):
        return self.word
# 按照权重由高到低出现在首页。
# 出现权重应该由 正确率和出现次数共同决定，
# rate down, submissions down, weight up.
# weigh