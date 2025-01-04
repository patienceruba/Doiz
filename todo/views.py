from django.shortcuts import render, redirect,get_object_or_404
from .models import  RecordRow,  TaskDone, PDFDocument
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your views here.
@login_required
@user_passes_test(lambda user: user.is_staff)
def home(request):
	task = RecordRow.objects.all()
	context = {"task":task}
	return render(request, "todo/index.html", context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def addRecord(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date_str = request.POST.get('starting-date')
        end_date_str = request.POST.get('ending-date')
        image_file = request.FILES.get('image')  # File upload handling

        if title and description:
            try:
                # Parse dates with defaults for missing values
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else timezone.now()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

                # If no image is uploaded, handle it (optional default image or None)
                if not image_file:
                    # Set a default image path if necessary (ensure your model supports it)
                    image_file = None  # or "/static/images/default.jpg"

                # Save record
                RecordRow.objects.create(
                    user=request.user,  # Ensure user is authenticated
                    title=title,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    image=image_file
                )
                return redirect("home")  # Redirect on success
            except ValueError:
                error = "Invalid date format. Please use YYYY-MM-DD."
        else:
            error = "Title and description are required."

        # Render the form with an error message
        return render(request, "todo/addrecord.html", {"error": error})

    return render(request, "todo/addrecord.html")




from django.contrib import messages

def deleteRow(request, pk):
    item = get_object_or_404(RecordRow, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "The record was deleted successfully.")
        return redirect("home")  # Replace "home" with the name of the view or URL to redirect to after deletion
    return render(request, "todo/delete.html", {"item": item})


def updateRecord(request, pk):
    record = get_object_or_404(RecordRow, pk=pk)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date_str = request.POST.get('starting-date')
        end_date_str = request.POST.get('ending-date')
        image_file = request.FILES.get('image')

        # Ensure that title and description are provided
        if title and description:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else record.start_date
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else record.end_date

                # Update the record
                record.title = title
                record.description = description
                record.start_date = start_date
                record.end_date = end_date
                record.image=image_file
                record.save()

                messages.success(request, "The record was updated successfully.")
                return redirect("home")  # Redirect to home or any other page after update

            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return render(request, "todo/update.html", {"record": record, "error": "Invalid date format."})

        messages.error(request, "Title and description are required.")
        return render(request, "todo/update.html", {"record": record, "error": "Title and description are required."})

    return render(request, "todo/update.html", {"record": record})



def search(request):
    query = request.GET.get('search', '')  # Get the search query from the GET request
    redirect_from = request.GET.get('redirect', '')  # Check where the search came from
    results = []

    if query:
        # Filter records based on the search query (e.g., search by title or description)
        results = RecordRow.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))  # Case-insensitive search

    # Redirect based on the 'redirect' parameter
    if redirect_from == 'regular':
        return render(request, 'todo/searchforregular.html', {'results': results, 'query': query})
    else:
        return render(request, 'todo/search.html', {'results': results, 'query': query})



def calendar(request):
    # Get all events from the database (filter based on conditions if needed)
    events = RecordRow.objects.all()

    # Pass events data (dates) to the template
    event_dates = [event.start_date.strftime('%Y-%m-%d') for event in events]  # Convert dates to string
    return render(request, "todo/calendar.html", {"event_dates": event_dates})





def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        title = request.POST.get('title')
        pdf_file = request.FILES['pdf']
        
        # Save the PDF file
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_url = fs.url(filename)

        # Save the document info to the database
        PDFDocument.objects.create(title=title, pdf=uploaded_file_url)

        return redirect('pdf_list')
    
    return render(request, 'upload_pdf.html')

def pdf_list(request):
    pdfs = PDFDocument.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})


def event(request):
    content = RecordRow.objects.all()
    context = {"content":content}
    return render(request, "todo/events.html", context)


@login_required
def task_done_view(request):
    # Retrieve all completed tasks for the logged-in user
    image = RecordRow.objects.all()
    task_done_list = TaskDone.objects.filter(user=request.user).order_by('-completed_at')
    context = {
        'task_done_list': task_done_list,"image":image
    }
    return render(request, 'todo/task_done.html', context)


def today_view(request):
    today = timezone.localdate()  # Local date without time
    events_today = RecordRow.objects.filter(start_date__date=today)
    return render(request, 'todo/today.html', {'events_today': events_today})


def dashboard_view(request):
    total_tasks = RecordRow.objects.count()
    tasks_completed = RecordRow.objects.filter(done=True).count()
    #upcoming_events = Task.objects.filter(start_date__gte=timezone.now()).count()  # Assuming tasks have a start date
    #team_members = User.objects.count()  # Adjust if team members are stored differently
    context = {
        'total_tasks': total_tasks,
        'tasks_completed': tasks_completed,
        #'upcoming_events': upcoming_events,
        #'team_members': team_members,
    }
    return render(request, 'todo/dashboard.html', context)
