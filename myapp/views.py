import razorpay
from django.conf import settings

from django.utils import timezone
from .models import (
    UserProfile,
    Book,
    Cart,
    Order,
    Wishlist,
    Category,
    Review
)

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
import random
from django.core.mail import send_mail
from .models import UserOTP


def home(request):
    books = Book.objects.all()

    return render(
        request,
        'index.html',
        {'books': books}
    )


def register_view(request):

    error = ""

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username'].strip()
            email = form.cleaned_data['email'].strip()
            phone = form.cleaned_data['phone'].strip()
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if User.objects.filter(username=username).exists():
                error = "Username already exists"

            elif User.objects.filter(email=email).exists():
                error = "Email already registered"

            elif UserProfile.objects.filter(phone=phone).exists():
                error = "Mobile Number already exists"

            elif password != confirm_password:
                error = "Passwords do not match"

            else:

                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )

                UserProfile.objects.create(
                    username=username,
                    email=email,
                    phone=phone
                )

                return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form,
            'error': error
        }
    )


def login_view(request):

    message = ""

    if request.method == "POST":

        email = request.POST.get('username')
        password = request.POST.get('password')

        try:

            user_obj = User.objects.get(email=email)

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user:

                otp = str(random.randint(100000, 999999))

                UserOTP.objects.create(
                    email=email,
                    otp=otp
                )
                request.session['otp_time'] = timezone.now().timestamp()

                send_mail(
                    'Rajalakshmy Book Store OTP',
                    f'Your OTP is {otp}',
                    'yourgmail@gmail.com',
                    [email],
                    fail_silently=False
                )

                request.session['user_id'] = user.id
                request.session['email'] = email

                return redirect('verify_otp')

            else:
                message = "Invalid Email or Password"

        except User.DoesNotExist:
            message = "Invalid Email or Password"

    return render(
        request,
        'login.html',
        {'message': message}
    )


# PRODUCTS PAGE
def products(request):
    books = Book.objects.all()

    return render(
        request,
        'products.html',
        {'books': books}
    )


# ADD TO CART
@login_required
def add_to_cart(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    Cart.objects.create(
        user=request.user,
        product=book,
        quantity=1
    )

    return redirect('cart')


# CART PAGE
@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )

@login_required
def payment_success(request):

    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:

        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect("orders")


# PLACE ORDER
@login_required
def place_order(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        return redirect('cart')

    for item in cart_items:

        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return render(
        request,
        'success.html'
    )


# ORDER HISTORY
@login_required
def orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-ordered_at')

    return render(
        request,
        'orders.html',
        {'orders': orders}
    )
from django.shortcuts import get_object_or_404

@login_required
def remove_cart(request, cart_id):

    item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    item.delete()

    return redirect('cart')
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import redirect, get_object_or_404

@login_required
def update_quantity(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    qty = request.POST.get("quantity")

    cart_item.quantity = int(qty)
    cart_item.save()

    return redirect("cart")

from .models import Cart, Order, Book
@login_required
def dashboard(request):

    total_books = Book.objects.count()

    cart_count = Cart.objects.filter(
        user=request.user
    ).count()

    order_count = Order.objects.filter(
        user=request.user
    ).count()

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    recent_orders = Order.objects.filter(
        user=request.user
    ).order_by('-ordered_at')[:5]

    return render(
        request,
        'dashboard.html',
        {
            'total_books': total_books,
            'cart_count': cart_count,
            'order_count': order_count,
            'wishlist_count': wishlist_count,
            'recent_orders': recent_orders
        }
    )
@login_required
def add_wishlist(request, book_id):

    book = Book.objects.get(id=book_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect('products')

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )
# SEARCH BOOKS
def search_books(request):

    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(
            title__icontains=query
        )
    else:
        books = Book.objects.all()

    return render(
        request,
        'products.html',
        {'books': books}
    )


# CATEGORY BOOKS
def category_books(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    books = Book.objects.filter(
        category=category
    )

    return render(
        request,
        'products.html',
        {
            'books': books,
            'category': category
        }
    )


# CANCEL ORDER
@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order.status = "Cancelled"
    order.save()

    return redirect('orders')


# BOOK DETAILS + REVIEW
def book_detail(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id
    )

    reviews = Review.objects.filter(
        book=book
    ).order_by('-created_at')

    if request.method == "POST":

        if request.user.is_authenticated:

            Review.objects.create(
                user=request.user,
                book=book,
                rating=request.POST.get('rating'),
                comment=request.POST.get('comment')
            )

            return redirect(
                'book_detail',
                book_id=book.id
            )

    return render(
        request,
        'book_detail.html',
        {
            'book': book,
            'reviews': reviews
        }
    )
@login_required
def remove_wishlist(request, wishlist_id):

    item = get_object_or_404(
        Wishlist,
        id=wishlist_id,
        user=request.user
    )

    item.delete()

    return redirect('wishlist')
def verify_otp(request):

    message = ""

    if request.method == "POST":

        otp = request.POST.get("otp")
        email = request.session.get("email")

        otp_time = request.session.get("otp_time")

        if otp_time:

            current_time = timezone.now().timestamp()

            if current_time - otp_time > 120:

                message = "OTP Expired. Please Resend OTP"

                return render(
                    request,
                    "verify_otp.html",
                    {"message": message}
                )

        otp_obj = UserOTP.objects.filter(
            email=email,
            otp=otp
        ).last()

        if otp_obj:

            user_id = request.session.get("user_id")

            user = User.objects.get(id=user_id)

            login(request, user)

            return redirect("home")

        else:

            message = "Invalid OTP"

    return render(
        request,
        "verify_otp.html",
        {"message": message}
    )
def resend_otp(request):

    email = request.session.get('email')

    if not email:
        return redirect('login')

    otp = str(random.randint(100000,999999))

    UserOTP.objects.create(
        email=email,
        otp=otp
    )

    request.session['otp_time'] = timezone.now().timestamp()

    send_mail(
        'Rajalakshmy Book Store OTP',
        f'Your New OTP is {otp}',
        'yourgmail@gmail.com',
        [email],
        fail_silently=False
    )

    return redirect('verify_otp')

@login_required
def payment(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment_data = {
        "amount": int(total * 100),
        "currency": "INR",
        "payment_capture": 1
    }

    razorpay_order = client.order.create(data=payment_data)

    context = {
        "order_id": razorpay_order["id"],
        "amount": payment_data["amount"],
        "key": settings.RAZORPAY_KEY_ID,
        "total": total
    }

    return render(request, "payment.html", context)

@login_required
def payment_success(request):

    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:

        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return render(
        request,
        'success.html'
    )





     