from django.shortcuts import render, redirect
import json
from . import dbutil
from . import textblobanalysis
from . import tokens
from . import data_visualization as dv

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


def visual(request):
    return render(request, 'mysite/visual.html')


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
    context = {'data': y, 'total': len(y['result'])}
    return render(request, 'mysite/csv.html', context)

    # return render(request, 'mysite/csv.html')


def login(request):
    if request.method == 'POST':  # If the form has been submitted...
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        print(emailid)
    else:
        print("not a valid user")

    return redirect(request.POST.get('redir'))


def token003(request):
    if request.method == 'POST':  # If the form has been submitted...
        print('sravan')
        data = request.POST.get('comment')
        print(data)
    else:
        print("error")
        return render(request, 'mysite/visual2.html', {})
    y = dv.visualize(data)
    z=y.process()
    print(json.dumps(z))
    # y = {"tokenization": ["once", "again", "mr.", "costner", "has", "dragged", "out", "a", "movie", "for", "far", "longer", "than", "necessary.", "aside", "from", "the", "terrific", "sea", "rescue", "sequences,", "of", "which", "there", "are", "very", "few", "i", "just", "did", "not", "care", "about", "any", "of", "the", "characters.", "most", "of", "us", "have", "ghosts", "in", "the", "closet,", "and", "costner's", "character", "are", "realized", "early", "on,", "and", "then", "forgotten", "until", "much", "later,", "by", "which", "time", "i", "did", "not", "care.", "the", "character", "we", "should", "really", "care", "about", "is", "a", "very", "cocky,", "overconfident", "ashton", "kutcher.", "the", "problem", "is", "he", "comes", "off", "as", "kid", "who", "thinks", "he's", "better", "than", "anyone", "else", "around", "him", "and", "shows", "no", "signs", "of", "a", "cluttered", "closet.", "his", "only", "obstacle", "appears", "to", "be", "winning", "over", "costner.", "finally", "when", "we", "are", "well", "past", "the", "half", "way", "point", "of", "this", "stinker,", "costner", "tells", "us", "all", "about", "kutcher's", "ghosts.", "we", "are", "told", "why", "kutcher", "is", "driven", "to", "be", "the", "best", "with", "no", "prior", "inkling", "or", "foreshadowing.", "no", "magic", "here,", "it", "was", "all", "i", "could", "do", "to", "keep", "from", "turning", "it", "off", "an", "hour", "in."], "remove_stop_words": ["mr.", "costner", "dragged", "movie", "far", "longer", "necessary.", "aside", "terrific", "sea", "rescue", "sequences,", "not", "care", "characters.", "us", "ghosts", "closet,", "costner's", "character", "realized", "early", "on,", "forgotten", "much", "later,", "time", "not", "care.", "character", "really", "care", "cocky,", "overconfident", "ashton", "kutcher.", "problem", "comes", "kid", "thinks", "he's", "better", "anyone", "else", "around", "shows", "signs", "cluttered", "closet.", "obstacle", "appears", "winning", "costner.", "finally", "well", "past", "half", "way", "point", "stinker,", "costner", "tells", "us", "kutcher's", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkling", "foreshadowing.", "magic", "here,", "could", "keep", "turning", "hour", "in."], "character_casing": ["mr.", "costner", "dragged", "movie", "far", "longer", "necessary.", "aside", "terrific", "sea", "rescue", "sequences,", "not", "care", "characters.", "us", "ghosts", "closet,", "costner's", "character", "realized", "early", "on,", "forgotten", "much", "later,", "time", "not", "care.", "character", "really", "care", "cocky,", "overconfident", "ashton", "kutcher.", "problem", "comes", "kid", "thinks", "he's", "better", "anyone", "else", "around", "shows", "signs", "cluttered", "closet.", "obstacle", "appears", "winning", "costner.", "finally", "well", "past", "half", "way", "point", "stinker,", "costner", "tells", "us", "kutcher's", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkling", "foreshadowing.", "magic", "here,", "could", "keep", "turning", "hour", "in."], "negation": ["mr.", "costner", "dragged", "movie", "far", "longer", "necessary.", "aside", "terrific", "sea", "rescue", "sequences,", "not", "care", "characters.", "us", "ghosts", "closet,", "costner's", "character", "realized", "early", "on,", "forgotten", "much", "later,", "time", "not", "care.", "character", "really", "care", "cocky,", "overconfident", "ashton", "kutcher.", "problem", "comes", "kid", "thinks", "he's", "better", "anyone", "else", "around", "shows", "signs", "cluttered", "closet.", "obstacle", "appears", "winning", "costner.", "finally", "well", "past", "half", "way", "point", "stinker,", "costner", "tells", "us", "kutcher's", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkling", "foreshadowing.", "magic", "here,", "could", "keep", "turning", "hour", "in."], "stemming": {"porter_stemmer_text": ["mr.", "costner", "drag", "movi", "far", "longer", "necessary.", "asid", "terrif", "sea", "rescu", "sequences,", "not", "care", "characters.", "us", "ghost", "closet,", "costner'", "charact", "realiz", "earli", "on,", "forgotten", "much", "later,", "time", "not", "care.", "charact", "realli", "care", "cocky,", "overconfid", "ashton", "kutcher.", "problem", "come", "kid", "think", "he'", "better", "anyon", "els", "around", "show", "sign", "clutter", "closet.", "obstacl", "appear", "win", "costner.", "final", "well", "past", "half", "way", "point", "stinker,", "costner", "tell", "us", "kutcher'", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkl", "foreshadowing.", "magic", "here,", "could", "keep", "turn", "hour", "in."], "snowball_stemmer_text": ["mr.", "costner", "drag", "movi", "far", "longer", "necessary.", "asid", "terrif", "sea", "rescu", "sequences,", "not", "care", "characters.", "us", "ghost", "closet,", "costner", "charact", "realiz", "earli", "on,", "forgotten", "much", "later,", "time", "not", "care.", "charact", "realli", "care", "cocky,", "overconfid", "ashton", "kutcher.", "problem", "come", "kid", "think", "he", "better", "anyon", "els", "around", "show", "sign", "clutter", "closet.", "obstacl", "appear", "win", "costner.", "final", "well", "past", "half", "way", "point", "stinker,", "costner", "tell", "us", "kutcher", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkl", "foreshadowing.", "magic", "here,", "could", "keep", "turn", "hour", "in."], "word_net_lemmatizer_stemmer_text": ["mr.", "costner", "dragged", "movie", "far", "longer", "necessary.", "aside", "terrific", "sea", "rescue", "sequences,", "not", "care", "characters.", "u", "ghost", "closet,", "costner's", "character", "realized", "early", "on,", "forgotten", "much", "later,", "time", "not", "care.", "character", "really", "care", "cocky,", "overconfident", "ashton", "kutcher.", "problem", "come", "kid", "think", "he's", "better", "anyone", "else", "around", "show", "sign", "cluttered", "closet.", "obstacle", "appears", "winning", "costner.", "finally", "well", "past", "half", "way", "point", "stinker,", "costner", "tell", "u", "kutcher's", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkling", "foreshadowing.", "magic", "here,", "could", "keep", "turning", "hour", "in."]}, "pos_tagging": ["mr.", "costner", "dragged", "movie", "far", "longer", "necessary.", "aside", "terrific", "sea", "rescue", "sequences,", "not", "care", "characters.", "u", "ghost", "closet,", "costner's", "character", "realized", "early", "on,", "forgotten", "much", "later,", "time", "not", "care.", "character", "really", "care", "cocky,", "overconfident", "ashton", "kutcher.", "problem", "come", "kid", "think", "he's", "better", "anyone", "else", "around", "show", "sign", "cluttered", "closet.", "obstacle", "appears", "winning", "costner.", "finally", "well", "past", "half", "way", "point", "stinker,", "costner", "tell", "u", "kutcher's", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkling", "foreshadowing.", "magic", "here,", "could", "keep", "turning", "hour", "in."], "analyser": ["mr.", "costner", "dragged", "movie", "far", "longer", "necessary.", "aside", "terrific", "sea", "rescue", "sequences,", "not", "care", "characters.", "u", "ghost", "closet,", "costner's", "character", "realized", "early", "on,", "forgotten", "much", "later,", "time", "not", "care.", "character", "really", "care", "cocky,", "overconfident", "ashton", "kutcher.", "problem", "come", "kid", "think", "he's", "better", "anyone", "else", "around", "show", "sign", "cluttered", "closet.", "obstacle", "appears", "winning", "costner.", "finally", "well", "past", "half", "way", "point", "stinker,", "costner", "tell", "u", "kutcher's", "ghosts.", "told", "kutcher", "driven", "best", "prior", "inkling", "foreshadowing.", "magic", "here,", "could", "keep", "turning", "hour", "in."]}

    context = {'data': z, 'total': len(z)}
    #context={}
    return render(request, 'mysite/visual2.html', context)
