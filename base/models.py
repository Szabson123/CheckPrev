from django.db import models

Flags = [
    ('down', 'Down'),
    ('up', 'Up'),
    ('nothing', 'Nothing'),
]


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    

class Famili(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f'{self.name} {self.category.name}'
    

class Product(models.Model):
    check_prev = models.ForeignKey(Famili, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    cols = models.IntegerField()
    img_width = models.IntegerField()
    img_height = models.IntegerField()
    
    def __str__(self) -> str:
        return f'{self.name} {self.check_prev.category.name}'
    

class Composition(models.Model):
    check_prev = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_change_down_flag = models.CharField(choices=Flags, default='nothing', max_length=255)
    phase = models.CharField(max_length=255)
    upper_snake = models.BooleanField(default=True)
    set_phase = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.name} {self.check_prev.check_prev.category.name}'
    
    
class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_none = models.ImageField(upload_to='product_media/')
    image_true = models.ImageField(upload_to='product_media/')
    image_false = models.ImageField(upload_to='product_media/')
    image_other = models.ImageField(upload_to='product_media/')