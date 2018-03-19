from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product
from django.template import RequestContext
from django.template.loader import render_to_string
from django import urls
from cart import cart
from django.http import HttpResponseRedirect
from catalog.forms import ProductAddToCartForm


# Create your views here.
def index(request):
    """ site home page """
    message = 'Modern Musician is an online supplier of instruments, sheet music, and other accessories for musicians'
    return render(request, 'catalog/index.html', {'message': message})


def show_category(request, category_slug):
    """ view for each individual category page """
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description

    context = {
        'c': c,
        'products': products,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description
        }

    return render(request, 'catalog/category.html', context)


def show_product(request, product_slug):
    """ view for each product page """
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # evaluate the HTTP method, change as needed
    if request.method == 'POST':
        # create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if posted data is valid
        if form.is_valid():
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
        url = urls.reverse('cart')
        return HttpResponseRedirect(url)
    else:
        # create the unbound form. Notice the request as a keyword argument
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set test cookie to make sure cookies are enabled
    request.session.set_test_cookie()

    context = {
        'p': p,
        'categories': categories,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'form': form,
        }
    return render(request, 'catalog/product.html', context)
