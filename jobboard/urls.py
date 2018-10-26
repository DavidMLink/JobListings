"""jobboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from jobboard_app import views

urlpatterns = [
    
    # LOGIN AND REGISTRATION
        path('', views.index),
        path('registerProcess', views.register),
        path('loginProcess', views.login),
        path('homeTemplate', views.home),
    # END OF LOGIN AND REGISTRATION

    # RESET SESSIONS
        path('resetSessions', views.resetSessions),
    # END OF RESET SESSIONS

    #UNKNOWN PROCESSES
        path('DeleteProcess/<id>', views.remove),
    # END OF PROCESSES

    # DASHBOARD ROUTING
    path('dashboardTemplate', views.dashboard),
        # LEFT FILTER
            path('sortByProcess', views.sortByProcess),
            path('distanceProcess', views.distanceProcess),
            path('salaryProcess', views.salaryProcess),
            path('jobProcess', views.jobProcess),
            path('locationProcess', views.locationProcess),
            path('companyProcess', views.companyProcess),
            path('experienceProcess', views.experienceProcess),
        # END OF LEFT FILTER

        # ARTICLE
            path('allJobsProcess', views.allJobsProcess),
            path('newestJobsProcess', views.newestJobsProcess),
            path('saveJobProcess/<id>', views.saveJob),
        # END OF ARTICLE

        # RIGHT ASIDE

        # END OF RIGHT ASIDE

    # END OF DASHBOARD

    # SAVED JOBS
        path('removeFromSavedlistProcess/<id>', views.removeFromSavedListProcess),
        path('mySavedJobsTemplate', views.mySavedJobsTemplate),
    # END OF SAVED JOBS

    # ADMIN
        path('adminTemplate', views.adminTemplate),
        path('addJobProcess', views.addJobProcess),
        path('viewUsersTemplate', views.viewUsersTemplate),
]
