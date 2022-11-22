from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    role = models.IntegerField()
    # role = models.ForeignKey('role.role', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{}. {} {} - with the email: {}, created on {}, updated on {}'.format(self.pk, self.firstname, self.lastname, self.email, self.created_at, self.updated_at)