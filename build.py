# -*- coding: utf-8 -*-

import fontforge
import datetime
import textwrap
import argparse
import psMat
import json
import csv
import os
import sys

version = '1.2.0'
today = datetime.date.today()

parser = argparse.ArgumentParser()
parser.add_argument('ricty')
parser.add_argument('firacode')
parser.add_argument('out_font')
parser.add_argument('weight')
parser.add_argument('discord')
options = parser.parse_args(sys.argv[1:])

if options.discord == 'true':
    fontname = 'RictyDiminishedDiscordWithFiraCode'
    familyname = 'Ricty Diminished Discord with Fira Code'
else:
    fontname = 'RictyDiminishedWithFiraCode'
    familyname = 'Ricty Diminished with Fira Code'
weight = options.weight

ricty = fontforge.open(options.ricty)
firacode = fontforge.open(options.firacode)

# Load ligatures data and create data to generate feature file
with open('ligatures.csv', 'r') as file:
    ligatures_reader = csv.reader(file, delimiter=' ')

    ligatures = []
    nullable_glyphs = []
    glyphs = []

    for [components, source_type, name] in ligatures_reader:
        glyphs.append((source_type, name))
        component_names = list(map(lambda c: ricty[ord(c)].glyphname, list(components)))

        nullable_glyphs.extend(component_names[:-1])

        ligatures.append({
            'glyph': name,
            'components': component_names,
            'lookup': '_'.join(map(lambda name: name.upper(), component_names)),
        })

# Unique
nullable_glyphs = list(set(nullable_glyphs))

# Dump data
with open('data.json', 'w') as file:
    file.write(json.dumps({
        'ligatures': ligatures,
        'nullable_glyphs': nullable_glyphs,
    }))

# Copy needed glyphs from Fira Code font to Ricty
for (source_type, name) in glyphs:
    ricty.createChar(-1, name)

    if source_type == 'svg':
        ricty[name].importOutlines('svg/{}.{}.svg'.format(name, weight))
        ricty[name].width = 500
    elif source_type == 'glf':
        firacode.selection.select(name)
        firacode.copy()
        ricty.selection.select(name)
        ricty.paste()

        ricty.transform(psMat.compose(psMat.scale(500 / 1200), psMat.translate(0, 50)))
        ricty[name].width = 500

# Import Powerline glyphs
powerline_codes = [0xE0A0, 0xE0A1, 0xE0A2, 0xE0B0, 0xE0B1, 0xE0B2, 0xE0B3]

for codepoint in powerline_codes:
    ricty.createChar(codepoint)
    firacode.selection.select(('unicode',), codepoint)
    firacode.copy()
    ricty.selection.select(('unicode',), codepoint)
    ricty.paste()

# Modify glyphs

# Branch
ricty[0xE0A0].transform(psMat.translate(-50, 0))
# Line Number
ricty[0xE0A1].transform(psMat.translate(-50, 0))
# Locked
ricty[0xE0A2].transform(psMat.scale(500 / 600))

# Reset widths
for codepoint in powerline_codes:
    ricty[codepoint].width = 500

# Set font name
ricty.familyname = familyname
ricty.fontname = '{}-{}'.format(fontname, weight)
ricty.fullname = '{} {}'.format(familyname, weight)
ricty.weight = weight

# Set base version of the font
ricty.version = version

# Unset other version names to make them auto-calculated by FontForge
ricty.sfntRevision = None
ricty.woffMajor = None
ricty.woffMinor = None

ricty.copyright = textwrap.dedent('''\
    Copyright (c) 2012-2014 Yasunori Yusa
    Copyright (c) 2006 Raph Levien
    Copyright (c) 2006-2013 itouhiro
    Copyright (c) 2002-2013 M+ FONTS PROJECT
    Copyright (c) 2014 Mozilla Foundation
    Copyright (c) 2014 Telefonica S.A.
    Copyright (c) 2014 Nikita Prokopov
    Copyright (c) 2014 The Fira Code Project Authors (https://github.com/tonsky/FiraCode)
    Copyright (c) 2016-2019 Koki Takahashi
    License:
    SIL Open Font License Version 1.1 (http://scripts.sil.org/ofl)
''')

with open('LICENSE') as file:
    ricty.appendSFNTName('English (US)', 'License', file.read())

ricty.appendSFNTName('English (US)', 'License URL', 'http://scripts.sil.org/OFL')

ricty.appendSFNTName('English (US)', 'UniqueID', '{} {} : {} : {}'.format(familyname, weight, version, today.isoformat()))

# Export
try:
    os.remove(options.out_font)
except OSError:
    pass
ricty.generate(options.out_font)
