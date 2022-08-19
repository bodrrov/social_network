from django.db import models

# Create your models here.
class CmsSlider(models.Model):
    cms_img = models.ImageField(upload_to='sliderimg/')

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'