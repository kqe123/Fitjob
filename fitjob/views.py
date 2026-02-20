from django.shortcuts import render

def main(request) :
    return render(request, "fitjob/main.html")

def board(request) :
    return render(request, "fitjob/board.html")
# Create your views here.
