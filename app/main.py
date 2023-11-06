from app import app
from flask import render_template, request, redirect, jsonify
import requests
from faker import Faker
import random
from app.models import db, Songs, Rating
from faker import Faker

USERNAME = ""

@app.route("/")
def index():
    return render_template("index.html",message=" ")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        url = "http://127.0.0.1:5000/api/user"
        form = request.form
        entry = {
            "user_name":form["name"],
            "user_password":form["password"],
        }
        response = requests.post(url, json=entry)
        if response.status_code==200:
            return render_template("index.html",message="Registration Successful, signin to proceed")
        return render_template("index.html",message="User already registered.")
    
@app.route("/signin", methods=["GET","POST"])
def signin():
    if request.method=="POST":
        form = request.form
        name = "%20".join(form["name"].split(" "))
        password = form["password"]
        url = f"http://127.0.0.1:5000/api/user/{name}/{password}"
        response = requests.get(url)
        if response.status_code==200:
            return redirect(f"/user/{name}")
        return render_template("index.html",message="Wrong Credentials. Please try again.")
    
@app.route("/user/<user_name>")
def home(user_name):
    url = f"http://127.0.0.1:5000/api/songs"
    response = requests.get(url).json()
    user_name = "%20".join(user_name.split(" "))
    return render_template("user.html",allSongs=response,user_name=user_name)

@app.route("/update-section")
def musicPlayer():
    song_id = request.args.get('song_id')
    url = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    response = requests.get(url).json()
    return response

@app.route("/user/<user_name>/lyrics")
def lyricist(user_name):
    song_id = request.args.get("song_id")
    time = request.args.get("current_time")
    paused = request.args.get("paused")
    url = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    response = requests.get(url).json()
    lyricsFetcher = f"http://127.0.0.1:5000/api/lyrics?song_id={song_id}"
    lyricsData = requests.get(lyricsFetcher).json()
    f = open(lyricsData["lyrics_path"],"r")
    lines = f.readlines()
    user_name = "%20".join(user_name.split(" "))
    ratingFetcher = f"http://127.0.0.1:5000/api/rating?song_id={song_id}&user_name={user_name}"
    ratingData = requests.get(ratingFetcher)
    if ratingData.status_code==200:
        rating=ratingData.json()["rating"]
        love=ratingData.json()["love"]
    else:
        rating=0
        love=0
    return render_template("readLyrics.html",song_id=song_id,time=time,paused=paused,response=response,lines=lines,rating=rating,love=love,user_name=user_name)

@app.route('/update-song-rating')
def update_rating():
    song_id = request.args.get("song_id")
    rating = request.args.get("rating")
    love = request.args.get("love")
    user_name = request.args.get("user_name")
    print(song_id,rating,user_name,love)

    url = "http://127.0.0.1:5000/api/rating"
    entry = {
        "song_id":song_id,
        "rating":rating,
        "love":love,
        "user_name":user_name,
    }
    response = requests.post(url, json=entry)
    if response.status_code==400:
        response = requests.put(url, json=entry)
        if response.status_code==400:
            return {"message":"Rating May Day"}
    return entry,200

@app.route("/go-back")
def go_back():
    user = request.args.get("user_name")
    return redirect(f"/user/{user}")


@app.route("/songpopulator")
def singer():
    fake = Faker()
    for _ in range(50):
        song = Songs(
            song_name=fake.word(),
            lyrics_id=random.randint(1, 100),
            duration=random.randint(1, 300),
            creator_id=random.randint(1, 100),
            artist_id=random.randint(1, 100),
            playlist_in=random.randint(1, 100),
            album_in=random.randint(1, 100),
            date_created=fake.word(),
        )
        db.session.add(song)
    db.session.commit()

if __name__=="__main__":
    app.run(debug=True)