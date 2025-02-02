# KalpRaag - Multi-User Music Streaming Platform
![image](https://github.com/user-attachments/assets/ba04c7e4-0fcc-4595-af82-9f82ff069667)

This project was created to fulfill the requirements for the MAD-2 Project of the **BS in Data Science and Application** degree program from **Indian Institute of Technology, Madras (IIT Madras)**.

KalpRaag is a multi-user music streaming platform designed for music lovers, passionate creators, and moderated by admins. The platform offers a seamless experience for users to listen to music, create playlists, and interact with content, while creators can upload and manage their songs and albums. Admins have the ability to moderate content and manage users.

Kindly watch this video demostration of the project: [Go to Video Demo](https://drive.google.com/file/d/1o0sdUVMwG27UjXLHg784Qswcl1zV3U4b/view?usp=sharing)

LinkedIn Post: [Go to LinkedIn Post](https://www.linkedin.com/posts/saranshsaini48_project-webdevelopment-fullstackdeveloper-activity-7170666359729610752-kARx?utm_source=share&utm_medium=member_desktop)

## Technologies Used

![image](https://github.com/user-attachments/assets/4b39c4ec-b3b6-4044-8cf5-e30ce44ef1a6)

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask
- **Database:** SQLite
- **API:** RESTful APIs

## System Architecture

![image](https://github.com/user-attachments/assets/fec1d02b-82d5-42e4-8561-d074f6daa568)

The application is divided into three main components:

1. **Database Management:** Powered by SQLite, with models designed using Flask-SQLAlchemy.
2. **Backend:** Built with Flask, handling CRUD operations through REST APIs.
3. **Frontend:** Developed using HTML, CSS, and JavaScript, with dynamic data rendering.

### Database Models

The database models are meticulously designed with appropriate constraints to ensure data integrity. Below is a snippet of the `Creator` model:

```python
class Creator(db.Model):
    creator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.Integer, unique=True, nullable=False)
    song_ids = db.Column(db.String, nullable=False)
    album_ids = db.Column(db.String, nullable=False)
```

## API Management

The database's CRUD operations are exclusively executed through APIs, leveraging Flask-Restful to implement essential functionalities such as GET, POST, PUT, and DELETE operations at specific endpoints. This ensures a robust and standardized mechanism for interacting with the database.

## Multi-User Functionalities and Features

### User Features:

- Read lyrics
- Rate and like songs
- Create & delete playlists
- Save albums
- Register for creator access

### Creator Features:

- All user access
- View statistics
- Add/Edit/Delete songs
- Add/Edit/Delete albums

### Admin Features:

- View all statistics
- Delete/Flag songs
- Delete/Flag albums
- Ban users temporarily or permanently
- Blacklist/Whitelist creators

## User Interface

![image](https://github.com/user-attachments/assets/595c8369-ab80-4c98-9121-3500c55328df)

The web application presents an intuitive User Interface designed to accommodate the distinct requirements of three user categories: Users, Creators, and Admins. The design prioritizes a relaxing ambiance for users, fostering a positive and enjoyable interaction with the platform.

## Database Schema

![image](https://github.com/user-attachments/assets/a217efc9-ed16-4066-9ed9-6b73ed851f26)

The database schema includes tables for Users, Creators, Songs, Albums, and more, ensuring a comprehensive structure for managing music and user interactions.

## Conclusion

Developing KalpRaag was an enjoyable and rewarding experience. The project provided valuable insights into building a multi-user platform with distinct roles and functionalities.

### Extra Information

- **Debug Song:** Only one song is loaded in the app for debugging purposes.
- **How to Run the App:** In the terminal, type `python -m app.main` to run the app as a module.
