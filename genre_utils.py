import eyed3
import os
import pickle
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from general_utils import unique_list


def read_genres(folder):
    genre_map = {}
    for subdir, dirs, files in os.walk(folder):
        if not dirs:  # album directory
            album_genres = []
            for f in files:
                try:
                    audio = EasyID3(os.path.join(subdir, f))
                except ID3NoHeaderError:
                    continue
                try:
                    audio['genre']
                except KeyError:
                    continue
                for g in audio['genre']:
                    album_genres += g.split('/')
            album_genres = unique_list(album_genres)
            if album_genres == []:
                album_genres = ['']
            genre_map[subdir] = album_genres
    for album, genre in genre_map.items():
        print(album + " -> " + str(genre))
    return genre_map


def replace_genres(lib_genres, corrections):
    for album, genres in lib_genres.items():
        new_genres = genres.copy()
        for g in genres:
            if g in corrections:
                rplc = corrections[g].split('/')
                new_genres.remove(g)
                new_genres += rplc
        new_genres = unique_list(new_genres)

        if genres == new_genres:
            continue
        if '' in new_genres:
            new_genres.remove('')
        if len(new_genres) == 0:
            print("WARNING: No Genres defined for ", album)
            genre_str = ''
        elif len(new_genres) == 1:
            genre_str = new_genres[0]
        else:
            genre_str = new_genres[0]
            for i in range(1,len(new_genres)):
                genre_str += '/'+new_genres[i]

        print("Replacing genre in ", album)
        print("\t",genres,"--->",genre_str)
        for file in os.listdir(album):
            try:
                audio = EasyID3(os.path.join(album, file))
            except ID3NoHeaderError:
                continue
            audio['genre'] = genre_str
            audio.save()
    return


def replace_genre_album(album, genre_str):
    print("Replacing genre in ", album)
    for file in os.listdir(album):
        try:
            audio = EasyID3(os.path.join(album, file))
        except ID3NoHeaderError:
            continue
        audio['genre'] = genre_str
        audio.save()
    return


def update_genre(rootdir, corrections):
    lib_genres = read_genres(rootdir)
    with open('lib_genres.pickle', 'wb') as handle:
        pickle.dump(lib_genres, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('lib_genres.pickle', 'rb') as handle:
    #     lib_genres = pickle.load(handle)

    all_genres = []
    for album, genre in lib_genres.items():
        print(album + " -> " + str(genre))
        all_genres += genre
    unique_list(all_genres)
    print(all_genres)

    # replace_genres(lib_genres, corrections)

    # album_corrections = {'path/to/album': 'Genre1/Gere2'}
    # for album, genre in album_corrections.items():
    #     replace_genre_album(album, genre)

