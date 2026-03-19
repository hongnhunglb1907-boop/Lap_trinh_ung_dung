from django.db import models

class LoanProfile(models.Model):
    STATUS_CHOICES = [
        ('Đã duyệt', 'Đã duyệt'),
        ('Chờ xử lý', 'Chờ xử lý'),
        ('Từ chối', 'Từ chối'),
    ]
    code         = models.CharField(max_length=20)
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    income       = models.DecimalField(max_digits=15, decimal_places=0)
    score        = models.IntegerField()
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES)
    occupation   = models.CharField(max_length=50, default='Nhân viên văn phòng')
    work_years   = models.IntegerField(default=1)
    loan_amount  = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    loan_purpose = models.CharField(max_length=100, default='Tiêu dùng')
    debt_ratio   = models.IntegerField(default=20)
    active_loans = models.IntegerField(default=0)
    late_payments= models.IntegerField(default=0)
    evaluated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_risk_level(self):
        if self.score >= 650: return 'Thấp'
        if self.score >= 500: return 'Trung bình'
        return 'Cao'