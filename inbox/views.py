from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import MyUser
from inbox.models import Chat 
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
import re
import json
from django.core import serializers
import datetime
from django.utils import timezone
# -----------------Channel Layer--------------------------------#
from channels.layers import get_channel_layer
# importing asysn to sync to convert channels group methods async to sync
from asgiref.sync import async_to_sync

# Create your views here.
def flat_list(mylist):
    """
    This function takes a multi-dimensional list and returns a single-dimensional list.

    Parameters:
    mylist (list): The input list that may contain sub-lists.

    Returns:
    list: A single-dimensional list containing the elements from the input list, including any nested sub-lists.
    """
    flat = []
    for i in mylist:
        if type(i) == list:                           # if i is a list
            flat.extend(flat_list(i))   
        else:
            flat.append(i)
    return flat



@login_required(login_url='/accounts/login_user')
def messages(request):
    try:
        current_user_id = request.user.id
        usr = MyUser.objects.get(id=current_user_id)
        chats = Chat.objects.filter(Q(sender=usr) | Q(reciever=usr))
        user_ids = set()

        for chat in chats:
            thread_ids = re.split('chats|-', chat.thread_name)
            user_ids.update(thread_ids)

        user_ids.discard(str(current_user_id))
        user_ids.discard('')

        chat_users = []
        for user_id in user_ids:
            ch_user = MyUser.objects.get(id=user_id)
            chat_messages = Chat.objects.filter(Q(reciever=ch_user, sender=request.user) | Q(sender=ch_user, reciever=request.user))
            last_message_obj = chat_messages.last()

            msg = last_message_obj.message[:20] if last_message_obj else ""
            msg_time = last_message_obj.timestamp if last_message_obj else None
            thread_name = f'chats{max(user_id, str(current_user_id))}-{min(user_id, str(current_user_id))}'
            unread_msg_count = Chat.objects.filter(thread_name=thread_name, reciever=request.user, is_seen=False).count()

            chat_users.append({
                'id': ch_user.id,
                'name': ch_user.name,
                'profile_img': ch_user.profile_img,
                'message': msg,
                'time': msg_time,
                'unread_messages': unread_msg_count
            })

        search_query = request.GET.get('search_input')
        if search_query:
            chat_users = [user for user in chat_users if search_query.lower() in user['name'].lower()]

        context = {
            'chat_users': chat_users,
        }
        return render(request, 'messages.html', context)

    except Exception as e:
        print(e)
        return render(request, 'messages.html')

# Chat to User Page 
@login_required(login_url='/accounts/login_user')
def chat_to_user(request, id):
    """
    This function is responsible for rendering the chat_to_user.html template with the necessary data.
    It retrieves the current user's id, their profile, and a list of users they have chats with.
    It then filters the list of users to include only the user with the given id, and retrieves their profile.
    It also retrieves all chat messages between the current user and the selected user, and marks them as read.
    Finally, it counts the number of unread messages and passes all the necessary data to the template.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param id: The id of the user to chat with.
    :type id: int
    :return: Renders the chat_to_user.html template with the necessary data.
    :rtype: HttpResponse
    """
    curren_user_id = request.user.id  # getting id of user
    usr = MyUser.objects.get(id=curren_user_id)
    ch = Chat.objects.filter(Q(sender=usr) | Q(reciever=usr))

    # Initializes an empty list to store user IDs involved in chats.
    ids = []

    for chat in ch:  # Loops through each chat in the filtered chat list, splits the thread_name on 'chats' and '-', and appends the resulting list to ids.
        ids.append(re.split('chats|-', chat.thread_name))
    ids = flat_list(ids)
    ids = list(dict.fromkeys(ids))
    if ids:
        print(True)
        ids.remove(str(curren_user_id))
    if '' in ids:
        ids.remove('')
    chat_users = []
    ids = [int(x) for x in ids]
    if ids:

        for i in ids:

            ch_user = MyUser.objects.get(id=i)
            chat_messages = Chat.objects.filter(Q(reciever=ch_user, sender=request.user) | Q(
                sender=ch_user, reciever=request.user))

            last_message_obj = chat_messages.last()
            msg = last_message_obj.message[:20]
            msg_time = last_message_obj.timestamp
            print(msg_time)

            # unread messages count
            if i > request.user.id:
                thread_name = f'chats{i}-{request.user.id}'
            else:
                thread_name = f'chats{request.user.id}-{i}'

            unread_msg = Chat.objects.filter(
                thread_name=thread_name, reciever=request.user, is_seen=False).count()

            chat_users_dict = {'id': ch_user.id, 'name': ch_user.name, 'profile_img': ch_user.profile_img,
                               'message': msg, 'time': msg_time, 'unread_messages': unread_msg}
            chat_users.append(chat_users_dict)

    # curent reciever
    print(ids)
    c_reciever = MyUser.objects.get(id=id)
    if id > curren_user_id:
        thread_name = f'chats{id}-{curren_user_id}'
    else:
        thread_name = f'chats{curren_user_id}-{id}'

    # Read All Unread Messages
    read_messages = Chat.objects.filter(
        thread_name=thread_name, reciever=request.user, is_seen=False)

    for chat in read_messages:
        chat.is_seen = True
        chat.save()

    # Read All Messages
    unread_msg = Chat.objects.filter(
        thread_name=thread_name, reciever=request.user, is_seen=False).count()

    # Search Bar
    if request.method == 'GET' and request.GET.get('search'):
        q = request.GET.get('search_input')
        print(q)
        for i in chat_users:
            if i['name'] == q:
                print(i)
                chat_users = [i]

    chats = Chat.objects.filter(thread_name=thread_name)
    print(chats)
    context = {
        'group_id': id,
        'chat_users': chat_users,
        'reciever': c_reciever,
        'chats': chats,
    }
    return render(request, 'chat_to_user.html', context)