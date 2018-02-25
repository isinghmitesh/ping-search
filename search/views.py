from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

from .models import *
from .functionsEbay import *
from .functionFlipkart import *
from .functionAmazon import *
from .functionSnapdeal import *
from .forms import SearchForm, ContactForm


def surprise(request):
    eby_products = list(Ebay.objects.order_by('?')[:20].prefetch_related())
    flp_products = list(Flipk.objects.order_by('?')[:100].prefetch_related())
    snd_products = list(Snd.objects.order_by('?')[:100].prefetch_related())
    amz_products = list(Amz.objects.order_by('?')[:100].prefetch_related())
    all_images = list(chain(eby_products, flp_products, snd_products, amz_products))
    page = request.GET.get('page', 1)
    paginator = Paginator(all_images, 50)
    try:
        all_images = paginator.page(page)
    except PageNotAnInteger:
        all_images = paginator.page(1)
    except EmptyPage:
        all_images = paginator.page(paginator.num_pages)
    return render(request, 'search/surprise_me.html', {'all_images': all_images})


def search(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        form.save(commit=False)
    query = request.GET['search_term']
    keyword = proper_word(query)
    x = search_term_view(keyword)
    if x == 0:
        data_amz = make_request_azn(url_azn, keyword)
        data_snd = make_request_snd(url_snd, keyword)
        # data_flp = make_request_flp(url_flp, keyword)
        data_eby = make_request_eby(url_eby, keyword)
        c = correct_keyword_amz(data_amz)
        if c != " ":
            keyword1 = c
            item_search_term = SearchTerm.objects.create(search_term=keyword1)
            item_search_term.save()
            search_term_view(keyword1)
            search_eby(data_eby, keyword1)
            # search_flp(data_flp, keyword1)
            search_amz(data_amz, keyword1)
            search_snd(data_snd, keyword1)
            s = SearchTerm.objects.get(search_term=keyword1)
            eby_products = s.ebay_set.all().prefetch_related()
            # flp_products = s.flipk_set.all().prefetch_related()
            snd_products = s.snd_set.all().prefetch_related()
            amz_products = s.amz_set.all().prefetch_related()
            auto_complete = SearchTerm.objects.all().prefetch_related()
            SearchTerm.objects.filter(search_term=keyword).delete()
            context = {
                'eby_products': eby_products,
                # 'flp_products': flp_products,
                'amz_products': amz_products,
                'snd_products': snd_products,
                'auto_complete': auto_complete,
                'form': form
            }
            return render(request, 'search/product.html', context)

        item_search_term = SearchTerm.objects.create(search_term=keyword)
        item_search_term.save()
        # search_flp(data_flp, keyword)
        search_amz(data_amz, keyword)
        search_snd(data_snd, keyword)
        search_eby(data_eby, keyword)
    s = SearchTerm.objects.get(search_term=keyword)
    eby_products = s.ebay_set.all().prefetch_related()
    # flp_products = s.flipk_set.all().prefetch_related()
    snd_products = s.snd_set.all().prefetch_related()
    amz_products = s.amz_set.all().prefetch_related()

    # if eby_products and flp_products:
    #     auto_complete = SearchTerm.objects.all().prefetch_related()
    #     context = {
    #         'eby_products': eby_products,
    #         'flp_products': flp_products,
    #         'amz_products': amz_products,
    #         'snd_products': snd_products,
    #         'auto_complete': auto_complete,
    #         'form': form
    #     }
    #     return render(request, 'search/product.html', context)
    # else:

    auto_complete = SearchTerm.objects.all().prefetch_related()
    context = {
        'eby_products': eby_products,
        # 'flp_products': flp_products,
        'amz_products': amz_products,
        'snd_products': snd_products,
        'auto_complete': auto_complete,
        'form': form
    }
    return render(request, 'search/product.html', context)


def base(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        form.save(commit=False)
    auto_complete = SearchTerm.objects.all().prefetch_related()
    context = {
        'auto_complete': auto_complete,
        'form': form
    }
    return render(request,'search/base.html', context)



def index(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        form.save(commit=False)
    auto_complete = SearchTerm.objects.all().prefetch_related()
    context = {
        'auto_complete': auto_complete,
        'form': form
    }
    return render(request, 'search/index.html', context)


# add to your views
def contact(request):
    form_class = ContactForm
    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '') + "      " + contact_email
            to_email = [settings.EMAIL_HOST_USER]

            send_mail(contact_name, form_content, contact_email, to_email, fail_silently=True)
            email = EmailData.objects.filter(email=contact_email)
            if not email:
                store_email = EmailData.objects.create(email=contact_email)
                store_email.save()
            return render(request, 'search/done.html')

    form = SearchForm(request.GET or None)
    if form.is_valid():
        form.save(commit=False)
    auto_complete = SearchTerm.objects.all().prefetch_related()
    context = {
        'auto_complete': auto_complete,
        'form': form,
        'form_class': form_class
    }
    return render(request, 'search/contact.html', context)


def privacy_policy(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        form.save(commit=False)
    auto_complete = SearchTerm.objects.all().prefetch_related()
    context = {
        'auto_complete': auto_complete,
        'form': form
    }
    return render(request, 'search/privacy-policy.html', context)
