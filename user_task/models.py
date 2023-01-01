from django.db import models


class UserTask(models.Model):
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{}. {} - {} / {}'.format(
            self.pk,
            self.task.id,
            self.task.label,
            self.user.email,
        )
