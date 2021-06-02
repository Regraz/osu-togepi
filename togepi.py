# TO-DO: 
# 1. Refactoring
# 2. Make mp3 files copy as well
# 3. Setting seeds or other information (such as dirs) interactively
# 4. README
# 5. Better .osu parsing

import glob
import numpy as np
import os
import shutil

class DirectoryProcessor():

    def __init__(self, work_dir:str, new_dir:str) -> None:
        self.work_dir = work_dir
        self.new_dir = new_dir
        self.files = []
        self.osufile = None

    def change_work_dir(self, work_dir:str) -> None:
        self.work_dir = work_dir
 
    def change_new_dir(self, new_dir:str) -> None:
        self.new_dir = new_dir

    def get_all_files(self) -> None:
        all_files = glob.glob(self.work_dir + '/*')
        all_files = [file.replace('\\', '/') for file in all_files]
        self.files = all_files.copy()

    def file_check_invalid(self, file) -> bool:
            filters = ['audio.mp3', '.png', '.PNG', '.osb', '.jpg', '.jpeg', '.JPG', '.JPEG']
            for filter in filters:
                if file.endswith(filter):
                    return True
            return False

    def copy_valid(self, file:str) -> None:
        file_ = '/' + file.split('/')[-1]
        shutil.copyfile(self.work_dir + file_, self.new_dir + file_)
        if file_.endswith('.osu'):
            self.osufile = self.new_dir + file_


    def file_process(self) -> None:
        for file in self.files:
            if self.file_check_invalid(file):
                continue
            else:
                self.copy_valid(file)
    
class OsuParser():

    def __init__(self, work_file:str, songs:list, anon_name:str) -> None:
        self.osufile = work_file
        self.songs = songs
        self.anon_name = anon_name

    def change_work_file(self, work_file:str) -> None:
        self.osufile = work_file

    def assign_anon_name(self, anon_name:str) -> None:
        self.anon_name = anon_name

    def save_file(self, fosu_:list) -> None:
        osufile_anon = os.path.dirname(self.osufile)
        with open(osufile_anon + '/' + self.anon_name + '.osu', 'w+', encoding="utf8") as fout:
            for lines in fosu_:
                fout.write('%s' % lines)

    def remove_old_file(self) -> None:
        os.remove(self.osufile)

    def anon_osufile(self) -> list: 
        with open(self.osufile, encoding="utf8") as fosu:
            fosu_ = fosu.readlines()
            fulltext = ''.join(fosu_)

        for idx in range(len(fosu_)):
            if fosu_[idx].startswith('AudioFilename:'):
                for song in self.songs:
                    if song in fulltext:
                        fosu_[idx] = 'AudioFilename: ../' + song + '.mp3\n'
                        break
            if fosu_[idx].startswith('Bookmarks:'):
                fosu_[idx] = 'Bookmark:\n'
            if fosu_[idx].startswith('Creator:'):
                fosu_[idx] = 'Creator:obwc 2021\n'
            if fosu_[idx].startswith('Version:'):
                fosu_[idx] = 'Version:' + self.anon_name + '\n'
            if fosu_[idx].startswith('BeatmapID:'):
                fosu_[idx] = 'BeatmapID:-1\n'
            if fosu_[idx].startswith('BeatmapSetID:'):
                fosu_[idx] = 'BeatmapSetID:-1\n'
            if fosu_[idx].startswith('//Background and Video events'):
                fosu_[idx + 1] = ''

        return fosu_

class Togepi():

    fun_names = ['anon_name1', 'anon_name2']
    songs = ['song_name1', 'song_name2']
    urmom = 'this is a secret'

    def __init__(self, entry_dir:str, anon_dir:str) -> None:
        self.anon_names = Togepi.fun_names.copy()
        self.entry_dir = entry_dir
        self.anon_dir = anon_dir
        self.all_entries = []

    def get_all_entries(self):
        all_entrynames = glob.glob(self.entry_dir + '*/')
        all_entrynames = [dir[2:-1] for dir in all_entrynames]
        self.all_entries = all_entrynames
       
    def metronome(self):
        np.random.seed(self.urmom)
        np.random.shuffle(self.anon_names)
        processor = DirectoryProcessor(None, None)
        parser = OsuParser(None, self.songs, None)
        entry_idx = 0
        for dir in self.all_entries:
            anon_name = self.anon_names[entry_idx]
            print(dir, anon_name, sep='$')
            os.makedirs(self.anon_dir + anon_name, exist_ok=True)
            processor.change_work_dir(self.entry_dir + dir)
            processor.change_new_dir(self.anon_dir + anon_name)
            processor.get_all_files()
            processor.file_process()

            parser.change_work_file(processor.osufile)
            parser.assign_anon_name(anon_name)
            parser.save_file(parser.anon_osufile())
            parser.remove_old_file()

            entry_idx += 1
            

if __name__=='__main__':
    togepi = Togepi('./', '../Anon_entries/')
    togepi.get_all_entries()
    togepi.metronome()
