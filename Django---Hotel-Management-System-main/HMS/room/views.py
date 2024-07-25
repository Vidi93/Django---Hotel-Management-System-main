# imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.http import HttpRequest

from datetime import datetime, date, timedelta
import random
# Create your views here.
from accounts.models import *
from room.models import *
from hotel.models import *
from .forms import BookingForm
from .models import Room, Booking, RoomServices, Refund
from datetime import datetime
from accounts.models import Guest
from .forms import RoomEditForm



@ login_required(login_url='login')
def rooms(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    rooms = Room.objects.all()
    firstDayStr = None
    lastDateStr = None

    def chech_availability(fd, ed):
        availableRooms = []
        for room in rooms:
            availList = []
            bookingList = Booking.objects.filter(roomNumber=room)
            if room.statusStartDate == None:
                for booking in bookingList:
                    if booking.startDate > ed.date() or booking.endDate < fd.date():
                        availList.append(True)
                    else:
                        availList.append(False)
                if all(availList):
                    availableRooms.append(room)
            else:
                if room.statusStartDate > ed.date() or room.statusEndDate < fd.date():
                    for booking in bookingList:
                        if booking.startDate > ed.date() or booking.endDate < fd.date():
                            availList.append(True)
                        else:
                            availList.append(False)
                        if all(availList):
                            availableRooms.append(room)

        return availableRooms

    if request.method == "POST":
        if "dateFilter" in request.POST:
            firstDayStr = request.POST.get("fd", "")
            lastDateStr = request.POST.get("ld", "")

            firstDay = datetime.strptime(firstDayStr, '%Y-%m-%d')
            lastDate = datetime.strptime(lastDateStr, '%Y-%m-%d')

            rooms = chech_availability(firstDay, lastDate)

        if "filter" in request.POST:
            if (request.POST.get("number") != ""):
                rooms = rooms.filter(
                    number__contains=request.POST.get("number"))

            if (request.POST.get("capacity") != ""):
                rooms = rooms.filter(
                    capacity__gte=request.POST.get("capacity"))

            if (request.POST.get("nob") != ""):
                rooms = rooms.filter(
                    numberOfBeds__gte=request.POST.get("nob"))

            if (request.POST.get("type") != ""):
                rooms = rooms.filter(
                    roomType__contains=request.POST.get("type"))

            if (request.POST.get("price") != ""):
                rooms = rooms.filter(
                    price__lte=request.POST.get("price"))

            context = {
                "role": role,
                "rooms": rooms,
                "number": request.POST.get("number"),
                "capacity": request.POST.get("capacity"),
                "nob": request.POST.get("nob"),
                "price": request.POST.get("price"),
                "type": request.POST.get("type")
            }
            return render(request, path + "rooms.html", context)

    context = {
        "role": role,
        'rooms': rooms,
        'fd': firstDayStr,
        'ld': lastDateStr
    }
    return render(request, path + "rooms.html", context)


@login_required(login_url='login')
def add_room(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    if request.method == "POST":
        guest = None
        if role == 'guest':
            guest = request.user.guest
        elif role == 'manager' or role == 'admin' or role == 'receptionist':
            guest = request.user.employee

        # announcement = Announcement(sender = sender, content = request.POST.get('textid'))
        number = request.POST.get('number')
        capacity = request.POST.get('capacity')
        numberOfBeds = request.POST.get('beds')
        roomType = request.POST.get('type')
        price = request.POST.get('price')
        print(capacity)
        room = Room(number=number, capacity=capacity,
                    numberOfBeds=numberOfBeds, roomType=roomType, price=price)

        room.save()
        return redirect('rooms')

    context = {
        "role": role
    }
    return render(request, path + "add-room.html", context)


@login_required(login_url='login')
def room_profile(request, id):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    tempRoom = Room.objects.get(number=id)
    bookings = Booking.objects.filter(roomNumber=tempRoom)
    guests = Guest.objects.all()
    bookings2 = Booking.objects.all()
    context = {
        "role": role,
        "bookings": bookings,
        "room": tempRoom,
        "guests": guests,
        "bookings2": bookings2
    }

    if request.method == "POST":
        if "lockRoom" in request.POST:
            fd = request.POST.get("bsd")
            ed = request.POST.get("bed")
            fd = datetime.strptime(fd, '%Y-%m-%d')
            ed = datetime.strptime(ed, '%Y-%m-%d')
            check = True
            for b in bookings:
                if b.endDate >= fd.date() and b.startDate <= ed.date():
                    check = False
                    break
            if check:
                tempRoom.statusStartDate = fd
                tempRoom.statusEndDate = ed
                tempRoom.save()
            else:
                messages.error(request, "Ya hay una reserva hecha")
        if "unlockRoom" in request.POST:
            tempRoom.statusStartDate = None
            tempRoom.statusEndDate = None
            tempRoom.save()
        if "deleteRoom" in request.POST:
            check = True
            for b in bookings:
                if b.startDate <= datetime.now().date() or b.endDate >= datetime.now().date():
                    check = False
            if check:
                tempRoom.delete()
                return redirect("rooms")
            else:
                messages.error(request, "Ya hay una reserva hecha")

    return render(request, path + "room-profile.html", context)


@login_required(login_url='login')
def room_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    room = Room.objects.get(number=pk)
    form1 = RoomEditForm(instance=room)

    context = {
        "role": role,
        "room": room,
        "form1": form1
    }

    if request.method == 'POST':
        form1 = RoomEditForm(request.POST, instance=room)
        if form1.is_valid():
            form1.save()
            return redirect("room-profile", id=room.number)
    return render(request, path + "room-edit.html", context)


@ login_required(login_url='login')
def room_services(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    room_services = RoomServices.objects.all()
    context = {
        "role": role,
        "room_services": room_services
    }
    return render(request, path + "room-services.html", context)


@login_required(login_url='login')
def current_room_services(request):
    import datetime

    role = str(request.user.groups.all()[0])
    path = role + "/"

    curGuest = Guest.objects.get(user=request.user)
    curBooking = Booking.objects.filter(guest=curGuest).last()
    if curBooking is not None:
        curRoom = Room.objects.get(number=curBooking.roomNumber.number)
    else:
        context = {
            "role": role,
            "error": "You Don't Have Booking Right Now"
        }
        return render(request, path + "current-room-services.html", context)
    curRoomServices = RoomServices.objects.filter(curBooking=curBooking)

    room_services = RoomServices.objects.all()

    group = Group.objects.get(name='staff')
    users = User.objects.filter(groups=group)
    allEmployees = Employee.objects.filter(user__in=users)
    availableEmployee = list()
    maxTaskNum = 10

    for e in allEmployees:
        counter = 0
        empTasks = Task.objects.filter(employee=e)
        for t in empTasks:
            counter += 1
        if counter < maxTaskNum:
            availableEmployee.append(e)

    context = {
        "role": role,
        "room_services": room_services,
        "curGuest": curGuest,
        "curBooking": curBooking,
        "curRoom": curRoom,
        "curRoomServices": curRoomServices
    }

    if request.method == "POST":
        if "foodReq" in request.POST:
            newServiceReq = RoomServices(
                curBooking=curBooking, price=50.0, room=curRoom,  servicesType='Comida')
            newServiceReq.save()

            chosenEmp = random.choice(availableEmployee)
            lastTask = Task.objects.filter(employee=chosenEmp).last()
            if(lastTask != None):
                newTask = Task(employee=chosenEmp, startTime=lastTask.endTime,
                               endTime=lastTask.endTime+datetime.timedelta(minutes=30), description="Pedido")
            else:
                newTask = Task(employee=chosenEmp, startTime=datetime.datetime.now(),
                               endTime=datetime.datetime.now()+datetime.timedelta(minutes=30), description="Pedido")
            newTask.save()
            return redirect("current-room-services")

        if "cleaningReq" in request.POST:
            newServiceReq = RoomServices(
                curBooking=curBooking, price=0.0, room=curRoom,  servicesType='Limpieza')
            newServiceReq.save()
            chosenEmp = random.choice(availableEmployee)
            lastTask = Task.objects.filter(employee=chosenEmp).last()

            if(lastTask != None):
                newTask = Task(employee=chosenEmp, startTime=lastTask.endTime,
                               endTime=lastTask.endTime+datetime.timedelta(minutes=30), description="Descripcion")
            else:
                newTask = Task(employee=chosenEmp, startTime=datetime.datetime.now(),
                               endTime=datetime.datetime.now()+datetime.timedelta(minutes=30), description="Descripcion")
            newTask.save()
            return redirect("current-room-services")

        if "techReq" in request.POST:
            newServiceReq = RoomServices(
                curBooking=curBooking, price=0.0, room=curRoom,  servicesType='Tecnico')
            newServiceReq.save()
            chosenEmp = random.choice(availableEmployee)
            lastTask = Task.objects.filter(employee=chosenEmp).last()
            if(lastTask != None):
                newTask = Task(employee=chosenEmp, startTime=lastTask.endTime,
                               endTime=lastTask.endTime+datetime.timedelta(minutes=30), description="Descripcion")
            else:
                newTask = Task(employee=chosenEmp, startTime=datetime.datetime.now(),
                               endTime=datetime.datetime.now()+datetime.timedelta(minutes=30), description="Descripcion")
            newTask.save()
            return redirect("current-room-services")

    return render(request, path + "current-room-services.html", context)


@login_required(login_url='login')
def bookings(request):
    import datetime
    role = str(request.user.groups.all()[0])
    path = role + "/"

    bookings = Booking.objects.all()
    # calculating total for every booking:
    totals = {}  # <booking : total>
    for booking in bookings:
        start_date = datetime.datetime.strptime(
            str(booking.startDate), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(booking.endDate), "%Y-%m-%d")
        numberOfDays = abs((end_date-start_date).days)
        # get room peice:
        price = Room.objects.get(number=booking.roomNumber.number).price
        total = price * numberOfDays
        totals[booking] = total

    if request.method == "POST":
        if "filter" in request.POST:
            if (request.POST.get("number") != ""):
                rooms = Room.objects.filter(
                    number__contains=request.POST.get("number"))
                bookings = bookings.filter(
                    roomNumber__in=rooms)

            if (request.POST.get("name") != ""):
                users = User.objects.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests = Guest.objects.filter(user__in=users)
                bookings = bookings.filter(
                    guest__in=guests)

            if (request.POST.get("rez") != ""):
                bookings = bookings.filter(
                    dateOfReservation=request.POST.get("rez"))

            if (request.POST.get("fd") != ""):
                bookings = bookings.filter(
                    startDate__gte=request.POST.get("fd"))

            if (request.POST.get("ed") != ""):
                bookings = bookings.filter(
                    endDate__lte=request.POST.get("ed"))

            context = {
                "role": role,
                'bookings': bookings,
                'totals': totals,
                "name": request.POST.get("name"),
                "number": request.POST.get("number"),
                "rez": request.POST.get("rez"),
                "fd": request.POST.get("fd"),
                "ed": request.POST.get("ed")
            }

            return render(request, path + "bookings.html", context)

    context = {
        "role": role,
        'bookings': bookings,
        'totals': totals
    }
    return render(request, path + "bookings.html", context)


#@login_required(login_url='login')
#def booking_make(request):
 #   print("Booking make view called")
  #  if request.method == 'POST':
   #     print("POST request received")
    #    print(request.POST)
    #else:
     #   print("GET request received")    
    #role = str(request.user.groups.all()[0])
    #path = role + "/"

    #room = Room.objects.get(number=request.POST.get("roomid"))
    #guests = Guest.objects.all()  # we pass this to context
    #names = []
    #if request.method == 'POST':
     #   if request.POST.get("fd") == "" or request.POST.get("ld") == "":
      #      return redirect("rooms")

       # start_date = datetime.strptime(
        #    str(request.POST.get("fd")), "%Y-%m-%d")
        #end_date = datetime.strptime(
         #   str(request.POST.get("ld")), "%Y-%m-%d")
       # numberOfDays = abs((end_date-start_date).days)
        # get room peice:
        #price = room.price
        #total = price * numberOfDays

       # start_date = datetime.strptime(
        #    str(request.POST.get("fd")), "%Y-%m-%d")
        #end_date =datetime.strptime(
         #   str(request.POST.get("ld")), "%Y-%m-%d")
        
        #if start_date > end_date:
         #   messages.info(request, 'Fecha incorrecta')
          #  print('Fecha incorrecta')
           # return redirect('rooms')
        
        #else:
         #   start_date = datetime.strptime(
          #      str(request.POST.get("fd")), "%Y-%m-%d")
           # end_date = datetime.strptime(
            #    str(request.POST.get("ld")), "%Y-%m-%d")
            #numberOfDays = abs((end_date-start_date).days)
            #get room price
           # price = room.price
            #total = price * numberOfDays
            

        #if 'add' in request.POST:  # add dependee
         #   name = request.POST.get("depName")
          #  names.append(name)
           # for i in range(room.capacity-2):
            #    nameid = "name" + str(i+1)
             #   if request.POST.get(nameid) != "":
              #      names.append(request.POST.get(nameid))

        #if 'bookGuestButton' in request.POST:
         #   if "guest" in request.POST:
          #      curguest = Guest.objects.get(id=request.POST.get("guest"))
           # else:
            #    curguest = request.user.guest
            #curbooking = Booking(guest=curguest, roomNumber=room, startDate=request.POST.get(
             #   "fd"), endDate=request.POST.get("ld"))
            #curbooking.save()

           # for i in range(room.capacity-1):
            #    nameid = "name" + str(i+1)
             #   if request.POST.get(nameid) != "":
              #      if request.POST.get(nameid) != None:
               #         d = Dependees(booking=curbooking,
                #                      name=request.POST.get(nameid))
                 #       d.save()
            #return redirect("payment")

    #context = {
     #   "fd": request.POST.get("fd"),
      #  "ld": request.POST.get("ld"),
       # "role": role,
        #"guests": guests,
        #"room": room,
        #"total": total,
        #"names": names
    #}

    #return render(request, path + "booking-make.html", context)##


@login_required(login_url='login')
def booking_make(request):
    if request.method == 'POST':
        room_id = request.POST.get("roomid")
        check_in = request.POST.get("fd")
        check_out = request.POST.get("ld")
        
        if not all([room_id, check_in, check_out]):
            messages.error(request, "Por favor, complete todos los campos.")
            return redirect("rooms")
        
        try:
            room = Room.objects.get(number=room_id)
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            if check_in_date >= check_out_date:
                messages.error(request, "La fecha de salida debe ser posterior a la fecha de entrada.")
                return redirect("rooms")
            
            if not room.is_available(check_in_date, check_out_date):
                messages.error(request, "La habitación no está disponible para las fechas seleccionadas.")
                return redirect("rooms")
            
            guest = Guest.objects.get(custom_user__user=request.user)
            booking = Booking.objects.create(
                guest=guest,
                roomNumber=room,
                startDate=check_in_date,
                endDate=check_out_date
            )
            
            messages.success(request, "Reserva realizada con éxito.")
            return redirect("payment")
        
        except Room.DoesNotExist:
            messages.error(request, "Habitación no encontrada.")
        except ValueError:
            messages.error(request, "Formato de fecha inválido.")
    
    return redirect("rooms")

@login_required(login_url='login')
def deleteBooking(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    booking = Booking.objects.get(id=pk)
    if request.method == "POST":
        booking.delete()
        return redirect('bookings')

    context = {
        "role": role,
        'booking': booking

    }
    return render(request, path + "deleteBooking.html", context)


@ login_required(login_url='login')
def refunds(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    refunds = Refund.objects.all()
    context = {
        "role": role,
        'refunds': refunds
    }

    if request.method == "POST":
        if "decline" in request.POST or "approve" in request.POST:
            refundId = request.POST.get("refund", "")
            guestUserId = request.POST.get("guestUserId", "")

            tempUser = User.objects.get(id=guestUserId)
            receiver = Guest.objects.get(user=tempUser)

            def send(request, receiver, text, subject):

                message_email = 'hms@support.com'
                message = text
                receiver_name = receiver.user.first_name + " " + receiver.user.last_name

                # send email
                send_mail(
                    receiver_name + " " + subject,   # subject
                    message,                          # message
                    message_email,                    # from email
                    [receiver.user.email],                    # to email
                    fail_silently=False,              # for user in users :
                    # user.email
                )

                messages.success(
                    request, 'El email ha sido enviado satisfactoriamente')

                Refund.objects.filter(id=refundId).delete()
                return render(request, path + "refunds.html", context)

            def send_mail_refund_approved(request, receiver):
                subject = "Refund"
                text = """
                    Querido {guestName},
                    Nos complace confirmar que su solicitud de reembolso ha sido aceptada.
                    El importe de reembolso estará en tu cuenta en 24 horas.
                    Este intervalo de tiempo puede variar hasta 48 horas según tu banco.
                    Lamentamos mucho este inconveniente. Esperamos verte pronto.
                """
                email_text = text.format(
                    guestName=receiver.user.first_name + " " + receiver.user.last_name)

                send(request, receiver, email_text, subject)

            def send_mail_refund_declined(request, receiver):
                subject = "Refund"
                text = """
                    Querido {guestName},
                    Lamentamos informarle que su solicitud de reembolso ha sido rechazada.
                    Después de nuestros exámenes, vemos que su solicitud no se puede realizar de a cuerdo
                    con nuestra política del Hotel.
                    Lamentamos mucho este inconveniente. Esperamos verte pronto.
                """
                email_text = text.format(
                    guestName=receiver.user.first_name + " " + receiver.user.last_name)

                send(request, receiver, email_text, subject)

            if "decline" in request.POST:
                send_mail_refund_declined(request, receiver)
            if "approve" in request.POST:
                send_mail_refund_approved(request, receiver)

            refundId = None
            statu = None

        if "filter" in request.POST:
            users = User.objects.all()
            if (request.POST.get("gid") != ""):
                users = users.filter(
                    id__contains=request.POST.get("gid"))
                guests = Guest.objects.filter(user__in=users)
                refunds = refunds.filter(guest__in=guests)

            if (request.POST.get("name") != ""):
                users = users.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests = Guest.objects.filter(user__in=users)
                refunds = refunds.filter(guest__in=guests)

            if (request.POST.get("booking") != ""):
                booking = Booking.objects.get(id=request.POST.get("booking"))
                refunds = refunds.filter(reservation=booking)

            if (request.POST.get("reason") != ""):
                refunds = refunds.filter(
                    reason__contains=request.POST.get("reason"))

            context = {
                "role": role,
                "refunds": refunds,
                "gid": request.POST.get("gid"),
                "name": request.POST.get("name"),
                "booking": request.POST.get("booking"),
                "reason": request.POST.get("reason")
            }
            return render(request, path + "refunds.html", context)

    return render(request, path + "refunds.html", context)


@login_required(login_url='login')
def request_refund(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    curGuest = Guest.objects.get(user=request.user)

    if request.method == "POST":
        if "sendReq" in request.POST:
            reason = request.POST.get("reqExp")
            curBookingId = request.POST.get("bid")
            currentBooking = Booking.objects.get(id=curBookingId)
            temp = Refund.objects.filter(reservation=currentBooking)
            if not temp:
                currentReq = Refund(
                    guest=curGuest, reservation=currentBooking, reason=reason)
                currentReq.save()
                messages.success(
                    request, "Tu solicitud ha sido enviada.")
            else:
                messages.error(
                    request, "Ya tenemos tu solicitud de devolución para ésta reserva.")

    context = {
        "role": role,
        "curGuest": curGuest,
        "id": request.POST.get("bookingId")
    }

    return render(request, path + "request-refund.html", context)


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(guest=request.user.guest)
    return render(request, 'room/my_bookings.html', {'bookings': bookings})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user.guest)
    return render(request, 'room/booking_confirmation.html', {'booking': booking})