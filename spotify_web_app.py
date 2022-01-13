from flask import Flask, request, redirect, send_file, render_template
import requests
import json, base64

# create an instance for flask
app = Flask(__name__)

def requesting_access_token():
       
   # code to get the refresh token
   refresh_auth_url = "https://accounts.spotify.com/api/token"
       
   # Note: I have resetted the client_id and client_secret in the spotify dashboard for security reasons.
   # You should have your own client_id and client_secret
   # client ids and secret from spotify dashboard
   client_id = '177fdaf7917e4342802f36bab4fadb3a'
   client_secret = '8dcc31415c884443ad5f5818a13bf7ac'

   # encoding it as mentioned in the spotify authorization code flow guidance
   message = f"{client_id}:{client_secret}"
   message_bytes = message.encode('ascii')
   base64_bytes = base64.b64encode(message_bytes)
   base64_message = base64_bytes.decode('ascii')

   # authentication headers
   auth_headers = {"Authorization":f"Basic {base64_message}"}
   auth_data = {"grant_type":"client_credentials"}

   # post request for the access token
   refresh_res = requests.post(refresh_auth_url, headers=auth_headers, data=auth_data)

   access_token = refresh_res.json()['access_token']

   return access_token

# end point for the home page
# it displays the list of genres
@app.route('/')
def home():
       
   # get the genre and displays genre list - gets the user playlist 
   spotify_genre = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
   # access_token_genre = "BQBjTCL4j5e2BEil-eCoVD1tbqDIS2Ifq9wxJ6hxb-7YdVJMdZZ7wLjwLOo_sV8PLzFX2f7DFgeryfbLm4KrgZlXx3A4sviIBL7ITNEWxDBkTQgkG6HZPDFOopIkhHqoZxxLa04ZwFvH0_23OxGAZM63lPoI95CHfOS_YSkk4W9aQtlPSrurBB5IIoyKSyKEUZBSu9-WpTcHf6nOfLHJvXiwxrlxQ9_QD0zdqfDOv6q4_XawVEniEH51"
   access_token_genre = requesting_access_token()

   response_genre = requests.get(spotify_genre,
                                 headers={"Authorization": f"Bearer {access_token_genre}"}
                                 )

   genres_list = response_genre.json()['genres']
   return render_template('spotify_web_ui.html', genres_list=genres_list)

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
       
   if request.method == "POST":
          
      user_id = request.form.get("user_id")
      playlist_name = request.form.get("playlist_name")

      # creates playlist in the mentioned user id
      # user_id = '31akjszmlsziys4dxuvplt373duy'
      spotify_create_playlist = f"https://api.spotify.com/v1/users/{user_id}/playlists"
      # access_token_playlist = 'BQCz1i_gGnsP6d9maNo9A-R5Nw-gsHfNTYO05pHwXhvUWYucbKG1w_TORmUvivKBuqkHOSXqdJMQ7Vy8NzCCmKT4BpRG2IxV_vefXyh2C8B86ME4taEhw7Ymf_eADh2yEzfc0IU_y23h8D477Kd-SDInZCstscu62GmMOgjhzw3yr_PA6Ej86KmZ1g1ao9naZp1vZhYYXzFui7HwNZ5PG_UHakgBGJ2c'
      access_token_playlist = requesting_access_token()

      response_playlist = requests.post(spotify_create_playlist,
                                 headers={"Authorization": f"Bearer {access_token_playlist}"},
                                 json={
                                    "name":playlist_name,
                                    "public":False
                                    }
                                 )

      response_playlist = response_playlist.json()
   return redirect("/")

if __name__ == '__main__':
   app.run(debug = True)
