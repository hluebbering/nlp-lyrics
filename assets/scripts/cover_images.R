library(imager)
library(rvest)
library(magick)
library(spotifyr)
library(httr)

# user information
Sys.setenv(SPOTIFY_CLIENT_ID = "bd1c5f1d16b94210bc1776e172cbd264")
Sys.setenv(SPOTIFY_CLIENT_SECRET = "bdd68b2a802e4fb4919ef751741deb6d")
Sys.setenv(SPOTIFY_REDIRECT_URI = "http://localhost:1410/")

access_token <- get_spotify_access_token()
# access_token <- get_spotify_authorization_code()

x <- get_playlist(playlist_id = "1wi4r0VTz0zCr0HLMm3cG5")
img1 <- x$images$url[1] # get image url

# read image url
cover1 <- image_read(img1)
R3 <- image_append(image_scale(cover1, "x580"))
image_write(R3, path = "R3.svg", format = "svg")

# get image url
img1 <- x$images %>%
  data.frame() %>%
  dplyr::filter(height == 640) %>%
  dplyr::select(url) %>%
  unlist(use.names = FALSE)

tiger <- image_read(path = img1, depth = 16, density = 1800)
playlist_img <- image_scale(tiger, "800x800")
playlist_img2 <- image_scale(playlist_img, "x900")
# image_write(playlist_img2, path = "playlist_img.png", format = "png", quality = 100, depth = 16, density = 1000)







tracks <- spotifyr::get_playlist_tracks("1wi4r0VTz0zCr0HLMm3cG5")
track_imgs <- tracks$track.album.images

playlist_images <- list()

for (i in 1:4) {
  myimage <- track_imgs[[i]] %>%
    data.frame() %>%
    dplyr::filter(height == 640) %>%
    dplyr::select(url) %>%
    unlist(use.names = FALSE)
  tiger <- image_read(path = myimage, depth = 16, density = 1800)
  playlist_images <- append(playlist_images, tiger)
}

playlist_images <- image_scale(playlist_images, "800x800")

playlist_imagesA <- image_append(image_scale(c(playlist_images[2], playlist_images[1]), "x900"))
playlist_imagesB <- image_append(image_scale(c(playlist_images[4], playlist_images[3]), "x900"))
all_playlist_images <- c(playlist_imagesA, playlist_imagesB)


x3 <- image_append(image_scale(all_playlist_images, "x750"), stack = TRUE)
image_write(x3, path = "assets/playlist_img.png", format = "png", quality = 100, depth = 16, density = 1000)
