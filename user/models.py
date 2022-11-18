from django.db import models
from django.db.models import Avg


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name="Account")
    password = models.CharField(max_length=32, verbose_name="Password")
    phone = models.CharField(max_length=32, verbose_name="Phone NUmber")
    name = models.CharField(max_length=32, verbose_name="Name", unique=True)
    address = models.CharField(max_length=32, verbose_name="Address")
    email = models.EmailField(verbose_name="Email Address")

    class Meta:
        verbose_name_plural = "User"
        verbose_name = "User"

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=32, verbose_name="Tag")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tag"

    def __str__(self):
        return self.name


class Book(models.Model):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name="Tag",
        related_name="tags",
        blank=True,
        null=True,
    )
    collect = models.ManyToManyField(User, verbose_name="Collector", blank=True)
    sump = models.IntegerField(verbose_name="Collections", default=0)
    rate_num = models.IntegerField(verbose_name="Number of Ratings", default=0)
    title = models.CharField(verbose_name="Course Name", max_length=32)
    author = models.CharField(verbose_name="Instructor", max_length=32)

    intro = models.TextField(verbose_name="Description")
    num = models.IntegerField(verbose_name="Views", default=0)
    pic = models.FileField(verbose_name="Picture", max_length=64, upload_to='book_cover')
    prize = (("诺贝尔文学奖", "诺贝尔文学奖"), ("茅盾文学奖", "茅盾文学奖"), ("None", "None"))
    good = models.CharField(verbose_name="Course Number", max_length=32)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Course"

    def __str__(self):
        return self.title


class Rate(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Course id"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User id",
    )
    mark = models.FloatField(verbose_name="Rate")
    create_time = models.DateTimeField(verbose_name="Publish time", auto_now_add=True)

    @property
    def avg_mark(self):
        average = Rate.objects.all().aggregate(Avg('mark'))['mark__avg']
        return average

    class Meta:
        verbose_name = "Rating Information"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Users")
    content = models.TextField(verbose_name="Content")
    create_time = models.DateTimeField(auto_now_add=True)
    good = models.IntegerField(verbose_name="Likes", default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Courses")

    class Meta:
        verbose_name = "Comments"
        verbose_name_plural = verbose_name


class Action(models.Model):
    user = models.ManyToManyField(User, verbose_name="Participants", blank=True)
    # new = models.ManyToManyField(
    #     User, verbose_name="审核用户", related_name="newuser", blank=True
    # )
    one = models.ImageField(upload_to="media", verbose_name="First")
    two = models.ImageField(upload_to="media", verbose_name="Second", null=True)
    three = models.ImageField(upload_to="media", verbose_name="Third", null=True)
    title = models.CharField(verbose_name="Activity title", max_length=64)
    content = models.TextField(verbose_name="Activity Content")
    status = models.BooleanField(verbose_name="Status")

    class Meta:
        verbose_name = "Activities"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ActionComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    action = models.ForeignKey(Action, on_delete=models.CASCADE, verbose_name="Activities")
    comment = models.TextField(verbose_name="Activity Comments")
    create_time = models.DateTimeField(auto_now_add=True)


class MessageBoard(models.Model):
    # 读书论坛
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    title = models.CharField(max_length=64, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    look_num = models.IntegerField(verbose_name='Clicks', default=1)
    like_num = models.IntegerField(verbose_name='Likes', default=0)
    feebback_num = models.IntegerField(verbose_name='Replies', default=0)
    collect_num = models.IntegerField(verbose_name='Collections', default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comments"
        verbose_name_plural = verbose_name


class CollectBoard(models.Model):
    # 收藏、点赞留言帖子
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Users")
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="Comments")
    create_time = models.DateTimeField(auto_now_add=True)
    is_collect = models.BooleanField(default=False, verbose_name='Collect?')
    is_like = models.BooleanField(default=False, verbose_name='Like?')

    class Meta:
        verbose_name = "Collections and likes"
        verbose_name_plural = verbose_name


class BoardComment(models.Model):
    # 回复留言
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="Comment")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User", related_name="user"
    )
    content = models.TextField( verbose_name="Content")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = verbose_name


class Num(models.Model):
    users = models.IntegerField(verbose_name="Number of Users", default=0)
    books = models.IntegerField(verbose_name="Number of Courses", default=0)
    comments = models.IntegerField(verbose_name="Number of Comments", default=0)
    rates = models.IntegerField(verbose_name="Ratings Summary", default=0)
    actions = models.IntegerField(verbose_name="Activities Summary", default=0)
    message_boards = models.IntegerField(verbose_name="Comments Summary", default=0)

    class Meta:
        verbose_name = "Statistics"
        verbose_name_plural = verbose_name

