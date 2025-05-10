# python-mini-projects

this is just a repo where im gonna dumb a lot of unrelated python mini projects, if the projects get too big they will be separated into their own repos

this is just a brief overview,each folder has its own readme, if the file isnt in a folder check the readme from here:

## Table of Contents

- [Habitica Quest Generator](#habitica-quest-generator)
- [Estimate read time](#estimate-read-time)
- [Anki wanikani mnemonics adder](#anki-wanikani-mnemonics-adder)
- [Subtitle files utility](#subtitle-files-utility)

## Habitica quest generator

**Description:** this script is quite good and refined, it will automatically add a questline from the json file you give it, to the app habitica, its very good in combination with something like chatgpt for generating the quests and then adding them to the todo app

**Technologies Used:** just normal standard libraries and some stuff for multi threading cuz who doesn't like cool CLI animations

**Instalation**

1. Download the repository.
2. Install requirements:

   ```bash
   pip install -r habitica_requirements.txt
   ```

3. Run:

   ```bash
   python habitica.py -f quest_lines/questline.json
   ```

## Estimate read time

**Description:** every site restricted the amount and size of documents i can scan at a time so i over engineered my own

**Technologies Used:** the colorama, fitz library along with basic python stuff like getopt and thats it lol

**Instalation**

1. Download the repository.
2. Install requirements:

   ```bash
   pip install -r estimate_read_time_requirements.txt
   ```

3. Run:

   ```bash
   python estimated_read_time.py -h
   ```

## Anki wanikani mnemonics adder

**Description:** this was supposed to be a one time run to add mnemonics to the 2k/6k deck on anki using the wanikani api, its extremely slow due to the rate limit of the api, please dont use :)

## Subtitle files utility

**Description:** I wanted to watch stuff with subtitles on vlc but the subtitles and the video names were different so it was annoying

**Instalation**

1. Download the repository.
2. Run:

   ```bash
   python subtitle_files_utility.py -h 
   ```
