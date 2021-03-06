from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .models import User,RestaurantProfile,DeliveryPersonProfile,CustomerProfile
from FoodItems.models import OrdersDescription,FoodCategory,FoodItemsDescription,FoodNames

def Restaurant_Required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_restaurant,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def Customer_Required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/user/login'):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_customer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
    

def DeliveryPerson_Required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_delivery_person,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def index(request):
    restaurants = RestaurantProfile.objects.all()[:6]
    context={
        'title' : 'FoodEx',
        'restaurants' : restaurants,
    }
    print(len(restaurants))
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('user-submit')=="Sign Up":
            username = request.POST.get('user_login793553')
            name  = request.POST.get('foodbakery_display_name793553')
            email = request.POST.get('foodbakery_user_email793553')
            password = request.POST.get('foodbakery_user_password793553')
            password = make_password(password)
            userObj = User(username=username,email=email,first_name=name,is_customer=True,password=password)
            userObj.save()
        if request.POST.get('user-submit-login'):
            username = request.POST.get('user_login92408')
            password =  request.POST.get('user_pass92408')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/logout/')
    return render(request,'users/index.html',context)

def logout_view(request):
    logout(request)
    return redirect('/')

def registerRestaurant(request):
    context = {
        'title' : 'Register Restaurant',
        'restaurantName' : 'Pizza Home',
        'username' : 'username',
        'useremail' : 'email@gmail.com',
    }
    if request.method == 'POST':
        if request.POST.get('user-submit')=="Sign Up":
            username = request.POST.get('user_login273579')
            name  = request.POST.get('foodbakery_display_name273579')
            email = request.POST.get('foodbakery_user_email273579')
            password = request.POST.get('foodbakery_user_password793553')
            password = make_password(password)
            userObj = User(username=username,email=email,first_name=name,is_customer=True,password=password)
            userObj.save()
            return redirect('index')
        if request.POST.get('next-btn'):
            restaurantName = request.POST.get('foodbakery_restaurant_title')
            restaurantMobile = request.POST.get('foodbakery_restaurant_contact_phone')
            managerName = request.POST.get('foodbakery_restaurant_manager_name')
            managerMobile = request.POST.get('foodbakery_restaurant_manager_phone')
            managerEmail = request.POST.get('foodbakery_restaurant_contact_email')

            country = request.POST.get('foodbakery_post_loc_country_restaurant')
            state = request.POST.get('foodbakery_post_loc_state_restaurant')
            city = request.POST.get('foodbakery_post_loc_city_restaurant')
            address = request.POST.get('trans_address')

            serviceType = request.POST.get('foodbakery_restaurant_pickup_delivery')
            cuisine = request.POST.get('foodbakery_restaurant_category[]')

            username = request.POST.get('foodbakery_restaurant_username')
            email = request.POST.get('foodbakery_restaurant_user_email')
            password = request.POST.get('foodbakery_restaurant_password')
            password2 = request.POST.get('foodbakery_restaurant_password2')
            password = make_password(password)
            # The case that password1 and password2 are not equal has to be checked and handled
            userObj = User(username=username,email=email,first_name=restaurantName,is_restaurant=True,password=password)
            userObj.save()

            restaurantObj = RestaurantProfile(
                user= userObj,
                restaurantName=restaurantName,
                restaurantMobile=restaurantMobile,
                managerName=managerName,
                managerMobile = managerMobile,
                managerEmail = managerEmail,
                address = address,
                country = country,
                state = state,
                city = city,
                serviceType =serviceType,
                cuisine = cuisine,
            )
            restaurantObj.save()


            return render(request,'users/register-user-and-add-restaurant/index2.html',context)
    return render(request,'users/register-user-and-add-restaurant/index.html',context)

def deliveryPersonLogin(request):
    if request.method == 'POST':
        if request.POST.get('login'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_delivery_person:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/deliveryperson/login/')
    return render(request,'users/my-account/index.html')

def deliveryPersonRegister(request):
    if request.method == 'POST':
        if request.POST.get('signup'):
            username = request.POST.get('username')
            fname = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            mobile= request.POST.get('mobile')
            address = request.POST.get('address')
            password = make_password(password)
            user  = User(username=username,email=email,first_name=fname,is_delivery_person=True,password=password)
            user.save()
            deliveryPerson = DeliveryPersonProfile(user=user,mobile=mobile,address=address)
            deliveryPerson.save()
            return redirect('/deliveryperson/login/')

    return render(request,'users/my-account/register.html')

@Customer_Required
def userDashboard(request,pk):
    return render(request,'users/user_dashboard/dashboard.html')

@Customer_Required
def userBookings(request,pk):
    return render(request,'users/user_dashboard/my-bookings.html')

@Customer_Required
def userOrders(request,pk):
    customer = CustomerProfile.objects.filter(pk=pk)
    if len(customer)==1:
        orders= customer[0].ordersdescription_set.all()
        customer=customer[0]
    else:
        orders=None
    print(orders)
    context={
        'customer':customer,
        'orders':orders,
    }
    return render(request,'users/user_dashboard/orders.html',context)

@Customer_Required
def userAccountSetting(request):
    return render(request,'users/user_dashboard/account-settings.html')

def userLogin(request):
    if request.method == 'POST':
        if request.POST.get('login'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET['next'])
            else:
                return redirect('/')  
    return render(request,'users/my-account/index.html')

def userLoginGeneral(request):
    if request.method == 'POST':
        if request.POST.get('login'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/user/login/')  
    return render(request,'users/my-account/index.html')

@Restaurant_Required
def restaurantOrders(request,pk):
    restaurant = get_object_or_404(RestaurantProfile,pk=pk)
    orders = restaurant.ordersdescription_set.all()
    context = {
        'orders' : orders,
        'restaurant' : restaurant
    }
    return render(request,'users/restaurant-dashboard/orders.html',context)

@Restaurant_Required
def restaurantMenuBuilder(request,pk):
    restaurant = RestaurantProfile.objects.filter(pk=pk)
    if restaurant:
        restaurant = restaurant[0]
    if request.method == 'POST':
        if request.POST.get('addCategory'):
            catName = request.POST.get('addCategoryname')
            catDesc = request.POST.get('addCategoryDesc')

            categ = FoodCategory(foodCategories=catName,categoryDescription=catName)
            categ.save()
            restaurant.foodcategory_set.add(categ)

        elif request.POST.get('addFooditem'):
            foodname = request.POST.get('foodtitle')
            foodNameObj = FoodNames.objects.filter(food_name=foodname)
            if len(foodNameObj)>0:
                foodNameObj=foodNameObj[0]
            elif len(foodNameObj)==0:
                foodNameObj= FoodNames(food_name=foodname)
                foodNameObj.save()
            
            foodPrice= request.POST.get('fooditemprice')
            fooditemDescription = request.POST.get('fooditemdescription')
            Foodcategory = request.POST.get('restaurant_menu_adingCateg')
            foodCateg = FoodCategory.objects.filter(foodCategories=Foodcategory,restaurants=restaurant)[0]
            newItem = FoodItemsDescription(
                description=fooditemDescription,
                price = foodPrice,
                restaurant=restaurant,
                food_name=foodNameObj,
                foodCategory=foodCateg
            )
            newItem.save()

        for key,value in request.POST.items():
            if key.startswith('categoryedit-'):
                categpk = key[len('categoryedit-'):]
                categpk=int(categpk)
                print("categ:",categpk)
                categoryFood = FoodCategory.objects.filter(pk=int(categpk))[0]
                print(categoryFood)
                categoryName = request.POST.get('menu_cat_title['+str(categpk)+']')
                categoryDesc = request.POST.get('menu_cat_desc['+str(categpk)+']')

                print(categoryName)
                print(categoryDesc)
                categoryFood.foodCategories=categoryName
                categoryFood.categoryDescription=categoryDesc
                categoryFood.save()

        for key,value in request.POST.items():
            if key.startswith('fooditemedit-'):
                fooditempk = key[len('fooditemedit-'):]
                print("fooditempk: " , fooditempk)
                fooditemObj = FoodItemsDescription.objects.filter(pk=int(fooditempk))[0]

                fooddesc = request.POST.get('menu_item_desc['+ fooditempk +']')
                foodprice = request.POST.get('menu_item_price['+ fooditempk +']')
                print("previousPrice:", foodprice,":::",fooditemObj.price)
                foodname = request.POST.get('menu_item_action['+ fooditempk +']')
                foodcateg = request.POST.get('restaurant_menu['+ fooditempk +']')
                categoryFood = FoodCategory.objects.filter(foodCategories=foodcateg,restaurants=restaurant)[0]
                fooditemObj.description =fooddesc
                fooditemObj.price = foodprice
                print("previousPrice:", foodprice,":::",fooditemObj.price)
                fooditemObj.food_name.food_name= foodname
                fooditemObj.foodCategory = categoryFood
                fooditemObj.save()

    # restaurant = RestaurantProfile.objects.filter(pk=pk)
    # if restaurant:
    #     restaurant = restaurant[0]
    categories = restaurant.foodcategory_set.all()
    foodItems = {}
    for category in categories:
        foods = category.fooditemsdescription_set.filter(restaurant=restaurant)
        foodItems[category]=foods
    
    context={
        'restaurant':restaurant,
        'categories':categories,
        'foodItems':foodItems
    }
    return render(request,'users/restaurant-dashboard/menubuilder.html',context)

@DeliveryPerson_Required
def deliveryPersonOrders(request,pk):
    deliveryPerson = get_object_or_404(DeliveryPersonProfile,pk=pk)
    orders = deliveryPerson.ordersdescription_set.all()
    context = {
        'orders' : orders,
        'deliveryPerson' : deliveryPerson
    }
    return render(request,'users/delivery-dashboard/orders.html',context)
