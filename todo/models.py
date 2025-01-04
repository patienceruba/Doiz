from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class RecordRow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    progress = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically set `done` to True if progress is 100 or more
        previous_done = self.done
        self.done = self.progress >= 100

        super().save(*args, **kwargs)

        # If the task has just been marked as done, create a TaskDone entry
        if self.done and not previous_done:
            TaskDone.objects.create(record=self, user=self.user)

    def __str__(self):
        return self.title

    def update_progress(self):
        # Assuming you have a related model for subtasks
        total_subtasks = self.subtasks.count()
        if total_subtasks > 0:
            completed_subtasks = self.subtasks.filter(done=True).count()
            self.progress = (completed_subtasks / total_subtasks) * 100
            self.save()


class TaskDone(models.Model):
    record = models.OneToOneField(RecordRow, on_delete=models.CASCADE, related_name='task_done')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task '{self.record.title}' completed by {self.user.username} on {self.completed_at}"


class PDFDocument(models.Model):
    record = models.ForeignKey(RecordRow, on_delete=models.CASCADE, related_name='pdf_documents')
    pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return f"{self.record.title} - {self.pdf.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


