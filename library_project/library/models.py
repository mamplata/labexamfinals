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

    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    book        = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,  # Orphan when book is deleted :contentReference[oaicite:1]{index=1}
        null=True,
        blank=True,
        related_name='transactions'
    )
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status      = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='borrowed'
    )

    def save(self, *args, **kwargs):
        # Adjust copies_available on borrow/return
        if self._state.adding and self.status == 'borrowed' and self.book:
            self.book.copies_available = models.F('copies_available') - 1
            self.book.save(update_fields=['copies_available'])
        elif not self._state.adding and self.status == 'returned' and self.book:
            self.book.copies_available = models.F('copies_available') + 1
            self.book.save(update_fields=['copies_available'])

        super().save(*args, **kwargs)

    def __str__(self):
        title = self.book.title if self.book else "(book deleted)"
        return f"{self.user} → {title} ({self.status})"
