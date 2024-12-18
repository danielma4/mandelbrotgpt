from django.db import models

# here, we create models which match our database tables
# allowing us to work with data from the db

# migrating -> propagating changes in models to database
# makemigration, then apply migrate
# this is very much a version control schema for dbases

# Create your models here.
class Equation(models.Model):
    name = models.CharField(max_length=100)
    equation = models.TextField()
    creators = models.TextField()

    def __str__(self):
        return self.name

class Mathematician(models.Model):
    name = models.CharField(max_length=100)
    fields = models.TextField()

    def __str__(self):
        return self.name