from artwork_utils import save_artwork
from general_utils import copy_dir
from genre_utils import update_genre


if __name__ == '__main__':
    use_temp_dir = True
    save_art = True
    correct_genre = False
    rootdir = r"/home/jimmy/Desktop/Jellyfin"
    tempdir = r"/home/jimmy/Desktop/temp"

    if use_temp_dir:
        copy_dir(rootdir, tempdir)
        rootdir = tempdir

    if save_art:
        save_artwork(rootdir)

    if correct_genre:
        update_genre(rootdir)
