
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from items.models import RentalItem
from .models import Comment
from accounts.models import MyUser
from django.db.models import Avg
from items.models import ItemCategory


@login_required(login_url='/accounts/login_user')
def pdp(request,id_cat,rental_item_id):
    rental_item = get_object_or_404(RentalItem, pk=rental_item_id)
    Category_of_items = get_object_or_404(ItemCategory, id=id_cat)



    if request.method == 'POST':
        comment_content = request.POST.get('comment', '')
        rating = request.POST.get('rate', 5)

        if rating:  # Check if rating is provided
            # Save the comment and rating
            comment = Comment.objects.create(
                user=request.user,
                rental_item=rental_item,                content=comment_content,
                rating=rating
            )
        else:
            # Save the comment without a rating
            comment = Comment.objects.create(
                user=request.user,
                rental_item=rental_item,
                content=comment_content,
            )

        return redirect('pdp', id_cat=id_cat, rental_item_id=rental_item_id)

    comments = Comment.objects.filter(rental_item=rental_item)
    average_rating = comments.aggregate(Avg('rating'))['rating__avg']
    average_rating = round(average_rating, 2) if average_rating else None
    comment_count = comments.count()

    return render(request, 'pdp.html', {'rental_item': rental_item, "comments": comments, 'average_rating': average_rating, "Category_of_items":Category_of_items ,    'comment_count': comment_count })




