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
    # lib_genres = read_genres(rootdir)
    # with open('lib_genres.pickle', 'wb') as handle:
    #     pickle.dump(lib_genres, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('lib_genres.pickle', 'rb') as handle:
    #     lib_genres = pickle.load(handle)

    # all_genres = []
    # for album, genre in lib_genres.items():
    #     print(album + " -> " + str(genre))
    #     all_genres += genre
    # unique_list(all_genres)
    # print(all_genres)

    # replace_genres(lib_genres, corrections)

    album_corrections = {
        {'/Users/jimmy/Music/Jellyfin/Longmont Potion Castle/Tour Line Live': 'Prank Calls',
'/Users/jimmy/Music/Jellyfin/Lifetones/For A Reason': 'Post-Punk',
'/Users/jimmy/Music/Jellyfin/Teenage Panzerkorps/Gleich Heilt Gleich': 'Rock/Punk',
'/Users/jimmy/Music/Jellyfin/Captain Beefheart & His Magic Band/Safe as Milk': 'Rock/Garage Rock',
'/Users/jimmy/Music/Jellyfin/Black Dice/Load Blown': 'Electronic',
'/Users/jimmy/Music/Jellyfin/This Heat/Deceit': 'Post-Punk/No Wave',
'/Users/jimmy/Music/Jellyfin/Chrome/Half Machine Lip Moves': 'Post-Punk/Noise Rock',
'/Users/jimmy/Music/Jellyfin/Radiohead/Amnesiac': 'Rock/Electronic',
'/Users/jimmy/Music/Jellyfin/Swans/Children of God': 'Art Rock/Goth/Industrial',
'/Users/jimmy/Music/Jellyfin/Polo & Pan/Dorothy': 'Electronic',
'/Users/jimmy/Music/Jellyfin/Compilations/I\'m Starting To Feel OK - Volume 3': 'Japanese/Deep House/Electronic/House/Techno',
'/Users/jimmy/Music/Jellyfin/Walter Wanderley/Rain Forest': 'Jazz/Latin/Bosa Nova',
'/Users/jimmy/Music/Jellyfin/Gary Numan/The Pleasure Principle': 'Electronic/Synth-Pop/Goth',
'/Users/jimmy/Music/Jellyfin/Air/LateNightTales_ Air': 'Electronic/Rock',
'/Users/jimmy/Music/Jellyfin/Hui Ohana/Ono': 'Hawaiian Folk',
'/Users/jimmy/Music/Jellyfin/Nicolas Jaar/Love You Gotta Lose Again': 'Electronic',
'/Users/jimmy/Music/Jellyfin/The Beat/The Beat': 'Rock/Power Pop',
'/Users/jimmy/Music/Jellyfin/Scion/Arrange And Process Basic Channel Tracks': 'Electronic/House',
'/Users/jimmy/Music/Jellyfin/Holden/The Idiots Are Winning': 'IDM/Electronic/House',
'/Users/jimmy/Music/Jellyfin/Maurizio/M-Series': 'Electronic',
'/Users/jimmy/Music/Jellyfin/Manuel Göttsching/E2-E4': 'Electronic/Ambient',
'/Users/jimmy/Music/Jellyfin/Stars Of The Lid/And Their Refinement of the Decline': 'Ambient/Electronic/Drone',
'/Users/jimmy/Music/Jellyfin/Popol Vuh/In Den Gärten Pharaos': 'Electronic/Krautrock/Ambient',
'/Users/jimmy/Music/Jellyfin/Animal Collective/Spirit They\'re Gone, Spirit They\'ve Vanished': 'Electronic/Indie Rock/Noise',
'/Users/jimmy/Music/Jellyfin/Arthur Russell/Tower Of Meaning': 'Contemporary Classical/Avant-garde',
'/Users/jimmy/Music/Jellyfin/Arthur Russell/First Thought Best Thought': 'Contemporary Classical/Avant-garde/Electronic',
'/Users/jimmy/Music/Jellyfin/Arthur Russell/Calling Out Of Context': 'Disco/Electronic',
'/Users/jimmy/Music/Jellyfin/Glenn Branca/Lesson No. 1': 'Rock/Noise/No Wave',
'/Users/jimmy/Music/Jellyfin/Ernest Hood/Neighborhoods': 'Electronic'}
    }
    for album, genre in album_corrections.items():
        replace_genre_album(album, genre)

