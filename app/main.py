from app import app
from flask import render_template, request, redirect, jsonify
import requests
from faker import Faker
import random
from app.models import db, Songs, Rating
from faker import Faker
from datetime import datetime
import json
from datetime import datetime, timedelta

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
        url = f"http://127.0.0.1:5000/api/user?user_name={name}&user_password={password}"
        response = requests.get(url)
        # print(type(response.json()["user_id"]))
        if response.status_code==200:
            with open("app/static/jsons/userActions.json", 'r') as file:
                data = json.load(file)
            if f"{response.json()['user_id']}" in data:
                reff = data[f"{response.json()['user_id']}"]
                if reff["ban_type"]=="temp ban":
                        if reff["end_date"]!=f"{datetime.now().date()}":
                            return render_template("index.html",message=f"You have been temporarily banned for 30 days. You can access your account on {reff['end_date']}.")
                        else:
                            return redirect(f"/user/{name}")
                else:
                    return render_template("index.html",message=f"You have been permanently banned from Kalp Raag for your improper behaviour. Hope you improve yourself.")

            else:
                return redirect(f"/user/{name}")

        return render_template("index.html",message="Wrong Credentials. Please try again.")
    
@app.route("/user/<user_name>")
def home(user_name):
    url = f"http://127.0.0.1:5000/api/songs"
    response = requests.get(url).json()[::-1]
    
    # #user_name = "%20".join(user_name.split(" "))
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json() if requests.get(playlistFetcher).status_code==200 else []
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json() if requests.get(albumFetcher).status_code==200 else []
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json() 
    # print(userData)
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    if creatorData.status_code==200:
        creator = 1
    else:
        creator = 0

    return render_template("user.html",allSongs=response,user_name=user_name,playlists=playlistData,albums=albumData,creator=creator,user_data=userData)

@app.route("/update-section")
def musicPlayer():
    song_id = request.args.get('song_id')
    url = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    response = requests.get(url).json()
    return response

@app.route("/user/<user_name>/lyrics")
def lyricist(user_name):
    print(user_name)
    song_id = request.args.get("song_id")
    time = request.args.get("current_time")
    paused = request.args.get("paused")
    url = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    response = requests.get(url).json()
    lyricsFetcher = f"http://127.0.0.1:5000/api/lyrics?song_id={song_id}"
    lyricsData = requests.get(lyricsFetcher).json()
    f = open(lyricsData["lyrics_path"],"r")
    lines = f.readlines()
    #user_name = "%20".join(user_name.split(" "))
    ratingFetcher = f"http://127.0.0.1:5000/api/rating?song_id={song_id}&user_name={user_name}"
    ratingData = requests.get(ratingFetcher)
    if ratingData.status_code==200:
        rating=ratingData.json()["rating"]
        love=ratingData.json()["love"]
    else:
        rating=0
        love=0
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    playlistData = requests.get(playlistFetcher)
    playlistList = []
    if playlistData.status_code==200:
        playlistData = playlistData.json()
        for i in playlistData:
            songer_ids = i["song_ids"].split(",") if i["song_ids"].split(",")[0]!="" else []
            if f"{song_id}" in songer_ids:
                playlistList.append(i)
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json()
    albumsIn = []
    albumsInFetcher = f"http://127.0.0.1:5000/api/album"
    albumsInData = requests.get(albumsInFetcher).json()
    for i in albumsInData:
        songer_ids = i["song_ids"].split(",") if i["song_ids"].split(",")[0]!="" else []
        if f"{song_id}" in songer_ids:
            albumsIn.append(i) 
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()

    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0
    return render_template("readLyrics.html",song_id=song_id,time=time,paused=paused,response=response,lines=lines,rating=rating,love=love,user_name=user_name,playlists=playlistData,playlistList=playlistList,albums=albumData,albumsIn=albumsIn,creator=creator,user_data=userData)

@app.route('/update-song-rating')
def update_rating():
    song_id = request.args.get("song_id")
    rating = request.args.get("rating")
    love = request.args.get("love")
    user_name = request.args.get("user_name")
    print(song_id,rating,love,user_name)
    # #user_name = "%20".join(user_name.split(" "))
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
    likeData = requests.get(likeFetcher)
    print(likeData)
    songs = []
    if likeData.status_code==200:
        likeData = likeData.json()
        for i in likeData:
            if i["love"]==1:
                song_id = i["song_id"]
                songFetcher = f"http://127.0.0.1:5000/api/songs?id={song_id}"
                songData = requests.get(songFetcher).json()
                songs.append(songData)
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json()
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0
    return render_template("liked_songs.html",allSongs=songs,user_name=user_name,playlists=playlistData,albums=albumData,creator=creator,user_data=userData)

@app.route("/user/<user_name>/playlists")
def playlist(user_name):
    user_name="%20".join(user_name.split(" "))
    playlist_id = request.args.get("playlist_id")
    allPlaylistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    allPlaylistData = requests.get(allPlaylistFetcher).json()
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?playlist_id={playlist_id}&user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    # song_ids = playlistData["song_ids"]
    song_ids = playlistData["song_ids"].split(",") if playlistData["song_ids"].split(",")[0]!="" else []
    songs = []
    if song_ids != "":
        for i in song_ids:
            songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
            songData = requests.get(songFetcher)
            if songData.status_code==200:
                songs.append(songData.json())
    # print(playlistData["playlist_name"])
    playlistName = "%20".join(playlistData["playlist_name"].split(" "))
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json()
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0
    return render_template("playlist.html",allSongs=songs,user_name=user_name,playlists=allPlaylistData,playlistName=playlistName,playlistId=playlist_id,albums=albumData,creator=creator,user_data=userData)

@app.route("/user/<user_name>/add_playlist")
def add_playlist(user_name):
    user_name="%20".join(user_name.split(" "))
    allPlaylistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    allPlaylistData = requests.get(allPlaylistFetcher).json()
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json()
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0
    return render_template("add_playlist.html", user_name=user_name,playlists=allPlaylistData,albums=albumData,creator=creator,user_data=userData)

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
    #user_name = "%20".join(user_name.split(" "))
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
    # song_ids = playlistData["song_ids"]
    song_ids = playlistData["song_ids"].split(",") if playlistData["song_ids"].split(",")[0]!="" else []
    song_ids.append(f"{song_id}")
    # if song_ids=="":
    #     song_ids+=f"{song_id}"
    # elif song_id in song_ids:
    #     song_ids=song_ids
    # else:
    #     song_ids+=f",{song_id}"
    entry = {
        "playlist_name":playlist_name,
        "user_name":user_name,
        "song_ids":",".join(song_ids),
    }
    response = requests.put(url, json=entry)
    if response.status_code==400:
        return {"message":"Rating May Day"}
    return entry,200

@app.route("/delete-song-from-playlist")
def delete_song_from_playlist():
    playlist_name = request.args.get("playlist_name")
    user_name = request.args.get("user_name")
    song_id = request.args.get("song_id")
    print(playlist_name,user_name,song_id)
    playlistFetcher = f"http://127.0.0.1:5000/api/playlist?playlist_name={playlist_name}&user_name={user_name}"
    playlistData = requests.get(playlistFetcher).json()
    url = "http://127.0.0.1:5000/api/playlist"
    # song_ids = playlistData["song_ids"].split(",")
    song_ids = playlistData["song_ids"].split(",") if playlistData["song_ids"].split(",")[0]!="" else []
    if str(song_id) in song_ids:
        song_ids.remove(song_id)
    song_ids = ",".join(song_ids)
    entry = {
        "playlist_name":playlist_name,
        "user_name":user_name,
        "song_ids":song_ids,
    }
    response = requests.put(url, json=entry)
    if response.status_code==400:
        return {"message":"Rating May Day"}
    return entry,200

@app.route("/user/<user_name>/album")
def album(user_name):
    # user_name="%20".join(user_name.split(" "))
    album_id = request.args.get("album_id")
    allPlaylistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    allPlaylistData = requests.get(allPlaylistFetcher).json()
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json()
    allAlbumFetcher = f"http://127.0.0.1:5000/api/album?album_id={album_id}"
    allAlbumData = requests.get(allAlbumFetcher).json()
    saved_by = allAlbumData["saved_by"].split(",")
    saved = 0
    if user_name in saved_by:
        saved=1

    song_ids = allAlbumData["song_ids"].split(",") if allAlbumData["song_ids"].split(",")[0]!="" else []
    songs = []
    # if song_ids != "":
    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            songs.append(songData.json())
    # print(songs)
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0
    return render_template("album.html",albums=albumData,playlists=allPlaylistData,user_name=user_name,albumData=allAlbumData,allSongs=songs,saved=saved,creator=creator,user_data=userData)

@app.route("/save-album")
def save_album():
    user_name = request.args.get("user_name")
    album_name = request.args.get("album_name")
    status = int(request.args.get("status"))
    albumFetcher = f"http://127.0.0.1:5000/api/album?album_name={album_name}"
    albumData = requests.get(albumFetcher).json()
    url = f"http://127.0.0.1:5000/api/album?album_id={albumData['album_id']}"
    # print(status)
    # print(albumData)
    if status==1:
        # print(albumData["saved_by"])
        saved_by = albumData["saved_by"].split(",")
        # print(saved_by)
        if user_name not in saved_by:
            saved_by.append(user_name)
        # print(saved_by)
        entry = {
            "album_id": albumData["album_id"],
            "album_name": albumData["album_name"],
            "genre": albumData["genre"],
            "artist_id": albumData["artist_id"],
            "creator_id": albumData["creator_id"],
            "date_created": albumData["date_created"],
            "song_ids": albumData["song_ids"],
            "saved_by": ",".join(saved_by),
        }
    else:
        saved_by = albumData["saved_by"].split(",")
        if user_name in saved_by:
            saved_by.remove(user_name)
        entry = {
            "album_id": albumData["album_id"],
            "album_name": albumData["album_name"],
            "genre": albumData["genre"],
            "artist_id": albumData["artist_id"],
            "creator_id": albumData["creator_id"],
            "date_created": albumData["date_created"],
            "song_ids": albumData["song_ids"],
            "saved_by": ",".join(saved_by),
        }
    response = requests.put(url, json=entry)
    if response.status_code==400:
        return {"message":"Rating May Day"}
    return entry,200

@app.route("/unlike-song")
def unlike_song():
    user_name = request.args.get("user_name")
    song_id = request.args.get("song_id")
    # user_name="%20".join(user_name.split(" "))
    likeFetcher = f"http://127.0.0.1:5000/api/rating?user_name={user_name}&song_id={song_id}"
    likeData = requests.get(likeFetcher).json()
    url = "http://127.0.0.1:5000/api/rating"
    entry = {
        "song_id": song_id,
        "rating": likeData["rating"],
        "love": 0,
        "user_name": user_name
    }
    response = requests.put(url, json=entry)
    if response.status_code==400:
        return {"message":"Rating May Day"}
    return entry,200

@app.route("/user/<user_name>/search")
def searcher(user_name):

    allPlaylistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    allPlaylistData = requests.get(allPlaylistFetcher).json()
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json()

    key = request.args.get("key")
    filterVal = request.args.get("filter")
    print(key,filterVal)
    fetchSearchData = []
    fetchAlbumData = []
    if filterVal=="Song":
        if key.lower()=="$all":
            fetchSearch = f"http://127.0.0.1:5000/api/songs"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchSearchData=searchData.json()
        else:
            fetchSearch = f"http://127.0.0.1:5000/api/songs?key={key}&filter={filterVal}"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchSearchData=searchData.json()

    elif filterVal=="Album":
        if key.lower()=="$all":
            fetchSearch = f"http://127.0.0.1:5000/api/album"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchAlbumData=searchData.json()
        else:
            fetchSearch = f"http://127.0.0.1:5000/api/album?key={key}&filter={filterVal}"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchAlbumData=searchData.json()

    elif filterVal=="Rating":
        fetchSearch = f"http://127.0.0.1:5000/api/rating?rating={int(key)}&user_name={user_name}"
        searchData = requests.get(fetchSearch)
        songs=searchData.json()
        # print(songs)
        if searchData.status_code!=400:
            for i in songs:
                songFetcher = f"http://127.0.0.1:5000/api/songs?id={i['song_id']}"
                songData = requests.get(songFetcher).json()
                fetchSearchData.append(songData)
    
    elif filterVal=="Genre":
        fetchSearch = f"http://127.0.0.1:5000/api/album?genre={key}"
        searchData = requests.get(fetchSearch)
        if searchData.status_code!=400:
            fetchAlbumData=searchData.json()
    
    elif filterVal=="Artist":
        fetchSearch = f"http://127.0.0.1:5000/api/album?artist_id={key}"
        searchData = requests.get(fetchSearch)
        if searchData.status_code!=400:
            fetchAlbumData=searchData.json()
    
    elif filterVal=="All":
        fetchSearchSong = f"http://127.0.0.1:5000/api/songs?key={key}&filter={filterVal}"
        searchDataSong = requests.get(fetchSearchSong)
        if searchDataSong.status_code!=400:
            fetchSearchData=searchDataSong.json()

        fetchSearchAlbum = f"http://127.0.0.1:5000/api/album?key={key}&filter={filterVal}"
        searchDataAlbum = requests.get(fetchSearchAlbum)
        if searchDataAlbum.status_code!=400:
            fetchAlbumData=searchDataAlbum.json()

        if key in [str(j) for j in range(0,6)]:
            fetchSearchRating = f"http://127.0.0.1:5000/api/rating?rating={int(key)}&user_name={user_name}"
            searchDataRating  = requests.get(fetchSearchRating)
            songs=searchDataRating.json()
            if searchDataRating.status_code!=400:
                for i in songs:
                    songFetcher = f"http://127.0.0.1:5000/api/songs?id={i['song_id']}"
                    songData = requests.get(songFetcher).json()
                    fetchSearchData.append(songData)
        
        fetchSearchGenre = f"http://127.0.0.1:5000/api/album?genre={key}"
        searchDataGenre = requests.get(fetchSearchGenre)
        if searchDataGenre.status_code!=400:
            fetchAlbumData=searchDataGenre.json()

        fetchSearchArtist = f"http://127.0.0.1:5000/api/album?artist_id={key}"
        searchDataArtist = requests.get(fetchSearchArtist)
        if searchDataArtist.status_code!=400:
            fetchAlbumData=searchDataArtist.json()
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0
    return render_template("search.html",albums=albumData,playlists=allPlaylistData,user_name=user_name,fetchSearchData=fetchSearchData,fetchAlbumData=fetchAlbumData,creator=creator,user_data=userData)


@app.route("/creator/<user_name>/search")
def creator_searcher(user_name):

    allPlaylistFetcher = f"http://127.0.0.1:5000/api/playlist?user_name={user_name}"
    allPlaylistData = requests.get(allPlaylistFetcher).json()
    albumFetcher = f"http://127.0.0.1:5000/api/album?saved_by={user_name}"
    albumData = requests.get(albumFetcher).json()

    key = request.args.get("key")
    filterVal = request.args.get("filter")
    print(key,filterVal)
    fetchSearchData = []
    fetchAlbumData = []
    if filterVal=="Song":
        if key.lower()=="$all":
            fetchSearch = f"http://127.0.0.1:5000/api/songs"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchSearchData=searchData.json()
        else:
            fetchSearch = f"http://127.0.0.1:5000/api/songs?key={key}&filter={filterVal}"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchSearchData=searchData.json()

    elif filterVal=="Album":
        if key.lower()=="$all":
            fetchSearch = f"http://127.0.0.1:5000/api/album"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchAlbumData=searchData.json()
        else:
            fetchSearch = f"http://127.0.0.1:5000/api/album?key={key}&filter={filterVal}"
            searchData = requests.get(fetchSearch)
            if searchData.status_code!=400:
                fetchAlbumData=searchData.json()

    elif filterVal=="Rating":
        fetchSearch = f"http://127.0.0.1:5000/api/rating?rating={int(key)}&user_name={user_name}"
        searchData = requests.get(fetchSearch)
        songs=searchData.json()
        # print(songs)
        if searchData.status_code!=400:
            for i in songs:
                songFetcher = f"http://127.0.0.1:5000/api/songs?id={i['song_id']}"
                songData = requests.get(songFetcher).json()
                fetchSearchData.append(songData)
    
    elif filterVal=="Genre":
        fetchSearch = f"http://127.0.0.1:5000/api/album?genre={key}"
        searchData = requests.get(fetchSearch)
        if searchData.status_code!=400:
            fetchAlbumData=searchData.json()
    
    elif filterVal=="Artist":
        fetchSearch = f"http://127.0.0.1:5000/api/album?artist_id={key}"
        searchData = requests.get(fetchSearch)
        if searchData.status_code!=400:
            fetchAlbumData=searchData.json()
    
    elif filterVal=="All":
        fetchSearchSong = f"http://127.0.0.1:5000/api/songs?key={key}&filter={filterVal}"
        searchDataSong = requests.get(fetchSearchSong)
        if searchDataSong.status_code!=400:
            fetchSearchData=searchDataSong.json()

        fetchSearchAlbum = f"http://127.0.0.1:5000/api/album?key={key}&filter={filterVal}"
        searchDataAlbum = requests.get(fetchSearchAlbum)
        if searchDataAlbum.status_code!=400:
            fetchAlbumData=searchDataAlbum.json()

        if key in [str(j) for j in range(0,6)]:
            fetchSearchRating = f"http://127.0.0.1:5000/api/rating?rating={int(key)}&user_name={user_name}"
            searchDataRating  = requests.get(fetchSearchRating)
            songs=searchDataRating.json()
            if searchDataRating.status_code!=400:
                for i in songs:
                    songFetcher = f"http://127.0.0.1:5000/api/songs?id={i['song_id']}"
                    songData = requests.get(songFetcher).json()
                    fetchSearchData.append(songData)
        
        fetchSearchGenre = f"http://127.0.0.1:5000/api/album?genre={key}"
        searchDataGenre = requests.get(fetchSearchGenre)
        if searchDataGenre.status_code!=400:
            fetchAlbumData=searchDataGenre.json()

        fetchSearchArtist = f"http://127.0.0.1:5000/api/album?artist_id={key}"
        searchDataArtist = requests.get(fetchSearchArtist)
        if searchDataArtist.status_code!=400:
            fetchAlbumData=searchDataArtist.json()
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0
    return render_template("search.html",albums=albumData,playlists=allPlaylistData,user_name=user_name,fetchSearchData=fetchSearchData,fetchAlbumData=fetchAlbumData,creator=creator,user_data=userData)


# Creator

@app.route("/creator-register")
def creator_register():
    user_name = request.args.get("user_name")

    return render_template("creator_register.html",user_name=user_name)

@app.route("/creator-save")
def creator_save():
    user_name = request.args.get("user_name")
    creatorPoster = "http://127.0.0.1:5000/api/creator"
    creatorEntry = {
        "user_name":user_name,
        "song_ids":"",
        "album_ids":"",
    }
    creatorResponse = requests.post(creatorPoster, json=creatorEntry)
    url = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    response = requests.get(url)
    if response.status_code==200:
        creator_id = response.json()["creator_id"]
        userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
        userEntry = {
            "creator_id":creator_id
        }
        userResponse = requests.put(userFetcher,json=userEntry)
        if userResponse.status_code==400:
            return {"message":"Rating May Day"}
        return userEntry,200

@app.route("/creator/<user_name>")
def creator_dash(user_name):
    userFetcher = f"http://127.0.0.1:5000/api/user?user_name={user_name}"
    userData = requests.get(userFetcher).json()
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher)
    creator = 1 if creatorData.status_code==200 else 0


    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    with open("app/static/jsons/creatorActions.json", 'r') as file:
        jsonData = json.load(file)
    if f"{creatorData['creator_id']}" in jsonData:
        usx = jsonData[f"{creatorData['creator_id']}"]
        if usx["list_type"]=="black":
            messenger = f"You have been blacklisted. You can no longer upload songs or create albums. All creator powers have been revoked."
            return render_template("creator_ban.html",message=messenger,user_data=userData)
    song_ids = creatorData["song_ids"].split(",") if creatorData["song_ids"].split(",")[0]!="" else []
    album_ids = creatorData["album_ids"].split(",") if creatorData["album_ids"].split(",")[0]!="" else []
    song_count=0
    album_count=0
    total_likes=0
    avg_rating=0
    avg_album=0
    total_rating=0
    count_rating=0
    total_album_saves=0
    count_album_saves=0

    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/rating?song_id={i}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            songData = songData.json()
            for j in songData:
                if j["love"]==1:
                    total_likes+=1
                if j["rating"]>0:
                    total_rating+=j["rating"]
                    count_rating+=1

    for i in album_ids:
        albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={i}"
        albumData = requests.get(albumFetcher)
        if albumData.status_code==200:
            albumData = albumData.json()
            total_album_saves+=len(albumData["saved_by"].split(",")) if albumData["saved_by"]!="" else 0
            count_album_saves+=len(albumData["saved_by"].split(",")) if albumData["saved_by"]!="" else 0
    
    avg_rating = round(total_rating/count_rating,2) if count_rating!=0 else 0
    avg_album = round(total_album_saves/count_album_saves,2) if count_album_saves!=0 else 0


    song_retter = []
    album_retter = []
    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            song_count+=1
            song_retter.append(songData.json())

    for i in album_ids:
        albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={int(i)}"
        albumData = requests.get(albumFetcher)
        if albumData.status_code==200:
            album_count+=1
            album_retter.append(albumData.json())
    window = request.args.get("window") if request.args.get("window")!=None else "songs"
    stats={
        "song_count":song_count,
        "album_count":album_count,
        "total_likes":total_likes,  
        "avg_rating":avg_rating,
        "avg_album":avg_album,
    }
    return render_template("creator_dash.html",user_name=user_name,creator=creator,user_data=userData,stats=stats,song_ids=song_retter,album_ids=album_retter,creator_id=creatorData["creator_id"],window=window)

@app.route("/creator/<user_name>/add-song")
def add_song(user_name):
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    song_ids = creatorData["song_ids"].split(",") if creatorData["song_ids"].split(",")[0]!="" else []
    album_ids = creatorData["album_ids"].split(",") if creatorData["album_ids"].split(",")[0]!="" else []
    song_retter = []
    album_retter = []
    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={i}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            song_retter.append(songData.json())

    for i in album_ids:
        albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={i}"
        albumData = requests.get(albumFetcher)
        if albumData.status_code==200:
            album_retter.append(albumData.json())
    return render_template("add_songs.html",user_name=user_name,song_ids=song_retter,album_ids=album_retter,creator_id=creatorData["creator_id"])

@app.route("/<user_name>/add-song-form",methods=["GET","POST"])
def add_song_form(user_name):
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json() 

    data = request.form
    artist_id = 0
    artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={data['artist']}"
    artistData = requests.get(artistFetcher)
    if artistData.status_code==200:
        artist_id=artistData.json()["artist_id"]
    else:
        artistPost = f"http://127.0.0.1:5000/api/artist"
        artistEntry = {
            "artist_name":data["artist"]
        }
        repo = requests.post(artistPost,json=artistEntry)
        if repo.status_code==200:
            artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={data['artist']}"
            artistData = requests.get(artistFetcher)
            artist_id = artistData.json()["artist_id"]
        
    songPost = f"http://127.0.0.1:5000/api/songs"
    songEntry={
        "song_name":data["title"],
        "lyrics_id":0,
        "duration":0,
        "creator_id":int(creatorData["creator_id"]),
        "artist_id":artist_id,
        "playlist_in":0,
        "album_in":0,
        "date_created":f"{data['date']}",
    }
    songResponse = requests.post(songPost,json=songEntry)
    if songResponse.status_code==200:
        # print(data['title'])
        songFetcher = f"http://127.0.0.1:5000/api/songs?name={data['title']}"
        songFetchData = requests.get(songFetcher)
        # print(songFetchData.json())
        if songFetchData.status_code==200:
            print(data["lyrics"])
            lyricsStringer = data["lyrics"]
            # lyricsStringer = lyricsStringer.replace("\n\n","\n#spacex\n")

            file_path = f"app/static/lyrics/lyrics_{songFetchData.json()['song_id']}.txt"
            with open(file_path, 'w') as file:
                file.write(lyricsStringer)
            lyricsPost = f"http://127.0.0.1:5000/api/lyrics"
            lyricsEntry = {
                "lyrics_path":file_path,
                "song_id":songFetchData.json()['song_id']
            }
            lyricsResponse = requests.post(lyricsPost,json=lyricsEntry)
            if lyricsResponse.status_code==400:
                return {"message":"may day"}


        song_ids = creatorData["song_ids"].split(",") if creatorData["song_ids"].split(",")[0]!="" else []
        song_ids.append(str(songFetchData.json()["song_id"]))
        print(song_ids)
        entry={
            "user_name":user_name,
            "song_ids":",".join(song_ids),
            "album_ids":creatorData["album_ids"]
        }
        creatorPutter = f"http://127.0.0.1:5000/api/creator"
        creatorRespo = requests.put(creatorPutter,json=entry)
    return redirect(f"/creator/{user_name}?creator_id={creatorData['creator_id']}")

@app.route("/creator/<user_name>/edit-song")
def edit_song(user_name):
    song_id = request.args.get("song_id")
    songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(song_id)}"
    songDataFetcher = requests.get(songFetcher).json()

    artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_id={songDataFetcher['artist_id']}"
    artistData = requests.get(artistFetcher).json()

    lyricsFetcher = f"http://127.0.0.1:5000/api/lyrics?song_id={songDataFetcher['song_id']}"
    lyricsData = requests.get(lyricsFetcher).json()
    
    file_path = lyricsData["lyrics_path"]
    with open(file_path, 'r') as file:
        lyrics = file.read()

    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    song_ids = creatorData["song_ids"].split(",") if creatorData["song_ids"].split(",")[0]!="" else []
    album_ids = creatorData["album_ids"].split(",") if creatorData["album_ids"].split(",")[0]!="" else []
    song_retter = []
    album_retter = []
    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            song_retter.append(songData.json())

    for i in album_ids:
        albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={int(i)}"
        albumData = requests.get(albumFetcher)
        if albumData.status_code==200:
            album_retter.append(albumData.json())
    return render_template("edit_songs.html",user_name=user_name,song_ids=song_retter,album_ids=album_retter,songData=songDataFetcher,artist_name=artistData["artist_name"],lyrics=lyrics,creator_id=creatorData["creator_id"])

@app.route("/<user_name>/edit-song-form",methods=["GET","POST"])
def edit_song_form(user_name):
    song_id = request.args.get("song_id")
    data = request.form

    artist_id = 0
    artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={data['artist']}"
    artistData = requests.get(artistFetcher)
    if artistData.status_code==200:
        artist_id=artistData.json()["artist_id"]
    else:
        artistPost = f"http://127.0.0.1:5000/api/artist"
        artistEntry = {
            "artist_name":data["artist"]
        }
        repo = requests.post(artistPost,json=artistEntry)
        if repo.status_code==200:
            artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={data['artist']}"
            artistData = requests.get(artistFetcher)
            artist_id = artistData.json()["artist_id"]
    
    songFetcher = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    songData = requests.get(songFetcher).json()
    songPut = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    songEntry={
        "song_name":data["title"],
        "lyrics_id":0,
        "duration":0,
        "creator_id":songData["creator_id"],
        "artist_id":artist_id,
        "playlist_in":0,
        "album_in":0,
        "date_created":f"{data['date']}",
    }
    songResponse = requests.put(songPut,json=songEntry)
    if songResponse.status_code==200:
        songFetcher = f"http://127.0.0.1:5000/api/songs?name={data['title']}"
        songFetchData = requests.get(songFetcher)

        if songFetchData.status_code==200:
            lyricsStringer = data["lyrics"]
            
            lyricsFetcher = f"http://127.0.0.1:5000/api/lyrics?song_id={song_id}"
            lyricsData = requests.get(lyricsFetcher).json()


            file_path = f"app/static/lyrics/lyrics_{songFetchData.json()['song_id']}.txt"
            with open(file_path, 'w') as file:
                file.write(lyricsStringer)
            lyricsPut = f"http://127.0.0.1:5000/api/lyrics?id={lyricsData['lyrics_id']}"
            lyricsEntry = {
                "lyrics_path":file_path,
                "song_id":songFetchData.json()['song_id']
            }
            lyricsResponse = requests.put(lyricsPut,json=lyricsEntry)
            if lyricsResponse.status_code==400:
                return {"message":"may day"}

    return redirect(f"/creator/{user_name}?creator_id={songData['creator_id']}")

@app.route("/creator/<user_name>/delete-song")
def delete_song(user_name):
    song_id = request.args.get("song_id")
    songFetcher = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    songData = requests.get(songFetcher).json()

    lyricsFetcher = f"http://127.0.0.1:5000/api/lyrics?song_id={song_id}"
    lyricsDeleter = requests.delete(lyricsFetcher)


    songDeleter = requests.delete(songFetcher)

    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    song_ids = creatorData["song_ids"].split(",") if creatorData["song_ids"].split(",")[0]!="" else []
    song_ids.remove(song_id)
    creatorPut = f"http://127.0.0.1:5000/api/creator"
    creatorEntry = {
        "user_name":user_name,
        "song_ids":",".join(song_ids),
        "album_ids":creatorData["album_ids"]
    }
    creatorRespo = requests.put(creatorPut,json=creatorEntry)
    if creatorRespo.status_code==400:
        return {"message":"may day!!"}
    return redirect(f"/creator/{user_name}?creator_id={creatorData['creator_id']}")

@app.route("/creator/<user_name>/create-album",methods=["GET","POST"])
def add_album(user_name):
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    song_ids = creatorData["song_ids"].split(",") if creatorData["song_ids"].split(",")[0]!="" else []
    album_ids = creatorData["album_ids"].split(",") if creatorData["album_ids"].split(",")[0]!="" else []
    song_retter = []
    album_retter = []
    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            song_retter.append(songData.json())

    for i in album_ids:
        albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={int(i)}"
        albumData = requests.get(albumFetcher)
        if albumData.status_code==200:
            album_retter.append(albumData.json())
    return render_template("add_album.html",user_name=user_name,song_ids=song_retter,album_ids=album_retter,creator_id=creatorData["creator_id"])

@app.route("/creator/<user_name>/add-album-form",methods=["GET","POST"])
def add_album_form(user_name):
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()

    title = request.form["title"]
    genre = request.form["genre"]
    artist = request.form["artist"]
    songList = request.form.getlist("songList")

    artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={artist}"
    artistData = requests.get(artistFetcher)
    if artistData.status_code==200:
        artist_id = artistData.json()["artist_id"]
    else:
        artistPoster = f"http://127.0.0.1:5000/api/artist"
        artistEntry = {
            "artist_name":artist
        }
        artistRespo = requests.post(artistPoster,json=artistEntry)
        if artistRespo.status_code==200:
            artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={artist}"
            artistData = requests.get(artistFetcher)
            artist_id = artistData.json()["artist_id"]

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%d/%m/%Y")
    albumPoster = f"http://127.0.0.1:5000/api/album"
    albumEntry = {
        "album_name": title,
        "genre": genre,
        "artist_id": artist_id,
        "creator_id": creatorData["creator_id"],
        "date_created": formatted_date,
        "song_ids": ','.join(songList),
        "saved_by": "",
    }
    albumRespo = requests.post(albumPoster,json=albumEntry)
    if albumRespo.status_code==200:
        albumFetcher = f"http://127.0.0.1:5000/api/album?album_name={title}"
        albumData = requests.get(albumFetcher).json()
        album_ids = creatorData["album_ids"].split(",") if creatorData["album_ids"].split(",")[0]!="" else []
        album_ids.append(str(albumData["album_id"]))
        print(album_ids)
        creatorPut = f"http://127.0.0.1:5000/api/creator"
        creatorEntry = {
            "user_name":user_name,
            "song_ids":creatorData["song_ids"],
            "album_ids":",".join(album_ids)
        }
        creatorRespo = requests.put(creatorPut,json=creatorEntry)
        if creatorRespo.status_code==400:
            return {"message":"may day!!!"}
    return redirect(f"/creator/{user_name}?creator_id={creatorData['creator_id']}&window=album")

@app.route("/creator/<user_name>/edit-album")
def edit_album(user_name):
    album_id = request.args.get("album_id")
    albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={album_id}"
    albumFetchedData = requests.get(albumFetcher).json()

    artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_id={albumFetchedData['artist_id']}"
    artistData = requests.get(artistFetcher)
    artist = artistData.json()["artist_name"]

    songer_ids = albumFetchedData["song_ids"].split(",") if albumFetchedData["song_ids"].split(",")[0]!="" else []
    songList = []
    for i in songer_ids:
        songFarFetch = f"http://127.0.0.1:5000/api/songs?id={i}"
        songFarData = requests.get(songFarFetch)
        if songFarData.status_code==200:
            songList.append(songFarData.json())

    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    # song_ids = creatorData["song_ids"].split(",")
    song_ids = creatorData["song_ids"].split(",") if creatorData["song_ids"].split(",")[0]!="" else []
    # album_ids = creatorData["album_ids"].split(",")
    album_ids = creatorData["album_ids"].split(",") if creatorData["album_ids"].split(",")[0]!="" else []
    song_retter = []
    album_retter = []
    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            song_retter.append(songData.json())

    for i in album_ids:
        albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={int(i)}"
        albumData = requests.get(albumFetcher)
        if albumData.status_code==200:
            album_retter.append(albumData.json())
    return render_template("edit_album.html",albumData=albumFetchedData,user_name=user_name,song_ids=song_retter,album_ids=album_retter,songList=songList,artist_name=artist,creator_id=creatorData["creator_id"])

@app.route("/edit-album-form",methods=["POST","GET"])
def edit_album_form():
    album_id = request.args.get("album_id")
    user_name = request.args.get("user_name")
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={int(album_id)}"
    albumData = requests.get(albumFetcher).json()
    title = request.form["title"]
    genre = request.form["genre"]
    artist = request.form["artist"]
    artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={artist}"
    artistData = requests.get(artistFetcher)
    if artistData.status_code==200:
        artist_id = artistData.json()["artist_id"]
    else:
        artistPoster = f"http://127.0.0.1:5000/api/artist"
        artistEntry = {
            "artist_name":artist
        }
        artistRespo = requests.post(artistPoster,json=artistEntry)
        if artistRespo.status_code==200:
            artistFetcher = f"http://127.0.0.1:5000/api/artist?artist_name={artist}"
            artistData = requests.get(artistFetcher)
            artist_id = artistData.json()["artist_id"]

    songList = request.form.getlist("songList")
    # print(songList)
    albumPuter = f"http://127.0.0.1:5000/api/album?album_id={int(album_id)}"
    albumEntry = {
        "album_name":title,
        "genre":genre,
        "artist_id":artist_id,
        "creator_id":albumData["creator_id"],
        "date_created":albumData["date_created"],
        "song_ids":",".join(songList),
        "saved_by":albumData["saved_by"],
    }
    albumRepos = requests.put(albumPuter,json=albumEntry)
    if albumRepos.status_code==400:
        return {"message":"may day !!"}
    return redirect(f"/creator/{user_name}?creator_id={creatorData['creator_id']}&window=album")

@app.route("/creator/<user_name>/delete-album")
def delete_album(user_name):
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?user_name={user_name}"
    creatorData = requests.get(creatorFetcher).json()
    album_id = request.args.get("album_id")
    albumDeleter = f"http://127.0.0.1:5000/api/album?album_id={int(album_id)}"
    albumRespo = requests.delete(albumDeleter)

    album_ids = creatorData["album_ids"].split(",")
    album_ids.remove(album_id)
    creatorPut = f"http://127.0.0.1:5000/api/creator"
    creatorEntry = {
        "user_name":user_name,
        "song_ids":creatorData["song_ids"],
        "album_ids":",".join(album_ids)
    }
    creatorRespo = requests.put(creatorPut,json=creatorEntry)
    if creatorRespo.status_code==400:
        return {"message":"may day!!"}
    return redirect(f"/creator/{user_name}?creator_id={creatorData['creator_id']}&window=album")

@app.route("/admin-signin")
def admin_signin():
    return render_template("admin_signin.html")

@app.route("/admin-signin-form",methods=["GET","POST"])
def admin_signin_form():
    data = request.form
    adminFetcher = f"http://127.0.0.1:5000/api/admin?user_name={data['name']}&password={data['password']}"
    adminData = requests.get(adminFetcher)
    if adminData.status_code==400:
        return render_template("admin_signin.html",message="Credentials wrong. You are not authorised.")

    return redirect(f"/admin/{data['name']}")

@app.route("/admin/<user_name>")
def admin_dash(user_name):
    usersFetcher = f"http://127.0.0.1:5000/api/user"
    usersData = requests.get(usersFetcher).json()
    
    creatorsFetcher = f"http://127.0.0.1:5000/api/creator"
    creatorsData = requests.get(creatorsFetcher).json()
    
    songsFetcher = f"http://127.0.0.1:5000/api/songs"
    songsData = requests.get(songsFetcher).json()
    
    albumsFetcher = f"http://127.0.0.1:5000/api/album"
    albumsData = requests.get(albumsFetcher).json()
    
    ratingFetcher = f"http://127.0.0.1:5000/api/rating"
    ratingData = requests.get(ratingFetcher).json()
    
    avg_rating = 0
    total_rating = 0
    total_saves = 0
    avg_saves = 0
    total_likes = 0
    popular_song = {}
    no_genre = []
    for i in ratingData:
        total_rating+=i['rating']
        total_likes+=i["love"]
        if i["song_id"] not in popular_song:
            popular_song[i["song_id"]] = i["love"]
        else:
            popular_song[i["song_id"]]+=i["love"]
    avg_rating = round(total_rating/len(ratingData),2)
    pop_song = max(popular_song, key=lambda k: popular_song[k])
    songFetcher = f"http://127.0.0.1:5000/api/songs?id={pop_song}"
    songData = requests.get(songFetcher).json()

    for i in albumsData:
        total_saves+=len(i['saved_by'].split(","))
        if i["genre"] not in no_genre:
            no_genre.append(i["genre"])
    avg_saves = round(total_saves/len(albumsData),2)
    no_genre = len(list(set(no_genre)))

    stats={
        "total_users":len(usersData),
        "total_creators":len(creatorsData),
        "total_songs":len(songsData),
        "total_albums":len(albumsData),
        "avg_rating":avg_rating,
        "avg_saves":avg_saves,
        "total_likes":total_likes,
        "most_popular_song":songData["song_name"],
        "no_genre":no_genre,
    }
    return render_template("admin_dash.html",stats=stats,user_name=user_name)

@app.route("/admin/<user_name>/allSongs")
def admin_songs(user_name):
    songFetcher = f"http://127.0.0.1:5000/api/songs"
    songData = requests.get(songFetcher).json()[::-1]
    return render_template("admin_songs.html",allSongs=songData,user_name=user_name)

@app.route("/admin-song-delete")
def admin_song_delete():
    song_id = request.args.get("song_id")
    user_name = request.args.get("user_name")
    songUrl = f"http://127.0.0.1:5000/api/songs?id={song_id}"
    songDeleter = requests.delete(songUrl)
    return redirect(f"/admin/{user_name}/allSongs")

@app.route("/admin-song-flag")
def admin_song_flag():
    song_id = request.args.get("song_id")
    user_name = request.args.get("user_name")
    return redirect(f"/admin/{user_name}/allSongs")

@app.route("/admin/<user_name>/allAlbums")
def admin_album(user_name):
    albumFetcher = f"http://127.0.0.1:5000/api/album"
    albumData = requests.get(albumFetcher).json()
    return render_template("admin_album.html",albumData=albumData,user_name=user_name)

@app.route("/admin/<user_name>/albums")
def admin_album_search(user_name):
    album_id = request.args.get("album_id")
    albumFetcher = f"http://127.0.0.1:5000/api/album?album_id={album_id}"
    albumData = requests.get(albumFetcher).json()
    allSongs = []
    song_ids = albumData["song_ids"].split(",") if albumData["song_ids"].split(",")[0]!="" else []
    for i in song_ids:
        songFetcher = f"http://127.0.0.1:5000/api/songs?id={int(i)}"
        songData = requests.get(songFetcher)
        if songData.status_code==200:
            allSongs.append(songData.json())
    return render_template("admin_album_search.html",albumData=albumData,user_name=user_name,allSongs=allSongs)

@app.route("/admin-album-delete")
def admin_album_delete():
    album_id = request.args.get("album_id")
    user_name = request.args.get("user_name")
    albumUrl = f"http://127.0.0.1:5000/api/album?album_id={album_id}"
    albumDeleter = requests.delete(albumUrl)
    if albumDeleter.status_code==400:
        return {"message":"may day !!"}
    return redirect(f"/admin/{user_name}/allAlbums")

@app.route("/admin-album-flag")
def admin_album_flag():
    song_id = request.args.get("song_id")
    user_name = request.args.get("user_name")
    return redirect(f"/admin/{user_name}/allAlbums")

@app.route("/admin/<user_name>/allUsers")
def admin_user(user_name):
    userFetcher = f"http://127.0.0.1:5000/api/user"
    userData = requests.get(userFetcher).json()
    for i in userData:
        ratingFetcher = f"http://127.0.0.1:5000/api/rating?user_name={i['user_name']}"
        ratingData = requests.get(ratingFetcher)
        if ratingData.status_code==200:
            love=0
            ratings=0
            for j in ratingData.json():
                love+=j["love"]
                ratings+=1
            engScore = 20*love + 80*ratings
        else:
            engScore = 0
        i["eng_score"] = engScore
    userData = sorted(userData, key=lambda x: x['eng_score'])[::-1]
    with open("app/static/jsons/userActions.json", 'r') as file:
        jsonData = json.load(file)
    return render_template("admin_user.html",userData=userData,user_name=user_name,banData=jsonData)

@app.route("/admin/<user_name>/allCreators")
def admin_creators(user_name):
    creatorFetcher = f"http://127.0.0.1:5000/api/creator"
    creatorData = requests.get(creatorFetcher).json()
    for i in creatorData:
        i["song_count"] = len(i["song_ids"].split(",")) if i["song_ids"].split(",")[0] != "" else 0
        i["album_count"] = len(i["album_ids"].split(",")) if i["album_ids"].split(",")[0] != "" else 0
    creatorData = sorted(creatorData, key=lambda x: x['song_count'])[::-1]
    with open("app/static/jsons/creatorActions.json", 'r') as file:
        jsonData = json.load(file)
    return render_template("admin_creator.html",creatorData=creatorData,user_name=user_name,listData=jsonData)

@app.route("/admin-user-tempBan")
def admin_user_tempBan():
    user_id = request.args.get("user_id")
    admin_name = request.args.get("admin_name")
    userFetcher = f"http://127.0.0.1:5000/api/user?user_id={user_id}"
    userData = requests.get(userFetcher).json()
    with open("app/static/jsons/userActions.json", 'r') as file:
        data = json.load(file)
    current_date_time = datetime.now()
    current_date = current_date_time.date()
    end_date = current_date + timedelta(days=30)
    print(current_date)
    data[f"{user_id}"] = {
        "ban_type" : "temp ban",
        "user_name" : userData["user_name"],
        "start_date" : f"{current_date}",
        "end_date" : f"{end_date}",
        "admin_name" : admin_name
    }
    print(data)
    with open("app/static/jsons/userActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allUsers")

@app.route("/admin-user-tempBan-remove")
def admin_user_tempBan_remove():
    user_id = request.args.get("user_id")
    admin_name = request.args.get("admin_name")
    with open("app/static/jsons/userActions.json", 'r') as file:
        data = json.load(file)
    del data[f"{user_id}"]

    with open("app/static/jsons/userActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allUsers")

@app.route("/admin-user-permaBan")
def admin_user_permaBan():
    user_id = request.args.get("user_id")
    admin_name = request.args.get("admin_name")
    userFetcher = f"http://127.0.0.1:5000/api/user?user_id={user_id}"
    userData = requests.get(userFetcher).json()
    with open("app/static/jsons/userActions.json", 'r') as file:
        data = json.load(file)
    current_date_time = datetime.now()
    current_date = current_date_time.date()
    data[f"{user_id}"] = {
        "ban_type" : "perma ban",
        "user_name" : userData["user_name"],
        "ban_date" : f"{current_date}",
        "admin_name" : admin_name
    }
    with open("app/static/jsons/userActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allUsers")

@app.route("/admin-user-permaBan-remove")
def admin_user_permaBan_remove():
    user_id = request.args.get("user_id")
    admin_name = request.args.get("admin_name")
    with open("app/static/jsons/userActions.json", 'r') as file:
        data = json.load(file)
    del data[f"{user_id}"]
    with open("app/static/jsons/userActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allUsers")


@app.route("/admin-creator-whitelist")
def admin_creator_whitelist():
    creator_id = request.args.get("creator_id")
    admin_name = request.args.get("admin_name")
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?creator_id={creator_id}"
    creatorData = requests.get(creatorFetcher).json()
    with open("app/static/jsons/creatorActions.json", 'r') as file:
        data = json.load(file)
    # print(current_date)
    data[f"{creator_id}"] = {
        "list_type" : "white",
        "user_name" : creatorData["user_name"],
        "admin_name" : admin_name
    }
    # print(data)
    with open("app/static/jsons/creatorActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allCreators")

@app.route("/admin-creator-whitelist-remove")
def admin_creator_whitelist_remove():
    creator_id = request.args.get("creator_id")
    admin_name = request.args.get("admin_name")
    with open("app/static/jsons/creatorActions.json", 'r') as file:
        data = json.load(file)
    del data[f"{creator_id}"]

    with open("app/static/jsons/creatorActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allCreators")

@app.route("/admin-creator-blacklist")
def admin_creator_blacklist():
    creator_id = request.args.get("creator_id")
    admin_name = request.args.get("admin_name")
    creatorFetcher = f"http://127.0.0.1:5000/api/creator?creator_id={creator_id}"
    creatorData = requests.get(creatorFetcher).json()
    with open("app/static/jsons/creatorActions.json", 'r') as file:
        data = json.load(file)
    # print(current_date)
    data[f"{creator_id}"] = {
        "list_type" : "black",
        "user_name" : creatorData["user_name"],
        "admin_name" : admin_name
    }
    # print(data)
    with open("app/static/jsons/creatorActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allCreators")

@app.route("/admin-creator-blacklist-remove")
def admin_user_blacklist_remove():
    creator_id = request.args.get("creator_id")
    admin_name = request.args.get("admin_name")
    with open("app/static/jsons/creatorActions.json", 'r') as file:
        data = json.load(file)
    del data[f"{creator_id}"]

    with open("app/static/jsons/creatorActions.json", 'w') as file:
        json.dump(data, file, indent=2)
    return redirect(f"/admin/{admin_name}/allCreators")


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

# if __name__=="__main__":
#     app.run(debug=True)