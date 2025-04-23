from django.db import models

# Create your models here.
## ESTO SE AGREGÓ TODO
class Rebate(models.Model):
    QUARTER_CHOICES = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
    ]

    year = models.IntegerField()
    quarter = models.CharField(max_length=2, choices=QUARTER_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('year', 'quarter')
        ordering = ['-year', 'quarter']

    def __str__(self):
        return f"{self.year} {self.quarter}: {self.amount}"