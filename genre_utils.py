import eyed3
import os
from general_utils import unique_list


def replace_genre(file, current, replace):
    audiofile = eyed3.load(file)
    if audiofile.tag.genre.name == current:
        audiofile.tag.genre.name = replace
        audiofile.tag.save()
    return


def update_genre(rootdir):
    all_genres = []
    genre_map = {}
    for subdir, dirs, files in os.walk(rootdir):
        if not dirs:  # album directory
            album_genres = []
            for f in files:
                audiofile = eyed3.load(os.path.join(subdir, f))
                if audiofile:
                    album_genres += audiofile.tag.genre.name.split('/')
            album_genres = unique_list(album_genres)
            all_genres += album_genres
            genre_map[subdir] = album_genres
    all_genres = unique_list(all_genres)

    for album, genre in genre_map.items():
        print(album + " -> " + str(genre))

    print(all_genres)
