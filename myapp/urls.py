from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'search/',
        views.search_books,
        name='search_books'
    ),

    path(
        'category/<int:category_id>/',
        views.category_books,
        name='category_books'
    ),

    path(
        'add-to-cart/<int:book_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'remove-cart/<int:cart_id>/',
        views.remove_cart,
        name='remove_cart'
    ),

    path(
        'update-quantity/<int:cart_id>/',
        views.update_quantity,
        name='update_quantity'
    ),

    path(
        'place-order/',
        views.place_order,
        name='place_order'
    ),
    path(
    'payment/',
    views.payment,
    name='payment'
),

path(
    'payment-success/',
    views.payment_success,
    name='payment_success'
),

    path(
        'orders/',
        views.orders,
        name='orders'
    ),

    path(
        'cancel-order/<int:order_id>/',
        views.cancel_order,
        name='cancel_order'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'wishlist/',
        views.wishlist,
        name='wishlist'
    ),

    path(
        'add-wishlist/<int:book_id>/',
        views.add_wishlist,
        name='add_wishlist'
    ),
    path(
        'book/<int:book_id>/',
        views.book_detail,
        name='book_detail'
    ),
    path(
        'remove-wishlist/<int:wishlist_id>/',
         views.remove_wishlist,
         name='remove_wishlist'
    ),
    path(
    'verify-otp/',
    views.verify_otp,
    name='verify_otp'
),
path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ),
    name='password_reset_complete'
),
path('resend-otp/', views.resend_otp, name='resend_otp'),

]