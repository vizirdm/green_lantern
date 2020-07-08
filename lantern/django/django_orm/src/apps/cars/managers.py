from django.db import models



class CarQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status='pending')

    def published(self):
        return self.filter(status='published')

    def sold(self):
        return self.filter(status='sold')