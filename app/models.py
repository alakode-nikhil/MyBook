from django.db import models

# Create your models here.


class Author(models.Model):

    author = models.CharField(max_length=200)

    def __str__(self) -> str:
        return '{}'.format(self.author)

class Book(models.Model):

    title = models.CharField(max_length=200, null=False)

    price = models.IntegerField(null=False, default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='book_media', null= True)

    quantity = models.IntegerField(null=False)

    def __str__(self) -> str:
        return '{}'.format(self.title)
    

    

