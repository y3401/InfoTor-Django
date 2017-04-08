from django.db import models

# Create your models here.
class Category(models.Model):
    code_category=models.SmallIntegerField(unique=True, db_index=True, primary_key=True, verbose_name='Код категории')
    name_category=models.CharField(max_length=50, verbose_name='Наименование категории')
    load_category=models.BooleanField(default=True, verbose_name='Загружать?')
    def __str__(self):
        return ('0'+str(self.code_category))[-2:]+'. '+self.name_category
    class Meta:
        db_table='category'
        ordering=['code_category']
        verbose_name_plural='Категории' 

class Forum(models.Model):
    code_forum=models.SmallIntegerField(unique=True, db_index=True, primary_key=True, verbose_name='Код форума')
    name_forum=models.CharField(max_length=80, verbose_name='Наименование форума')
    category=models.ForeignKey(Category, default=0, verbose_name='Категория', on_delete=models.SET_DEFAULT, related_name='categorylink')
    def __str__(self):
        return ('0'+str(self.category_id))[-2:]+' - ' + str(self.code_forum)+'. '+self.name_forum    
    class Meta:
        db_table='forum'
        ordering=['category_id','code_forum']
        verbose_name_plural='Форумы'

class Torrents(models.Model):
    #category=models.ForeignKey(Category, default=0, verbose_name='Категория', on_delete=models.SET_DEFAULT)
    forum=models.ForeignKey(Forum, default=0, verbose_name='Форум', on_delete=models.SET_DEFAULT, related_name='forumlink')
    file_id=models.IntegerField(unique=True, db_index=True, primary_key=True, verbose_name='ID файла')
    hash_info=models.CharField(max_length=40, verbose_name='Hash')
    title=models.CharField(max_length=255, verbose_name='Наименование раздачи')
    size_b=models.IntegerField(verbose_name='Размер файла в байтах')
    date_reg=models.CharField(max_length=20, verbose_name='Зарегистрировано')
    class Meta:
        db_table='torrent'
        ordering=['file_id']
        verbose_name_plural='Раздачи'
    def __str__(self):
        return (str(self.file_id) + ' :: ' + self.title)    

class Contents(models.Model):
    tid=models.IntegerField(unique=True, db_index=True, primary_key=True, verbose_name='ID файла')
    cont=models.TextField(verbose_name='Контент')
    class Meta:
        db_table='contents'
        ordering=['tid']
        verbose_name_plural='Контент'

class Vers(models.Model):
    vers=models.CharField(max_length=8, verbose_name='Версия')
    class Meta:
        db_table='vers'
    def __str__(self):
        return self.vers    
