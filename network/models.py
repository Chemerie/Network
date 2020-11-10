from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
	poster = models.CharField(max_length=64)
	content = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)

	def serialize(self):
		return{
		"id": self.id,
		"poster": self.poster,
		"content": self.content,
		"date": self.date,
		"likes": self.likes
		}

class Follow(models.Model):
	following = models.CharField(max_length=64)
	followed = models.CharField(max_length=64)

	def serialize(self):
	 	return{
	 	"id": self.id,
	 	"following": self.following,
	 	"followed": self.followed
	 	}


class Like(models.Model):
	liker = models.CharField(max_length=64)
	post_id = models.IntegerField(default=0)

	def serialize(self):
		return{
		"id": self.id,
		"liker": self.liker,
		"p_id": self.post_id
		}