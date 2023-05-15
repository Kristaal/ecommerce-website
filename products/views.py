from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Product, Category, Wishlist, ProductReview
from .forms import ProductForm, ReviewForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    user = request.user
    wished_list = []
    if user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=user)
        for i in wishlist:
            wished_list.append(i.product)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'wished_list': wished_list,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm()
    # Check if product is in users wishlist
    user = request.user
    in_wishlist = False
    wishlist_item = None
    if user.is_authenticated:
        wishlist_item = Wishlist.objects.filter(
            product=product, user=user).first()
        in_wishlist = Wishlist.objects.filter(
            product=product, user=user).exists()
    # Add a product review
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review = form.save()
            messages.success(request, 'Successfully added review!')
            store_email = settings.DEFAULT_FROM_EMAIL
            subject = f'You got a new review for {review.product}!'
            body = f'New review from: {review.user}. Login to admin dashboard \
                to review it. Product: {review.product} \
                    https://beautybliss.herokuapp.com/admin/'
            send_mail(subject, body, store_email, [store_email])
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add review.\
                 Please check that the form is valid.')

    context = {
        'product': product,
        'form': form,
        'in_wishlist': in_wishlist,
        'wishlist_item': wishlist_item,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def wishlist(request):
    """
    View wishlist for logged in user
    """
    if request.user.is_authenticated:
        user = request.user
        wishlist = Wishlist.objects.filter(user=user)
        items_count = wishlist.count()
    context = {
        'wishlist': wishlist,
        'items_count': items_count
    }
    template = 'products/wishlist.html'

    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id, user_id):
    """
    Add products to wishlist
    """
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        product=product, user=user)
    if created:
        wishlist_item.save()
        messages.success(request, 'Product added to wishlist!')
    else:
        messages.info(request, 'Product is already in your wishlist.')

    return redirect(reverse('product_detail', args=[product_id]))


@login_required
def remove_from_wishlist(request, wishlist_id):
    """
    Remove item from wishlist
    """
    wishlist_item = Wishlist.objects.get(id=wishlist_id)
    wishlist_item.delete()
    messages.success(request, 'Removed from wishlist!!')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        if 'wishlist' in referer:
            return redirect('wishlist')
        else:
            return redirect(referer)
    else:
        return redirect('wishlist')


@login_required
def add_to_wishlist_all_products(request, product_id, user_id):
    """
    Add product to wishlist
    """
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
                                product=product,
                                user=user
    )
    if created:
        wishlist_item.save()
        messages.success(request, 'Product added to wishlist!')
    else:
        messages.info(request, 'Product is already in your wishlist.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_wishlist_all_products(request, product_id, user_id):
    """
    Remove item from wishlist
    """
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    wishlist_item = Wishlist.objects.filter(product=product, user=user)
    wishlist_item.delete()
    messages.success(request, 'Removed from wishlist!!')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        if 'wishlist' in referer:
            return redirect('wishlist')
        else:
            return redirect(referer)
    else:
        return redirect('wishlist')
