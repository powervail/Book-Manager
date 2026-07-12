from django.db import models
import os

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    total_pages =models.IntegerField()
    current_page = models.IntegerField(default=0)

    STATUS = [
        ("NS", "Not Started"),
        ("RD", "Reading"),
        ("CP", "Completed")
    ]

    status = models.CharField(max_length=2, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    is_favorite = models.BooleanField(default=False)

    book_file = models.FileField(upload_to="books/", blank=True, null=True)


    @property
    def is_pdf(self):
        if self.book_file:
            return os.path.splitext(self.book_file.name)[1].lower() == ".pdf"
        return False
    

    @property
    def is_epub(self):
        if self.book_file:
            return os.path.splitext(self.book_file.name)[1].lower() == ".epub"
        return False

    @property
    def progress(self):
        if self.total_pages == 0:
            return 0
        return int((self.current_page / self.total_pages) * 100)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created_at"]


class Note(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200, blank=True, default="")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.book.title}"
    
    class Meta:
        ordering = ["-created_at"]

class Quote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quotes")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
    
    class Meta:
        ordering = ["-created_at"]