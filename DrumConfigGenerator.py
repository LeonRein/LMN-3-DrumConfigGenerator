from __future__ import annotations
from genericpath import isdir

import os
import re
from dataclasses import dataclass
from glob import glob
from string import digits
from typing import Dict, List

import yaml

class SubConfigGenerator:
    @dataclass
    class File:
        path: str
        prio: int
        regex: str
        
    @classmethod
    def __get_files(cls, path: str, notes_regex: Dict) -> Dict[str, int]:
        files = map(os.path.basename, glob(os.path.join(path, "*.wav")))
        file_dict = {}
        for file in files:
            for regex in notes_regex.values():
                if re.search(regex, file):
                    file_dict[file] = cls.File(file, 0, regex)
                    break
            
            if file in file_dict:
                continue
            
            regex = re.escape(file)
            regex = re.sub("\\d+", "\\\d+", regex)

            file_dict[file] = cls.File(file, 0, regex)

        return file_dict

    @classmethod
    def __init_drum_config(cls, name) -> Dict:
        drum_config = {}
        drum_config["name"] = name
        drum_config["mappings"] = []

        return drum_config

    @classmethod
    def __init_notes(cls, config: Dict) -> Dict[int, str]:
        notes = {}
        note_range = config["note_range"]
        for note in range(int(note_range["first_note"]), int(note_range["last_note"])):
            notes[note] = None

        return notes

    @classmethod
    def __init_notes_mapping(cls, config) -> Dict[int, str]:
        notes_mapping = {}
        for mapping in config["mappings"]:
            notes_mapping[int(mapping["note_number"])] = mapping["file_name_regex"]

        return notes_mapping

    def __init__(self, path, config) -> None:
        self.path = os.path.abspath(path)
        self.drum_config : Dict = self.__init_drum_config(os.path.basename(os.path.normpath(self.path)))
        self.notes : Dict[int, str] = self.__init_notes(config)
        self.notes_regex : Dict[int, str] = self.__init_notes_mapping(config)
        self.file_dict : Dict[str, self.File] = self.__get_files(path, self.notes_regex)

    def __assign_note(self, note: int, file: SubConfigGenerator.File):
        self.notes[note] = file
        del(self.file_dict[file.path])
        files = self.__get_files_by_regex(file.regex)
        for cur_file in files:
            cur_file.prio -= 1

    def __get_files_by_regex(self, regex) -> List[str]:
        files = []
        for file in self.file_dict.values():
            if file.regex == regex:
                files.append(file)
        files = sorted(files, key=lambda x: x.path)
        return files

    def __get_highest_prio_file(self) -> List[str]:
        if len(self.file_dict) == 0:
            return None
        highest_prio = float('-inf')
        for file in self.file_dict.values():
            if file.prio > highest_prio:
                highest_prio = file.prio

        files = []

        for file in self.file_dict.values():
            if file.prio == highest_prio:
                files.append(file)

        files = sorted(files, key=lambda x: x.path)
        return files[0]

    def __get_lowest_prio_note(self) -> List[str]:
        lowest_prio = float('inf')
        for note in self.notes.values():
            if note == None:
                lowest_prio = float('-inf')
            elif note.prio < lowest_prio:
                lowest_prio = note.prio

        for note in self.notes:
            if self.notes[note] == None or self.notes[note].prio == lowest_prio:
                return note

        return None

    def __assign_unused_files(self) -> bool:
        while True:
            note = self.__get_lowest_prio_note()
            if note is None:
                break
            file = self.__get_highest_prio_file()
            if file is None:
                break
            if self.notes[note] is not None:
                if file.prio <= self.notes[note].prio:
                    break
            self.__assign_note(note, file)

    def __write_drum_config(self) -> None:
        mappings: List = self.drum_config["mappings"]
        for note in self.notes:
            mapping = {}
            mapping["note_number"] = note
            mapping["file_name"] = self.notes[note].path
            mappings.append(mapping)

        with open(os.path.join(self.path, self.drum_config["name"] + ".yaml"), "w") as file:
            yaml.dump(self.drum_config, file)

    def gen_drum_config(self):
        for note in self.notes_regex:
            files = self.__get_files_by_regex(self.notes_regex[note])
            cur_note = note
            while True:
                if len(files) == 0:
                    break
                self.__assign_note(cur_note, files.pop(0))
                if cur_note + 1 in self.notes_regex:
                    break
                cur_note += 1

        self.__assign_unused_files()

        self.__write_drum_config()
 

class DrumConfigGenerator:
    @classmethod
    def __get_subfolders(cls, path) -> List[str]:
        subfolders = []
        for dir in os.listdir(path):
            full_dir = os.path.join(path, dir)
            wav_files = glob(os.path.join(full_dir, "*.wav"))
            if len(wav_files) > 0:
                subfolders.append(full_dir)
        return subfolders
    

    @classmethod
    def __read_config(cls) -> Dict:
        config = {}
        with open("config.yaml", "r") as config_file:
            config =  yaml.load(config_file)
        return config

    def gen_drum_config(self) -> None:
        for dir in self.subfolders:
            scg = SubConfigGenerator(dir, self.config)
            scg.gen_drum_config()

    def __init__(self) -> None:
        self.config = self.__read_config()


        self.path = self.config["path"]
        self.use_subfolders = bool(self.config["use_subfolders"])

        if self.use_subfolders:
            self.subfolders = self.__get_subfolders(self.path)
        else:
            self.subfolders = [self.path]

        if len(self.subfolders) == 0:
            return


if __name__ == "__main__":
    dcg = DrumConfigGenerator()
    dcg.gen_drum_config()
