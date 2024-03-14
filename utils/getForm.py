from reciation import models
import random

def getForm(number, criteria1, criteria2):
    """Ordered by criteria1 and criteria2 to get the form of words."""
    cr1Num =int (number * 0.8)
    cr2Num = number - cr1Num
    form1 = models.Word.objects.all().order_by(criteria1)[:cr1Num]
    form2 = models.Word.objects.all().order_by(criteria2)[:cr2Num]
    form = list(form1) + list(form2)
    form = sorted(form,key=lambda x:random.random())
    return form