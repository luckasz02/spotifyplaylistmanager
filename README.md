# Spotify Playlist Manager

This project is a Spotify Playlist Manager web application that allows users to easily add multiple songs at once to their playlists and shuffle the order of songs in their playlists. The application uses the Spotify Web API for music data and playlist management.

## Features

- Add Songs to Playlist: Search for songs by name and add them to any of your playlists.
- Shuffle Playlist: Randomly shuffle the songs within a selected playlist.

## Technologies Used

- Python: Backend development.
- Flask: Web framework to manage routing, sessions, and the server.
- Spotipy: A Python library for interacting with the Spotify Web API.
- JavaScript (Fetch API): To handle client-side interactions and AJAX requests.
- HTML & CSS: Frontend structure and styling.

## Setup & Installation

### Prerequisites

1. Spotify Developer Account: Ensure you have a Spotify Developer account.
2. Python: Make sure Python is installed on your system.
3. Environment Variables: Install python-dotenv to handle environment variables.

### Installation Steps

1. Clone this repository:

   git clone https://github.com/yourusername/spotify-playlist-manager.git
   cd spotify-playlist-manager

2. Create a virtual environment and activate it:

   python -m venv venv
   source venv/bin/activate # On Windows use venv\Scripts\activate

3. Install required packages:

   pip install -r requirements.txt

4. Set up your Spotify Developer credentials:

   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Create a new app to obtain your Client ID and Client Secret.
   - Set the Redirect URI to http://localhost:8888/callback.

5. Replace the "# Spotify credentials" section in "app.py" with your credentials:

   CLIENT_ID='your_client_id'
   CLIENT_SECRET='your_client_secret'
   REDIRECT_URI='http://localhost:8888/callback'

6. Run the application:

   flask run

7. Open the app in your browser at http://localhost:8888.

## Usage

1. Login with Spotify: Click the "Login with Spotify" button. You’ll be redirected to Spotify for authentication.
2. Select a Playlist: Choose a playlist from the dropdown to add songs or shuffle.
3. Add Songs to Playlist: Use the search box to find songs and add them to the selected playlist.
4. Shuffle Playlist: Click the "Shuffle" button to shuffle the selected playlist.
5. Account Information: The application displays the logged-in Spotify account name for confirmation.

### Note

Only registered users in the Spotify Developer Dashboard can access this app. If you'd like to use the app, please contact me to add your email to the app's registered users list on the Spotify Developer Dashboard.

## License

This project is licensed with a restrictive custom license.

**Usage is limited to authorized users only** – redistribution, modification, or commercial use of this software is strictly prohibited. For full details, please see the [LICENSE](./LICENSE) file.

If you’d like to request access, please contact the author.

### Explanation

- Setup & Installation: Guides the user through setting up the environment, installing dependencies, and configuring Spotify credentials.
- Usage: Provides instructions on using the main features.
- License: Specifies that the app is for personal use only, and it cannot be redistributed or modified without permission.
