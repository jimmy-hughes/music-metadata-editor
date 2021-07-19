import eyed3
import os
from mutagen.mp4 import MP4

def save_artwork_file(file, folder):
    with open(os.path.join(folder, "cover.jpg"), "wb") as img:
        img.write(file.tag.images[0].image_data)


def has_image_tags(file):
    if len(file.tag.images) > 0:
        return True
    return False


def has_image_tags_mutagen(file):
    if len(file['covr']) > 0:
        return True
    return False


def has_artwork_file(folder):
    for entry in os.scandir(folder):
        if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():
            return True
    return False


def save_artwork(rootdir):
    art_paths = {}
    missing_art = []
    for subdir, dirs, files in os.walk(rootdir):
        if not dirs:  # album directory
            print(subdir)
            if not has_artwork_file(subdir):
                found_art = False
                for f in files:
                    if f.endswith(".m4a"):
                        track = MP4(os.path.join(subdir, f))
                        if has_image_tags_mutagen(track):
                            art_paths[subdir] = f
                            found_art = True
                            break
                    elif f.endswith(".mp3") or f.endswith(".mp4") or f.endswith(".wav"):
                        audiofile = eyed3.load(os.path.join(subdir, f))
                        if has_image_tags(audiofile):
                            art_paths[subdir] = f
                            found_art = True
                            break
                if not found_art:
                    missing_art.append(subdir)
    print("Missing artwork could NOT be found for the following: ")
    for fldr in missing_art:
        print("\t" + fldr)
    print("Missing artwork was found for the following: ")
    for fldr in art_paths:
        print("\t" + fldr)
    resp = input("Do you want to save these images? (y/n)")
    if resp == 'y':
        print("Saving artwork")
        for subdir, f in art_paths.items():
            print("\t" + subdir)
            if f.endswith(".m4a"):
                track = MP4(os.path.join(subdir, f))
                pict = track['covr'][0]
                if pict.imageformat == 14:
                    fmt = '.png'
                else:
                    fmt = '.jpg'
                with open(os.path.join(subdir, "cover" + fmt), "wb") as img:
                    img.write(pict)
            elif f.endswith(".mp3") or f.endswith(".mp4") or f.endswith(".wav"):
                audiofile = eyed3.load(os.path.join(subdir, f))
                save_artwork_file(audiofile, subdir)
    else:
        print("Canceling artwork saving")
