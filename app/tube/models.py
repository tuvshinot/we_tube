from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TubeChannel(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    @property
    def subscribers_count(self):
        return self.tubeuser_set.count()

    # slug_url_kwarg = 'channel'
    def get_absolute_url(self):
        return reverse('channel-detail', kwargs={'channel': self.slug})

    def __str__(self):
        return self.name


class TubeUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    has_channel = models.BooleanField(default=False)
    subscriptions = models.ManyToManyField(
        TubeChannel, related_name='subscribed_channels', blank=True)
    channel = models.OneToOneField(
        TubeChannel, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        default='users_profile/default.jpg', upload_to='users_profile')

    def __str__(self):
        return str(self.user)

    @property
    def subscribed_channels(self):
        return self.subscribed_channels.all()


def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.channel.id, filename)


class Video(models.Model):
    title = models.CharField(max_length=200)
    channel = models.ForeignKey(
        TubeChannel, on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='profile_pics')
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    video_content = models.FileField(upload_to=directory_path)

    def __str__(self):
        return self.title

    # pk_url_kwarg = 'v'
    def get_absolute_url(self):
        return reverse('video-detail', kwargs={'v': self.pk})


def post_save_tubeuser_create(sender, instance, created, *args, **kwargs):
    if created:
        TubeUser.objects.get_or_create(user=instance)

    tube_user, created = TubeUser.objects.get_or_create(
        user=instance)
    tube_user.save()


post_save.connect(post_save_tubeuser_create,
                  sender=settings.AUTH_USER_MODEL)
