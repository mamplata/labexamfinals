from django.conf import settings
from django.db import models

class Book(models.Model):
    title            = models.CharField(max_length=200)
    author           = models.CharField(max_length=200)
    isbn             = models.CharField(max_length=20, unique=True)
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class BorrowTransaction(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ]
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=True, blank=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    def save(self, *args, **kwargs):
        if self.pk is None and self.status == 'borrowed':
            self.book.copies_available -= 1
            self.book.save()
        elif self.status == 'returned':
            self.book.copies_available += 1
            self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} → {self.book} ({self.status})"