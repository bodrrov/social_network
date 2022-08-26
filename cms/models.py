from django.db import models


class CmsSlider(models.Model):
    cms_img = models.ImageField(upload_to='sliderimg/')

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'