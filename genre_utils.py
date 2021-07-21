import eyed3
import os
import pickle
from general_utils import unique_list


def read_genres(folder):
    # all_genres = []
    genre_map = {}
    for subdir, dirs, files in os.walk(folder):
        if not dirs:  # album directory
            album_genres = []
            for f in files:
                audiofile = eyed3.load(os.path.join(subdir, f))
                if audiofile and audiofile.info != None:
                    if not audiofile.tag.genre:
                        album_genres += ['']
                    else:
                        album_genres += audiofile.tag.genre.name.split('/')
            album_genres = unique_list(album_genres)
            if album_genres == []:
                album_genres = ['']
            # all_genres += album_genres
            genre_map[subdir] = album_genres
    # all_genres = unique_list(all_genres)
    # for album, genre in genre_map.items():
    #     print(album + " -> " + str(genre))
    # print(all_genres)
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
            audiofile = eyed3.load(os.path.join(album, file))
            if audiofile and audiofile.info != None:
                audiofile.tag._setGenre(genre_str)
                audiofile.tag.save()
    return


def update_genre(rootdir, corrections):
    # lib_genres = read_genres(rootdir)
    # with open('lib_genres.pickle', 'wb') as handle:
    #     pickle.dump(lib_genres, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('lib_genres.pickle', 'rb') as handle:
        lib_genres = pickle.load(handle)
    replace_genres(lib_genres, corrections)

