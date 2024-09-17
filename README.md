# Pythonic P5R Parser Playground

*An experimental collection of Pythonic parsers for P5R file formats.*

## Basic Guide

The main purpose of this repo is to share some of the Python classes I use for file format research + the scripts that help to do so.
- In the `Formats/` directory, the actual parser classes (basically the equivalent of templates) are defined.
- In the `Scripts/` directory, there are examples of scripts/tests/mini-tools that use these classes for file reading, writing, editing, collating, research, etc.

## Usage

Most scripts should simply run with a relatively recent version of [Python](https://www.python.org/downloads/). They were developed on 3.12, but should largely be backward-compatible. They largely don't need additional libraries, but if you're using one of the image-processing parsers, those may use [NumPy](https://pypi.org/project/numpy/) and [Pillow](https://pypi.org/project/pillow/). If you want to use these, you can just run:

```bash
pip install -r requirements.txt
```

Then, to run a script such as `Scripts/ModFntMap.py`, call it like so:

```bash
python -m Scripts.ModFntMap
```

## Credits

- Many parsers here are translations of the templates found in [TGE](https://github.com/tge-was-taken)'s [010-Editor-Templates](https://github.com/tge-was-taken/010-Editor-Templates) (or, in some cases, [Secre-C](https://github.com/Secre-C)'s [fork](https://github.com/Secre-C/010-Editor-Templates) specifically).
  - Some of the parsers are also translations of those found in TGE's [Amicitia](https://github.com/tge-was-taken/Amicitia).
- Some parsers are for file types specific to [Meloman19](https://github.com/Meloman19)'s [PersonaEditor](https://github.com/Meloman19/PersonaEditor).
- The parsers are all built upon a prerelease version of [Pherakki](https://github.com/Pherakki)'s forthcoming `exbip` library.
  - (Possibly to be updated for the official release version of said library, which may change the code significantly... eventually.)
