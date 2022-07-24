# LMN-3-DrumConfigGenerator

A small python script, which automatically generates the drum kit configuration for the [LMN-3 DAW](https://github.com/FundamentalFrequency/LMN-3-DAW).

## Functionality

The script maps all files found in a given directory to a specified range of notes. Therefore, a mapping is provided through the config.yaml file, which specifies a regex for each note (e.g. "_BD" or "_HH"). 

The file which matches the regex is mapped to the corresponding note. If multiple files match the regex, the alphabetically first file is mapped to the note. The remaining files, which matched the regex, are mapped to the following notes.

All remaining files, which do not match any regex, are mapped to the remaining notes in a given range.

## Configuration

The script can be configured through the config.yaml file:
```YAML
### LMN-3 DrumConfigGenerator Configuration ###
# path: 
#   - path to the drum kits
# use_subfolders: 
#   - if true, multiple drum kits in subfolders are expected
#   - if false, only one drum kit in the specified path is expected
# note_range: 
#   - notes in this range are populated with remaining files, which were not used in the mapping
# mappings: 
#   - mapping for each note to a specific file
#   note_number: 
#     - number of the note
#   file_name_regex: 
#     - if the regex is found somewhere in a file name, the corresponding file is mapped to that note
#     - if multiple files are matching the given regex, the alphabetically first file is used. The remaining files, which matched the regex, are mapped to the following notes.
### 

path: "DrumKits"
use_subfolders: true
note_range:
  first_note: 53
  last_note: 76
mappings:
  - note_number: 53
    file_name_regex: "_BD"
  - note_number: 55
    file_name_regex: "_SN"
  - note_number: 61
    file_name_regex: "_HH"
  - note_number: 58
    file_name_regex: "_CP"
  - note_number: 63
    file_name_regex: "_OH"
  - note_number: 66
    file_name_regex: "_RD"
  - note_number: 68
    file_name_regex: "_CR"
```

## Example

The configuration file from above with these files in the subdirectory "606" in the "DrumKits" folder 
```
606_BD_01.wav  606_LT_01.wav
606_BD_02.wav  606_LT_02-001.wav
606_CR_01.wav  606_LT_02-002.wav
606_CR_02.wav  606_OH_01.wav
606_HH_01.wav  606_OH_02.wav
606_HH_02.wav  606_SN_01.wav
606_HT_01.wav  606_SN_02.wav
```

will generate the drum kit configuration file "606.yaml" in the corresponding folder:
```YAML
mappings:
- file_name: 606_BD_01.wav
  note_number: 53
- file_name: 606_BD_02.wav
  note_number: 54
- file_name: 606_SN_01.wav
  note_number: 55
- file_name: 606_SN_02.wav
  note_number: 56
- file_name: 606_HT_01.wav
  note_number: 57
- file_name: 606_LT_01.wav
  note_number: 58
- file_name: 606_LT_02-001.wav
  note_number: 59
- file_name: 606_LT_02-002.wav
  note_number: 60
- file_name: 606_HH_01.wav
  note_number: 61
- file_name: 606_HH_02.wav
  note_number: 62
- file_name: 606_OH_01.wav
  note_number: 63
- file_name: 606_OH_02.wav
  note_number: 64
- file_name: 606_CR_01.wav
  note_number: 68
- file_name: 606_CR_02.wav
  note_number: 69
name: '606'
```
