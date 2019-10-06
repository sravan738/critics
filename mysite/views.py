from django.shortcuts import render, redirect

from . import dbutil
from . import textblobanalysis
from . import tokens

database = "C:\\Users\\sravan\\PycharmProjects\\project1\\db.sqlite3"


def index(request):
    return render(request, 'mysite/home.html')


def index2(request):
    return render(request, 'mysite/header.html')


def index3(request):
    return render(request, 'mysite/login.html')


def thor(request):
    conn = dbutil.create_connection(database)
    cur = conn.cursor()
    cur.execute(
        "SELECT comment,rating,user_name,commented_dat FROM mysite_comment_tbl  where movie_name='Thor' order by commented_dat")

    rows = cur.fetchall()

    for row in rows:
        print(row[0])
    context = {'comment_list': rows}
    return render(request, 'mysite/thor.html', context)


def avengers(request):
    conn = dbutil.create_connection(database)
    cur = conn.cursor()
    cur.execute(
        "SELECT comment,rating,user_name,commented_dat FROM mysite_comment_tbl  where movie_name='Avengers' order by commented_dat")

    rows = cur.fetchall()

    for row in rows:
        print(row[0])
    context = {'comment_list': rows}
    return render(request, 'mysite/avengers.html', context)


def sherlock(request):
    conn = dbutil.create_connection(database)
    cur = conn.cursor()
    cur.execute(
        "SELECT comment,rating,user_name,commented_dat FROM mysite_comment_tbl  where movie_name='Sherlock' order by commented_dat")

    rows = cur.fetchall()

    for row in rows:
        print(row[0])
    context = {'comment_list': rows}
    return render(request, 'mysite/sherlock.html', context)


def lion(request):
    conn = dbutil.create_connection(database)
    cur = conn.cursor()
    cur.execute(
        "SELECT comment,rating,user_name,commented_dat FROM mysite_comment_tbl  where movie_name='Lion' order by commented_dat")

    rows = cur.fetchall()

    for row in rows:
        print(row[0])
    context = {'comment_list': rows}
    return render(request, 'mysite/lion.html', context)


def about(request):
    return render(request, 'mysite/about.html')


def csv(request):
    return render(request, 'mysite/csv.html')


def textfile(request):
    return render(request, 'mysite/textfile.html')


def saveComment(request):
    if request.method == 'POST':  # If the form has been submitted...
        comment = request.POST.get('comment')
        print(comment)
        movie_name = request.POST.get('movie')
        print(movie_name)
        p1 = textblobanalysis.mycomment(request.POST.get('comment'))
        print(p1.showRating())
        result = (p1.showRating() * 10) / 2
        # if result >= 3.0:
        #     rating=5.0
        # elif result >0.0 & result < 3.0:
        #     rating=4.0
        # elif result == 0.0:
        #     rating=3.0
        # elif result<0.0 & result > -3.0:
        #     rating=2.0
        # else:
        #     rating=1.0
        if result > 0.0:
            print("positive")
            if result >= 3.0:
                rating = 5.0
            elif result > 0.0 and result < 3.0:
                rating = 4.0
        elif result < 0.0:

            result = result + 5.0
            print("result3 = ", result)
            if result >= 3.0:
                rating = 2.0
            elif result >= 0.0 and result < 3.0:
                rating = 1.0
        else:
            rating = 3.0

        print("result2 = ", result)
        sql = "insert into mysite_comment_tbl (comment,rating,movie_name,user_name,commented_dat) values ('" + comment + "','" + str(
            rating) + "','" + movie_name + "','sravan',date('now'))"

        conn = dbutil.create_connection(database)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    else:
        print("not a post")

    return redirect(request.POST.get('redir'))


def token001(request):
    if request.method == 'POST' and request.FILES['csvfile']:  # If the form has been submitted...
        # comment = request.POST.get('csvfile')
        comment = request.FILES['csvfile']
        data = []
        # csv_reader = csv.reader(comment)
        for rows in comment:
            data.append(str(rows).split(","))
        y = tokens.normalization(data)
    else:
        print("no file selected")
    context = {'data': y,'total': len(y['result'])}
    return render(request, 'mysite/csv.html', context)

    #return render(request, 'mysite/csv.html')


def login(request):
    if request.method == 'POST':  # If the form has been submitted...
        emailid = request.POST.get('emailid')
        password= request.POST.get('password')
        print(emailid)
    else:
        print("not a valid user")

    return redirect(request.POST.get('redir'))





