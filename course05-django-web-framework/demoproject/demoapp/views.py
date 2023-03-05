from django.http import HttpResponse 

def home(request):
    # return HttpResponse("Welcome to Little Lemon restaurant!")
    path = request.path
    scheme = request.scheme
    method = request.method
    address = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT")
    path_info = request.path_info

    msg = f"""<br>
    <h1>Path: {path}</h1>
    <h1>Scheme: {scheme}</h1>
    <h1>Method: {method}</h1>
    <h1>Address: {address}</h1>
    <h1>User Agent: {user_agent}</h1>
    <h1>Path Info: {path_info}</h1>
    """ 

    response = HttpResponse(msg, content_type = "text/html", charset = "utf-8")

    return response

    #return HttpResponse(path, content_type = "text/html", charset = "utf-8")

def dishes(request, dish):
    # return HttpResponse(f"Welcome to Little Lemon restaurant! We have {dish} for you!")
    
    items = {
        "pasta": "Pasta is a type of food typically made from an unleavened dough of a durum wheat flour mixed with water or eggs, and formed into sheets or various shapes, then cooked by boiling or baking.",
        "falafel": "Falafel is a deep-fried ball or patty made from ground chickpeas, fava beans, or both. It is a common street food in the Middle East and the Mediterranean.",
        "cheesecake": "Cheesecake is a sweet dessert consisting of one or more layers. The main, and thickest, layer consists of a mixture of soft, fresh cheese, eggs, and sugar; if there is a bottom layer it often consists of a crust or base made from crushed cookies (or digestive biscuits), graham crackers, pastry, or sponge cake.",
    }

    if dish in items:
        msg = f"""<br>
        <h1>{dish}</h1>
        <p>{items[dish]}</p>
        """
    else:
        msg = f"""<br>
        <h1>Sorry, we don't have {dish}.</h1>
        """

    return HttpResponse(msg, content_type = "text/html", charset = "utf-8")

def display_menu_item(request, menu_item):
    return HttpResponse(f"Welcome to Little Lemon restaurant! We have menu item {menu_item} for you!")
