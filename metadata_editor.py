from artwork_utils import save_artwork
from general_utils import copy_dir
from genre_utils import update_genre


if __name__ == '__main__':
    use_temp_dir = False
    save_art = False
    correct_genre = True
    # rootdir = r"/home/jimmy/Desktop/Jellyfin"
    rootdir = r"/Users/jimmy/Music/Jellyfin"
    tempdir = r"/home/jimmy/Desktop/temp"

    if use_temp_dir:
        copy_dir(rootdir, tempdir)
        rootdir = tempdir

    if save_art:
        save_artwork(rootdir)

    if correct_genre:
        corrections = {'old_genre': 'new_genre'}
        update_genre(rootdir, corrections)
