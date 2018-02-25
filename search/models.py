from django.db import models


class SearchTerm(models.Model):
    search_term = models.CharField(max_length=300)

    def __str__(self):
        return self.search_term


class Imgaes(models.Model):
    img_id = models.CharField(max_length=30)
    low_res = models.CharField(max_length=500)
    hi_res = models.CharField(max_length=500)

    def __str__(self):
        return self.img_id


class Reviews_amz(models.Model):
    p_id = models.CharField(max_length=30)
    r_head = models.CharField(max_length=200)
    r_name = models.CharField(max_length=100)
    r_date = models.CharField(max_length=10)
    r_statement = models.CharField(max_length=2000)
    r_helpful = models.CharField(max_length=50)
    r_tags = models.CharField(max_length=50)


class Ebay(models.Model):
    search_id_eby = models.ManyToManyField(SearchTerm)
    p_id = models.CharField(max_length=20)
    p_name = models.CharField(max_length=250)
    p_link = models.CharField(max_length=1000)
    mrp = models.CharField(max_length=30)
    act_price = models.CharField(max_length=30)
    p_description = models.TextField()
    p_img = models.CharField(max_length=2000)
    p_hotness = models.CharField(max_length=50)

    def __str__(self):
        return self.p_name + " | " + self.p_id


class Flipk(models.Model):
    search_id_flp = models.ManyToManyField(SearchTerm)
    p_name = models.CharField(max_length=250)
    p_link = models.CharField(max_length=1000, null=True)
    st_price = models.CharField(max_length=30)
    act_price = models.CharField(max_length=30)
    p_id = models.CharField(max_length=20)
    p_description = models.TextField()
    p_discount = models.CharField(max_length=10)
    in_stock = models.BooleanField(default=True)
    p_brand_name = models.CharField(max_length=100)
    p_img = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.p_name + " | " + self.p_id


class Amz(models.Model):
    search_id_amz = models.ManyToManyField(SearchTerm)
    p_link = models.CharField(max_length=1000)
    p_name = models.CharField(max_length=250)
    p_id = models.CharField(max_length=20)
    st_price = models.CharField(max_length=30)
    act_price = models.CharField(max_length=30)
    review = models.TextField()
    p_img = models.CharField(max_length=2000)

    def __str__(self):
        return self.p_name + "  |  " + self.p_id


class Snd(models.Model):
    search_id_snd = models.ManyToManyField(SearchTerm)
    p_link = models.CharField(max_length=1000)
    p_name = models.CharField(max_length=250)
    p_id = models.CharField(max_length=20)
    st_price = models.CharField(max_length=30)
    act_price = models.CharField(max_length=30)
    review = models.TextField()
    p_img = models.CharField(max_length=20000)

    def __str__(self):
        return self.p_name + "  |  " + self.p_id


class Clu(models.Model):
    p_name = models.CharField(max_length=500)
    price = models.CharField(max_length=30)
    review = models.CharField(max_length=10)
    p_id = models.CharField(max_length=20)
    p_img = models.CharField(max_length=20000)
    p_price = models.CharField(max_length=30)

    def __str__(self):
        return self.p_name


class EmailData(models.Model):
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email
