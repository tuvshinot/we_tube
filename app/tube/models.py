from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from uuid import uuid4
import os
from datetime import datetime


def video_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'

    return os.path.join(f'videos/{instance.channel.id}/', filename)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TubeChannel(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    @property
    def subscribers_count(self):
        return self.subscribed_tubeusers.count()

    @property
    def get_videos(self):
        return self.video_set.all()

    @property
    def get_last_two(self):
        return self.video_set.order_by('-id')[:2]

    # slug_url_kwarg = 'channel'
    def get_absolute_url(self):
        return reverse('channel-detail', kwargs={'channel': self.slug})

    def __str__(self):
        return self.name

    def get_featured_video(self):
        return self.video_set.last()


class TubeUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    has_channel = models.BooleanField(default=False)
    subscriptions = models.ManyToManyField(
        TubeChannel, related_name='subscribed_tubeusers', blank=True)
    channel = models.OneToOneField(
        TubeChannel, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        default='users_profile/default.jpg', upload_to='users_profile')

    def __str__(self):
        return str(self.user)


class Video(models.Model):
    title = models.CharField(max_length=200)
    channel = models.ForeignKey(
        TubeChannel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='thumbnails')
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    video_content = models.FileField(upload_to=video_file_path)

    def __str__(self):
        return self.title

    # pk_url_kwarg = 'video'
    def get_absolute_url(self):
        return reverse('watch-video', kwargs={'video': self.pk})

    def _count_minute(self, total_seconds):
        return int(total_seconds / 60)

    def _count_hour(self, total_minutes):
        return int(total_minutes / 60)

    def _count_week(self, total_days):
        return int(total_days / 7)

    def _count_month(self, total_days):
        return int(total_days / 30)

    def _count_year(self, total_days):
        return int(total_days / 365)

    @property
    def created_at(self):
        result = ''
        now = datetime.now()
        ts = datetime(year=self.timestamp.year, month=self.timestamp.month,
                      day=self.timestamp.day, hour=self.timestamp.hour,
                      minute=self.timestamp.minute, second=self.timestamp.second)
        diff = now - ts

        if diff.days == 0:
            mins = self._count_minute(diff.total_seconds())
            if mins < 60:
                result = f'{mins} minutes ago'
            else:
                hrs = self._count_hour(mins)
                if hrs == 1:
                    result = f'{hrs} hour ago'
                else:
                    result = f'{hrs} hours ago'
        elif diff.days == 1:
            result = f'{diff.days} day ago'
        elif diff.days > 1 and diff.days < 7:
            result = f'{diff.days} days ago'
        elif diff.days >= 7 and diff.days < 30:
            wks = self._count_week(diff.days)
            if wks == 1:
                result = f'{wks} week ago'
            else:
                result = f'{wks} weeks ago'
        elif diff.days >= 30 and diff.days < 365:
            mts = self._count_month(diff.days)
            if mts == 1:
                result = f'{mts} month ago'
            else:
                result = f'{mts} months ago'
        else:
            yrs = self._count_year(diff.days)
            if yrs == 1:
                result = f'{yrs} year ago'
            else:
                result = f'{yrs} years ago'

        return result


def post_save_tubeuser_create(sender, instance, created, *args, **kwargs):
    if created:
        TubeUser.objects.get_or_create(user=instance)

    tube_user, created = TubeUser.objects.get_or_create(
        user=instance)
    tube_user.save()


post_save.connect(post_save_tubeuser_create,
                  sender=settings.AUTH_USER_MODEL)
