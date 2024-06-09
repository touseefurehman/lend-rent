from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import RentalItem
from rating.models import Comment
from accounts.models import MyUser
from django.db.models import Avg
from items.models import ItemCategory,CheckoutInfo
from django.conf import settings  # new
from django.urls import reverse
import stripe
from django import template
from datetime import datetime
# views for listing items
@login_required(login_url='/accounts/login_user')
def rental_item_form(request):

    items_cat = ItemCategory.objects.all()
    # print(items_categories)
    if request.method == 'POST':
        title = request.POST['title']
        daily = request.POST.get('daily')
        weekly = request.POST.get('weekly')
        monthly = request.POST.get('monthly')
        rental_period = request.POST.get('rentalPeriod')
        market_value = request.POST.get('marketValue')
        quantity = request.POST.get('quantity')
        location = request.POST.get('location')
        description = request.POST.get('profileDescription')
        image = request.FILES.get('image')
        category_id = request.POST.get('ItemCategory')
        category_item = get_object_or_404(ItemCategory, id=category_id)
        print(category_id)

        user = request.user
        rental_item = RentalItem.objects.create(
            title=title,
            daily_price=daily,
            weekly_price=weekly,
            monthly_price=monthly,
            rental_period=rental_period,
            market_value=market_value,
            quantity=quantity,
            location=location,
            description=description,
            image=image,
            user=user,
            Category_of_items=category_item,
        )
        return redirect('Category')
    print("user items: ", request.user.RENTAL_ITEM.all())
    return render(request, 'items/list_an_item.html' , {'items_categories': items_cat})


 # views for category of items
def Category (request):
    items_cate= ItemCategory.objects.all()
    return render(request,'search_pages/search.html',{'items_cat':items_cate})




# views for items of category
def test(request, id_cat=None):
    search_query = request.GET.get('q')

    if id_cat:
        Category_of_items = get_object_or_404(ItemCategory, id=id_cat)
        rental_items = RentalItem.objects.filter(Category_of_items_id=id_cat)
        if search_query:
            rental_items = rental_items.filter(title__icontains=search_query)
    elif search_query:
        rental_items = RentalItem.objects.filter(title__icontains=search_query).order_by('id')
    else:
        rental_items = RentalItem.objects.all().order_by('id')

    for item in rental_items:
        comments = Comment.objects.filter(rental_item=item)
        item.average_rating = comments.aggregate(Avg('rating'))['rating__avg']
        item.average_rating = round(item.average_rating, 2) if item.average_rating else None

    paginator = Paginator(rental_items, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    if id_cat:
        context['category'] = Category_of_items

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, "search_pages/search_by_category.html", context)
    else:
        return render(request, "search_pages/search_by_category.html", context)
@login_required(login_url='/accounts/login_user')
def my_item(request):
    user = request.user
    rental_items = RentalItem.objects.filter(user=user)
    
    return render(request, 'items/my_item.html', {'rental_items': rental_items, 'user': user})

#view for  edi items

@login_required(login_url='/accounts/login_user')
def edit_item(request, item_id):
    rental_item = get_object_or_404(RentalItem, pk=item_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        daily_price = request.POST.get('daily_price')
        weekly_price = request.POST.get('weekly_price')
        monthly_price = request.POST.get('monthly_price')
        rental_period = request.POST.get('rental_period')
        market_value = request.POST.get('market_value')
        quantity = request.POST.get('quantity')
        location = request.POST.get('location')
        description = request.POST.get('description')

        rental_item.title = title
        rental_item.daily_price = daily_price
        rental_item.weekly_price = weekly_price
        rental_item.monthly_price = monthly_price
        rental_item.rental_period = rental_period
        rental_item.market_value = market_value
        rental_item.quantity = quantity
        rental_item.location = location
        rental_item.description = description
        rental_item.save()
        return redirect('my_item')
    return render(request, 'items/edit_item.html', {'rental_item': rental_item})



def search_by_list(request):
    user_profile = bio.objects.filter(user=request.user).first()
    rental_items = RentalItem.objects.all() 
    return render(request, "search_pages/search_by_list.html", {'rental_items': rental_items, 'user_profile': user_profile})

def delete_item(request, item_id):
    rental_item = get_object_or_404(RentalItem, id=item_id)
    print(rental_item)
    if request.method == 'POST':
        rental_item.delete()
        return redirect('my_item')
    return redirect('my_item' ,{'rental_item': rental_item})







def navbar(request):
        rental_items = RentalItem.objects.all(user=request.user)
        return render(request,'header.html',rental_items)
# checkout
def checkout(request, category_id, rental_item_id):
    category_instance = get_object_or_404(ItemCategory, id=category_id)
    rental_item_instance = get_object_or_404(RentalItem, id=rental_item_id)
   
    fromDate = datetime.strptime(request.GET.get('fromDate'), '%Y-%m-%d').date() 
    toDate = datetime.strptime(request.GET.get('toDate'), '%Y-%m-%d').date() 
    days = (toDate - fromDate).days    
    print(days)
    rental_item_price = rental_item_instance.daily_price
    print(rental_item_price)
    total_price = days * rental_item_price
    print(total_price)

    if request.method == "POST":
        username = request.POST.get('username')
        last_name = request.POST.get('Last_Name')  
        email = request.POST.get('Email')
        mobile_number = request.POST.get('Mobile_NUmber')  
        address = request.POST.get('address')
        country = request.POST.get('country')
        note_to_lender = request.POST.get('note_to_lender')

        # Fetch your list of products dynamically from the database or elsewhere
        products = [
            {
                "name": rental_item_instance.title,
                "description": rental_item_instance.description,
                "price": total_price * 100,
                "quantity": 1,
            }
        ]

        line_items = []
        for product in products:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": product["price"],
                    "product_data": {
                        "name": product["name"],
                        "description": product["description"],  # Optionally include description
                    },
                },
                "quantity": product["quantity"],
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel")),
            metadata={
                "rental_item_id": rental_item_instance.id,
                "category_id": category_instance.id,
                "username": username,
                "last_name": last_name,
                "email": email,
                "mobile_number": mobile_number,
                "address": address,
                "country": country,
                "note_to_lender": note_to_lender,
            }
        )
        return redirect(checkout_session.url, code=303)

        # Create a new CheckoutInfo object
        checkout_info = CheckoutInfo.objects.create(
            Category_of_items_checkout=category_instance,
            rental_item_checkout=rental_item_instance,
            username=username,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            address=address,
            country=country,
            note_to_lender=note_to_lender
        )

   
    return render(request, 'checkout.html', {'Category_of_items': category_instance,
    'rental_item': rental_item_instance,
    'fromDate': fromDate,
    'toDate': toDate,
    "days":days,
    "total_price":total_price,
       })

def success(request):
    return render(request, "success.html")

def cancel(request):
    return render(request, "cancel.html")