from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import*
from django.shortcuts import get_object_or_404
from django.db.models import Sum




# Create your views here.

def home(request):
    return render(request,'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return render(request, 'login.html')  
        else:
            messages.error(request, "username or password incorrect!")
            return redirect('login')
        
    return render(request, 'login.html')
        

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')

        # Check for missing fields
        if not all([username, password, confirm_password, email, first_name, last_name]):
            messages.error(request, "All fields are required!")
            return redirect('register')

        # Check for password mismatch
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken!")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken!")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "User registered successfully!")
        return render(request, 'register.html')  

    return render(request, 'register.html')



def logout(request):
    auth.logout(request)
    return redirect('/') 

def sell_page(request):
    return render(request, 'sell_page.html')
    
@login_required
def sell_view(request):
    image_url = request.GET.get('image_url', '')  # Get the image URL from query parameters
    if request.method == 'POST':
        username1 = request.user.username
        card_number = request.POST.get('card_number')
        pin = request.POST.get('pin')
        giftcard_type = request.POST.get('giftcard_type')
        expiry = request.POST.get('expiry')
        giftcard_balance = request.POST.get('giftcard_balance')
        selling_price = request.POST.get('selling_price')

        # Save the form data
        sell_obj = selling_info.objects.create(
            username1=username1,
            card_number=card_number,
            pin=pin,
            giftcard_type=giftcard_type,
            expiry=expiry,
            giftcard_balance=giftcard_balance,
            selling_price=selling_price,
        )
        sell_obj.save()
        return redirect('listings') 

    return render(request, 'sell_view.html', {'image_url': image_url})

@login_required
def listings(request):
    if request.user.is_authenticated:
        listings_obj = selling_info.objects.filter(username1=request.user.username)
        return render(request, 'listings.html', {'listings_obj': listings_obj})
    else:
        return redirect('/')

# Admin View to Manage Gift Cards
# @login_required
# def admin_manage_cards(request):
#     if request.user.is_staff:  # Ensure the user is an admin
#         all_cards = sell_details.objects.all()
#         if request.method == 'POST':
#             card_id = request.POST.get('card_id')
#             new_status = request.POST.get('status')
#             reason = request.POST.get('reason')
#             card = sell_details.objects.get(id=card_id)
#             card.status = new_status
#             card.reason = reason
#             card.save()
#             messages.success(request, "Card status updated successfully!")
#         return render(request, 'admin_manage_cards.html', {'all_cards': all_cards})
#     else:
#         return redirect('home')


def mark_card_as_sold(card_id):
    card = get_object_or_404(selling_info, id=card_id)
    if card.status == 'active':
        card.status = 'sold'
        card.save()
        print(f"Card {card.id} marked as sold.")  # Debugging statement
        return card
    print(f"Card {card.id} was not active, so it wasn't sold.")
    return None


def buy_page(request):
    # Fetch 
    active_gift_cards = selling_info.objects.filter(status='active')

    # Safely calculate the total tracked value for sold gift cards
    total_tracked = (
        selling_info.objects.filter(status='sold')
        .aggregate(total=Sum('selling_price'))['total'] or 0
    )

    return render(request, 'buy_page.html', {
        'gift_cards': active_gift_cards,
        'total_tracked': total_tracked
    })



import traceback  # Import for debugging errors

@login_required
def buy_gift_card(request, card_id):
    card = mark_card_as_sold(card_id)

    if card:
        print(f"✅ Card {card.id} is now sold.")  # Debugging

        try:
            # Save purchase details in PurchasedGiftCard model
            purchase = PurchasedGiftCard.objects.create(
                buyer=request.user,
                card_number=card.card_number,
                pin=card.pin,
                giftcard_type=card.giftcard_type,
                expiry=card.expiry,
                giftcard_balance=card.giftcard_balance,
                selling_price=card.selling_price,
            )

            print(f"✅ Purchase created: {purchase}")  # Debugging
            messages.success(request, f"You purchased {card.giftcard_type} for ₹{card.selling_price}!")
            return redirect('purchase_history')

        except Exception as e:
            print("❌ ERROR: Purchase could not be created")
            print(traceback.format_exc())  # Prints detailed error
            messages.error(request, "An error occurred while processing your purchase.")

    else:
        print("❌ Card could not be sold.")  # Debugging
        messages.error(request, "This gift card could not be sold.")

    return redirect('buy_page')





def payment_page(request, card_id):
    card = get_object_or_404(selling_info, id=card_id, status='active')

    if request.method == 'POST':
        card = mark_card_as_sold(card_id)

        if card:
            return render(request, 'payment_page.html', {'card': card, 'success': True})
   
    return render(request, 'payment_page.html', {'card': card})

def confirm_purchase(request, card_id):
    if request.method == 'POST':
        card = mark_card_as_sold(card_id)

        if card:
            # messages.success(request, f'Gift card {card.card_number} purchased successfully!')
            return redirect('purchase_details', card_id=card.id) 
        else:
            messages.error(request, 'This gift card is no longer available.')

    return redirect('home')

from django.shortcuts import render

@login_required
def purchase_details(request, card_id):
    # Fetch the card details for the purchased card
    card = get_object_or_404(selling_info, id=card_id,)
    return render(request, 'purchase_details.html', {'card': card})

@login_required
def purchase_history(request):
    # Fetch purchases made by the logged-in user
    purchases = PurchasedGiftCard.objects.filter(buyer=request.user)

    print(f"Purchases fetched: {purchases}")  # Debugging statement
    return render(request, 'purchase_history.html', {'purchases': purchases})
