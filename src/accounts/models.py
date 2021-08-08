from django.db import models

class Person(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.username


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Person, blank=True,
                                     null=True, related_name="groups",
                                     through='Membership'
                                     )
    
    def __str__(self):
        return F"{self.name} Group."


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-order']
