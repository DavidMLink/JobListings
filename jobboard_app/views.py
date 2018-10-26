from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

"""
.##........#######...######...####.##....##..........##....########..########..######...####..######..########.########.########.
.##.......##.....##.##....##...##..###...##.........##.....##.....##.##.......##....##...##..##....##....##....##.......##.....##
.##.......##.....##.##.........##..####..##........##......##.....##.##.......##.........##..##..........##....##.......##.....##
.##.......##.....##.##...####..##..##.##.##.......##.......########..######...##...####..##...######.....##....######...########.
.##.......##.....##.##....##...##..##..####......##........##...##...##.......##....##...##........##....##....##.......##...##..
.##.......##.....##.##....##...##..##...###.....##.........##....##..##.......##....##...##..##....##....##....##.......##....##.
.########..#######...######...####.##....##....##..........##.....##.########..######...####..######.....##....########.##.....##
"""

def index(request):

    # User.objects.all().delete()
    # Job.objects.all().delete()

    return redirect('/homeTemplate')

# TEMPLATE
def home(request):

    return render(request, "index.html")


# PROCESS
def resetSessions(request):
    print("i made it to reset")
    request.session.clear()
    return redirect("/")

# PROCESS
def register(request):
    print(" i am in register!! yay")

    #<<--------VALIDATIONS-------->>
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        
        print(errors)
        
        print("done with register if")

        # redirect the user back to the form to fix the errors
        return redirect('/homeTemplate')
    else:
        hash_brown = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        # Check for any users, if not make the first user an admin
        print ("Total users are:", User.objects.count())
        if User.objects.count() == 0:
            user = User.objects.create(first_name = request.POST['name'], last_name = request.POST['name'], email = request.POST['email'], password = hash_brown.decode("utf-8"), admin = True)
            print("New Admin Created!")

                #store user id in session
            request.session['id'] = user.id
            request.session['first_name'] = user.first_name

            return redirect('/adminTemplate')
        else:
            user = User.objects.create(first_name = request.POST['name'], last_name = request.POST['name'], email = request.POST['email'], password = hash_brown.decode("utf-8"))
            print("New User Created!")

            #store user id in session
            request.session['id'] = user.id
            request.session['first_name'] = user.first_name

            return redirect('/dashboardTemplate')

# PROCESS
def login(request):

    errors = User.objects.login_validator(request.POST)
    print(errors)

    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        
        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/homeTemplate')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
            print("password match")
            # HAVE A CHECK FOR ADMIN OR USER
            request.session['id'] = user.id
            request.session['first_name']=user.first_name
            return redirect("/dashboardTemplate")
        else:
            print("failed password")
            messages.error(request, "Wrong password")

            return redirect('/homeTemplate')


"""
.########.##....##.########......#######..########....##........#######...######............##....########..########..######..
.##.......###...##.##.....##....##.....##.##..........##.......##.....##.##....##..........##.....##.....##.##.......##....##.
.##.......####..##.##.....##....##.....##.##..........##.......##.....##.##...............##......##.....##.##.......##.......
.######...##.##.##.##.....##....##.....##.######......##.......##.....##.##...####.......##.......########..######...##...####
.##.......##..####.##.....##....##.....##.##..........##.......##.....##.##....##.......##........##...##...##.......##....##.
.##.......##...###.##.....##....##.....##.##..........##.......##.....##.##....##......##.........##....##..##.......##....##.
.########.##....##.########......#######..##..........########..#######...######......##..........##.....##.########..######..
"""










"""
.########.....###.....######..##.....##.########...#######.....###....########..########.
.##.....##...##.##...##....##.##.....##.##.....##.##.....##...##.##...##.....##.##.....##
.##.....##..##...##..##.......##.....##.##.....##.##.....##..##...##..##.....##.##.....##
.##.....##.##.....##..######..#########.########..##.....##.##.....##.########..##.....##
.##.....##.#########.......##.##.....##.##.....##.##.....##.#########.##...##...##.....##
.##.....##.##.....##.##....##.##.....##.##.....##.##.....##.##.....##.##....##..##.....##
.########..##.....##..######..##.....##.########...#######..##.....##.##.....##.########.
"""

# TEMPLATE
def dashboard(request):

    # my_jobs = Saved.objects.filter(user_id = request.session['id'])
    # my_jobs2 = Job.objects.filter(added_by_user= request.session['name'])

    # context = {
    #     "my_jobs" : my_jobs, "my_jobs2":my_jobs2, "jobs" : Job.objects.exclude(added_by_user = request.session['name'])
    # }

    # Checks if signed in or not
    if "id" in request.session:

        context = {
            "jobs": Job.objects.all(),
            "savedjobs": Saved.objects.filter(user_id = request.session['id']),
        }

        return render(request,"dashboard.html", context=context)
    
    else:
        return HttpResponse("You are not signed in!! Your cookie was deleted!")


# what is this doing???????
# PROCESS
def remove(request,id):
    print(" i made it to delete!!!!!!!!")
    print("this is my id: ", id)
    # b = Wish.objects.filter(id = int(id))

    # Wish.objects.raw("delete from wish_list_app_wish where id = "+id)    
    
    job_to_remove = Job.objects.filter(id=id)
    # print(job_to_remove.delete)
   
    job_to_remove.delete()
    print(" -=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-==")
    
    return redirect("/dashboardTemplate")

"""
88     888888 888888 888888     888888 88 88     888888 888888 88""Yb
88     88__   88__     88       88__   88 88       88   88__   88__dP
88  .o 88""   88""     88       88""   88 88  .o   88   88""   88"Yb
88ood8 888888 88       88       88     88 88ood8   88   888888 88  Yb
"""

def sortByProcess(request):
    return redirect("/dashboardTemplate")

def distanceProcess(request):
    return redirect("/dashboardTemplate")

def salaryProcess(request):
    return redirect("/dashboardTemplate")

def jobProcess(request):
    return redirect("/dashboardTemplate")

def locationProcess(request):
    return redirect("/dashboardTemplate")

def companyProcess(request):
    return redirect("/dashboardTemplate")

def experienceProcess(request):
    return redirect("/dashboardTemplate")

"""
888888 88b 88 8888b.       dP"Yb  888888     88     888888 888888 888888     888888 88 88     888888 888888 88""Yb
88__   88Yb88  8I  Yb     dP   Yb 88__       88     88__   88__     88       88__   88 88       88   88__   88__dP
88""   88 Y88  8I  dY     Yb   dP 88""       88  .o 88""   88""     88       88""   88 88  .o   88   88""   88"Yb
888888 88  Y8 8888Y"       YbodP  88         88ood8 888888 88       88       88     88 88ood8   88   888888 88  Yb
"""





"""
 88888  dP"Yb  88""Yb     88""Yb  dP"Yb  .dP"Y8 888888 88 88b 88  dP""b8 .dP"Y8
    88 dP   Yb 88__dP     88__dP dP   Yb `Ybo."   88   88 88Yb88 dP   `" `Ybo."
o.  88 Yb   dP 88""Yb     88-""  Yb   dP o.`Y8b   88   88 88 Y88 Yb  "88 o.`Y8b
"bodP'  YbodP  88oodP     88      YbodP  8bodP'   88   88 88  Y8  YboodP 8bodP'
"""

# PROCESS
def allJobsProcess(request):
    return redirect("/dashboardTemplate") 

# PROCESS
def newestJobsProcess(request):
    return redirect("/dashboardTemplate") 


# PROCESS
def saveJob(request,id):
    print("this is my real job_id: ", id)
    user = User.objects.get(id=request.session["id"])
    print("this is my user: ", user.name)

    job = Job.objects.get(id=id)
    print("this is my job: ", job.id)

    new_job = Saved(job=job, user = user)
    new_job.save()
    print("this is my new job:", new_job)

    return redirect('/dashboardTemplate')


"""
888888 88b 88 8888b.       dP"Yb  888888      88888  dP"Yb  88""Yb     88""Yb  dP"Yb  .dP"Y8 888888 88 88b 88  dP""b8 .dP"Y8
88__   88Yb88  8I  Yb     dP   Yb 88__           88 dP   Yb 88__dP     88__dP dP   Yb `Ybo."   88   88 88Yb88 dP   `" `Ybo."
88""   88 Y88  8I  dY     Yb   dP 88""       o.  88 Yb   dP 88""Yb     88-""  Yb   dP o.`Y8b   88   88 88 Y88 Yb  "88 o.`Y8b
888888 88  Y8 8888Y"       YbodP  88         "bodP'  YbodP  88oodP     88      YbodP  8bodP'   88   88 88  Y8  YboodP 8bodP'
"""




"""
.########.##....##.########......#######..########....########.....###.....######..##.....##.########...#######.....###....########..########.
.##.......###...##.##.....##....##.....##.##..........##.....##...##.##...##....##.##.....##.##.....##.##.....##...##.##...##.....##.##.....##
.##.......####..##.##.....##....##.....##.##..........##.....##..##...##..##.......##.....##.##.....##.##.....##..##...##..##.....##.##.....##
.######...##.##.##.##.....##....##.....##.######......##.....##.##.....##..######..#########.########..##.....##.##.....##.########..##.....##
.##.......##..####.##.....##....##.....##.##..........##.....##.#########.......##.##.....##.##.....##.##.....##.#########.##...##...##.....##
.##.......##...###.##.....##....##.....##.##..........##.....##.##.....##.##....##.##.....##.##.....##.##.....##.##.....##.##....##..##.....##
.########.##....##.########......#######..##..........########..##.....##..######..##.....##.########...#######..##.....##.##.....##.########.
"""













"""
..######.....###....##.....##.########.########...........##..#######..########...######.
.##....##...##.##...##.....##.##.......##.....##..........##.##.....##.##.....##.##....##
.##........##...##..##.....##.##.......##.....##..........##.##.....##.##.....##.##......
..######..##.....##.##.....##.######...##.....##..........##.##.....##.########...######.
.......##.#########..##...##..##.......##.....##....##....##.##.....##.##.....##.......##
.##....##.##.....##...##.##...##.......##.....##....##....##.##.....##.##.....##.##....##
..######..##.....##....###....########.########......######...#######..########...######.
"""

# TEMPLATE
def mySavedJobsTemplate(request):

    context = {
        "jobs": Job.objects.all(),
        "savedjobs": Saved.objects.filter(user_id = request.session['id']),
    }

    return render(request,"mysavedjobs.html", context=context)

# PROCESS
def removeFromSavedListProcess(request,id):
    print(" i made it to RemoveFromSavedlist !!!!!!!!")

    job_to_remove = Saved.objects.get(id=id)
    print("this is the id i'm trying to remove:" ,id)
    job_to_remove.delete()
    print("it's done! it's gone-=-=-=--=-=-==--==--=-=-=--=-=-==--==---=-=-=--=-=-==--==-- koala -")

    return redirect("/dashboardTemplate")

# what is this doing???????
# TEMPLATE
def job(request, id):

    job_row = Job.objects.get(id = id)
    # job_row.added_by_id
    first_name_row = User.objects.get ( id = job_row.added_by_id)
    context = {
        "my_job": Job.objects.get(id = id),
        "Other_Users_On_Job": Saved.objects.filter(job_id= id),
        "first_name_row": first_name_row
    }

    return render(request, "job.html", context=context)

"""
.########.##....##.########......#######..########.....######.....###....##.....##.########.########...........##..#######..########...######.
.##.......###...##.##.....##....##.....##.##..........##....##...##.##...##.....##.##.......##.....##..........##.##.....##.##.....##.##....##
.##.......####..##.##.....##....##.....##.##..........##........##...##..##.....##.##.......##.....##..........##.##.....##.##.....##.##......
.######...##.##.##.##.....##....##.....##.######.......######..##.....##.##.....##.######...##.....##..........##.##.....##.########...######.
.##.......##..####.##.....##....##.....##.##................##.#########..##...##..##.......##.....##....##....##.##.....##.##.....##.......##
.##.......##...###.##.....##....##.....##.##..........##....##.##.....##...##.##...##.......##.....##....##....##.##.....##.##.....##.##....##
.########.##....##.########......#######..##...........######..##.....##....###....########.########......######...#######..########...######.
"""












"""
....###....########..##.....##.####.##....##
...##.##...##.....##.###...###..##..###...##
..##...##..##.....##.####.####..##..####..##
.##.....##.##.....##.##.###.##..##..##.##.##
.#########.##.....##.##.....##..##..##..####
.##.....##.##.....##.##.....##..##..##...###
.##.....##.########..##.....##.####.##....##
"""

# TEMPLATE
def adminTemplate(request):
    return render(request, "admin.html")

# TEMPLATE
def addJobTemplate(request):
    return render(request, "Add_Job.html")

# TEMPLATE
def viewUsersTemplate(request):
    context = {
        
    }
    return render(request, "viewusers.html")

def viewAdminsTemplate(request):
    context = {

    }
    return render(request, "viewusers.html")

# PROCESS
def addJobProcess(request):

    #<<--------VALIDATIONS-------->>
    errors = Job.objects.basic_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        
        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/addJobTemplate')
        
    else:
        new_job = Job(comp_name = request.POST["comp_name"], comp_loc = request.POST["comp_loc"], job_desc = request.POST["job_desc"], job_tech = request.POST["job_tech"], POC_name = request.POST["POC_name"], POC_email = request.POST["POC_email"], 
        added_by = User.objects.get(id=request.session["id"]) )
        
        new_job.save()

        print(" i just created a new job!")
        return redirect("/dashboardTemplate")

"""
.########.##....##.########......#######..########.......###....########..##.....##.####.##....##
.##.......###...##.##.....##....##.....##.##............##.##...##.....##.###...###..##..###...##
.##.......####..##.##.....##....##.....##.##...........##...##..##.....##.####.####..##..####..##
.######...##.##.##.##.....##....##.....##.######......##.....##.##.....##.##.###.##..##..##.##.##
.##.......##..####.##.....##....##.....##.##..........#########.##.....##.##.....##..##..##..####
.##.......##...###.##.....##....##.....##.##..........##.....##.##.....##.##.....##..##..##...###
.########.##....##.########......#######..##..........##.....##.########..##.....##.####.##....##
"""