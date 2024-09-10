from django.db import models

class Playlist(models.Model):
    name = models.CharField(unique=True, max_length=50)
    numberOfSongs = models.IntegerField()


class Song(models.Model):
    track = models.CharField(max_length=50)
    artist = models.CharField(unique=True, max_length=50)
    album = models.CharField(max_length=50)
    # 时间用什么Field？TimeField
    length = models.TimeField()
    # ManyToMany的参数：要关联的模型，关联的模型访问本模型的关键字
    playlist_name = models.ManyToManyField(Playlist, related_name='songs')

