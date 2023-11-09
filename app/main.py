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
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    return render_template("user.html",allSongs=response,user_name=user_name,playlists=playlistData)

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
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    playlistList = []
    for i in playlistData:
        if song_id in i["song_ids"].split(","):
            playlistList.append(i)
    return render_template("readLyrics.html",song_id=song_id,time=time,paused=paused,response=response,lines=lines,rating=rating,love=love,user_name=user_name,playlists=playlistData,playlistList=playlistList)

@app.route('/update-song-rating')
def update_rating():
    song_id = request.args.get("song_id")
    rating = request.args.get("rating")
    love = request.args.get("love")
    user_name = request.args.get("user_name")
    user_name = "%20".join(user_name.split(" "))
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


@app.route("/user/<user_name>/liked_songs")
def liked_songs(user_name):
    user_name="%20".join(user_name.split(" "))
    likeFetcher = f"http://127.0.0.1:5000/api/rating?user_name={user_name}"
    likeData = requests.get(likeFetcher).json()
    songs = []
    for i in likeData:
        song_id = i["song_id"]
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={song_id}"
        songData = requests.get(songFetcher).json()
        songs.append(songData)
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    return render_template("liked_songs.html",allSongs=songs,user_name=user_name,playlists=playlistData)

@app.route("/user/<user_name>/playlists")
def playlist(user_name):
    user_name="%20".join(user_name.split(" "))
    playlist_id = request.args.get("playlist_id")
    allPlaylistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    allPlaylistData = requests.get(allPlaylistFetcher).json()
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?playlist_id={playlist_id}&user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    song_ids = playlistData["song_ids"]
    songs = []
    if song_ids != "":
        for i in song_ids.split(","):
            songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
            songData = requests.get(songFetcher).json()
            songs.append(songData)
    # print(playlistData["playlist_name"])
    playlistName = "%20".join(playlistData["playlist_name"].split(" "))
    # print(playlistName)
    return render_template("playlist.html",allSongs=songs,user_name=user_name,playlists=allPlaylistData,playlistName=playlistName)

@app.route("/user/<user_name>/add_playlist")
def add_playlist(user_name):
    user_name="%20".join(user_name.split(" "))
    allPlaylistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    allPlaylistData = requests.get(allPlaylistFetcher).json()
    return render_template("add_playlist.html", user_name=user_name,playlists=allPlaylistData)

@app.route('/add-playlist')
def create_playlist():
    playlist_name = request.args.get("playlist_name")
    user_name = request.args.get("user_name")

    url = "http://127.0.0.1:5000/api/playlist"
    entry = {
        "playlist_name":playlist_name,
        "user_name":user_name,
        "song_ids":"",
    }
    user_name = "%20".join(user_name.split(" "))
    playlist_name = "%20".join(playlist_name.split(" "))
    response = requests.post(url, json=entry)
    if response.status_code==400:
        response = requests.put(url, json=entry)
        if response.status_code==400:
            return {"message":"Rating May Day"}
    return entry,200

@app.route("/delete-playlist")
def delete_playlist():
    playlistName = request.args.get("playlist_name")
    user_name = request.args.get("user_name")
    # print(playlistName,user_name)
    url = f"http://127.0.0.1:5000/api/playlist?playlist_name={playlistName}&user_name={user_name}"
    response = requests.delete(url)
    if response.status_code==400:
        return {"message":"Rating May Day"}
    return response,200 

@app.route("/add-song-to-playlist")
def add_song_to_playlist():
    playlist_name = request.args.get("playlist_name")
    user_name = request.args.get("user_name")
    song_id = request.args.get("song_id")
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?playlist_name={playlist_name}&user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    url = "http://127.0.0.1:5000/api/playlist"
    song_ids = playlistData["song_ids"]
    if song_ids=="":
        song_ids+=f"{song_id}"
    elif song_id in song_ids:
        song_ids=song_ids
    else:
        song_ids+=f",{song_id}"
    entry = {
        "playlist_name":playlist_name,
        "user_name":user_name,
        "song_ids":song_ids,
    }
    response = requests.put(url, json=entry)
    if response.status_code==400:
        return {"message":"Rating May Day"}
    return entry,200

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