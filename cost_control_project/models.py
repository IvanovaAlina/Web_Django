from django.db import models
from django.contrib.auth.models import User
import django
import datetime

# Чеки
def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'cost_control_project/user_{0}/{1}'.format(instance.owner.id, filename)

class Checks(models.Model):
    text = models.CharField(max_length = 1000, blank=True)
    summ_check = models.DecimalField(max_digits = 100, decimal_places=2)
    date_check = models.DateTimeField(default=django.utils.timezone.now)
    photo_check = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('CategoryPurchase', on_delete = models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.date_check) + " " + str(self.summ_check);

class CategoryPurchase(models.Model):
    name_purchase = models.CharField(max_length = 100)
    comment = models.CharField(max_length = 1000, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name_purchase