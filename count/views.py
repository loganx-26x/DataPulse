from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from count.models import Company
from .serilizers import CompanySerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import os
import csv

# Create your views here.


def user_register(request):
    data = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if username == "" or password == "" or password2 == "":
            data["error_msg"] = "Fields cant be empty"
        elif password != password2:
            data["error_msg"] = "Password Does not matched"
        elif User.objects.filter(username=username).exists():
            data["error_msg"] = username + " already exist"
        else:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            return redirect("/login")
    return render(request, "register.html", context=data)


def user_login(request):
    data = {}
    if request.method == "POST":
        uname = request.POST["username"]
        upass = request.POST["password"]
        if uname == "" or upass == "":
            data["error_msg"] = "Fields cant be empty"
        elif not User.objects.filter(username=uname).exists():
            data["error_msg"] = uname + " user does not exist"
        else:
            user = authenticate(username=uname, password=upass)
            if user is None:
                data["error_msg"] = "Wrong password"
            else:
                login(request, user)
                if user.is_superuser:
                    return redirect("/admin")
                else:
                    return redirect("/")
    return render(request, "login.html", context=data)


def user_logout(request):
    logout(request)
    return redirect("/login")


def query_builder(request):
    industries = [
        "Information",
        "Military",
        "Accounting",
        "Automotive",
        "Computer",
        "Telecommunications",
        "Defense Space",
        "Financial Services",
        "Banking",
        "Internet",
        "Consumer Electronics",
        "Management Consulting",
        "Electrical/Electronic Manufacturing",
        "Information Technology and Services",
        "Hospital & Health Care",
        "Food & Beverages",
        "Computer Networking",
        "Semiconductors",
        "Oil & Energy",
        "Transportation",
        "Public Policy",
        "Government Administration",
        "Pharmaceuticals",
        "Education Management",
        "Photography",
        "Insurance",
        "Logistics and Supply Chain",
        "Restaurants",
        "Retail",
        "Real Estate",
        "Design",
        "Aviation & Aerospace",
        "Computer Software",
    ]

    cities = [
        "New York",
        "Bombay",
        "Dublin",
        "Alexandria",
        "London",
        "Palo Alto",
        "Teaneck",
        "Withee",
        "Redmond",
        "Dallas",
        "Randolph",
        "San Francisco",
        "Bangalore",
        "Charlotte",
        "Washington",
        "Seattle",
        "Cupertino",
        "Munich",
        "Redwood Shores",
        "Espoo",
        "Paris",
        "Mountain View",
        "Oak Brook",
        "Kista",
        "Chicago",
        "Berks",
        "Oakland",
        "Dearborn",
        "Santa Clara",
        "San Jose",
        "Detroit",
        "Purchase",
        "Minneapolis",
        "The Hague",
        "Noida",
        "Atlanta",
        "Vevey",
        "Shenzhen",
        "Round Rock",
        "Hayes",
        "Morristown",
        "Houston",
        "Bethesda",
    ]

    states = [
        "California",
        "Maharashtra",
        "New Jersey",
        "Virginia",
        "Greater London",
        "Texas",
        "Washington",
        "District of Columbia",
        "Bavaria",
        "Uusimaa",
        "Île-de-France",
        "Stockholm",
        "Ontario",
        "Connecticut",
        "Switzerland",
        "Karnataka",
        "Germany",
        "North Carolina",
        "Kentucky",
        "Illinois",
        "Georgia",
        "Quebec",
        "Madrid",
        "Bayern",
        "Pennsylvania",
        "Kansas",
        "Eastern Province",
        "West Sussex",
        "Victoria",
        "Rhode Island",
        "Buckinghamshire",
        "New York",
        "Northbrook",
        "Brazil",
        "Hessen",
        "Italy",
        "South Carolina",
        "Sweden",
        "Turkey",
        "Missouri",
    ]

    countries = [
        "United States",
        "India",
        "Ireland",
        "United Kingdom",
        "Sweden",
        "Finland",
        "France",
        "Germany",
        "Canada",
        "Italy",
        "Spain",
        "South Korea",
        "Australia",
        "Saudi Arabia",
        "Netherlands",
        "Czechia",
        "United Arab Emirates",
        "Turkey",
        "Brazil",
        "Switzerland",
        "Mexico",
        "Japan",
        "China",
        "Denmark",
        "Norway",
        "Belgium",
        "Portugal",
        "Poland",
        "Singapore",
        "Malaysia",
        "Thailand",
        "Vietnam",
        "Philippines",
        "New Zealand",
        "Argentina",
        "Chile",
        "Colombia",
        "Peru",
        "Egypt",
        "Morocco",
        "South Africa",
        "Nigeria",
        "Kenya",
        "Ethiopia",
        "Ghana",
        "Uganda",
        "Cameroon",
        "Ivory Coast",
        "Senegal",
        "Angola",
        "Tanzania",
        "Madagascar",
        "Papua New Guinea",
        "Fiji",
        "Solomon Islands",
        "Samoa",
        "Tonga",
        "Vanuatu",
        "Kiribati",
        "Marshall Islands",
        "Micronesia",
        "Palau",
        "Nauru",
        "Tuvalu",
        "Antigua and Barbuda",
        "Bahamas",
        "Barbados",
        "Belize",
        "Costa Rica",
        "Cuba",
        "Dominica",
        "Dominican Republic",
        "El Salvador",
        "Grenada",
        "Guatemala",
        "Haiti",
        "Honduras",
        "Jamaica",
        "Nicaragua",
        "Panama",
        "Saint Kitts and Nevis",
        "Saint Lucia",
        "Saint Vincent and the Grenadines",
        "Trinidad and Tobago",
    ]

    return render(
        request,
        "query.html",
        {
            "industries": industries,
            "cities": cities,
            "states": states,
            "countries": countries,
        },
    )


@api_view(["GET"])
@csrf_exempt
def return_result(request):
    keyword = request.GET.get("keyword")
    industry = request.GET.get("industry")
    year = request.GET.get("year")
    city = request.GET.get("city")
    state = request.GET.get("state")
    country = request.GET.get("country")
    employees_from = request.GET.get("employeeMin")
    employees_to = request.GET.get("employeeMax")
    companies = Company.objects.all()
    if keyword:
        companies = companies.filter(name__icontains=keyword)
    if industry:
        companies = companies.filter(industry__icontains=industry)
    if year:
        companies = companies.filter(year=year)
    if city:
        companies = companies.filter(city__icontains=city)
    if state:
        companies = companies.filter(state__icontains=state)
    if country:
        companies = companies.filter(country__icontains=country)
    if employees_from:
        companies = companies.filter(current_employee_estimate__gte=employees_from)
    if employees_to:
        companies = companies.filter(total_employee_estimate__lte=employees_to)
    serializers = CompanySerializer(companies, many=True)
    print(len(serializers.data))
    return JsonResponse({"data": len(serializers.data)})


def all_users(request):
    data = {}
    users = User.objects.all()
    data["users"] = users
    return render(request, "user.html", context=data)


def upload(request):
    if request.method == "POST" and request.FILES["file"]:
        file = request.FILES["file"]
        if not file.name.endswith(".csv"):
            return HttpResponse("<h1> Only Csv files are allowed")
        upload_dir = "../files"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        destination = os.path.join(upload_dir, file.name)
        with open(destination, "wb+") as destination_file:
            for chunk in file.chunks():
                destination_file.write(chunk)
        with open(destination, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                locality = row.get("locality", "")
                if locality:
                    city_state = locality.split(",")[:2]
                    city = city_state[0].strip() if len(city_state) > 0 else ""
                    state = city_state[1].strip() if len(city_state) > 1 else ""
                else:
                    city = ""
                    state = ""
                try:
                    year_founded = int(float(row.get("year founded", 0)))
                except ValueError:
                    year_founded = 2000
                Company.objects.create(
                    user=request.user,
                    name=row.get("name", "Unknown"),
                    domain=row.get("domain", "Unknown"),
                    year=year_founded,
                    industry=row.get("industry", "UNKNOWN"),
                    size_range=row.get("size range", "Unknown"),
                    city=city,
                    state=state,
                    country=row.get("country", "Unknown"),
                    linkedin_url=row.get("linkedin url", "Unknown"),
                    current_employee_estimate=row.get("current employee estimate"),
                    total_employee_estimate=row.get("total employee estimate"),
                )
        os.remove(destination)
        return redirect("/")


def home(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    return render(request, "home.html")
