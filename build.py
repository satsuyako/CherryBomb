from fontmake import __main__
from fontTools.ttLib import TTFont, newTable
import shutil
import subprocess
from glyphsLib.cli import main
import ufoLib2
import ufo2ft
import os

print ("Converting to UFO")
main(("glyphs2ufo", "sources/CherryBomb.glyphs"))

exportFont = ufoLib2.Font.open("sources/CherryBombOne-Regular.ufo")

exportFont.lib['com.github.googlei18n.ufo2ft.filters'] = [{
    "name": "flattenComponents",
    "pre": 1,
}]

print ("Compiling")
static_ttf = ufo2ft.compileTTF(exportFont, removeOverlaps=True)

static_ttf["DSIG"] = newTable("DSIG")
static_ttf["DSIG"].ulVersion = 1
static_ttf["DSIG"].usFlag = 0
static_ttf["DSIG"].usNumSigs = 0
static_ttf["DSIG"].signatureRecords = []
static_ttf["head"].flags |= 1 << 3        #sets flag to always round PPEM to integer

print ("[Cherry Bomb One] Saving")
static_ttf.save("fonts/ttf/CherryBombOne-Regular.ttf")

shutil.rmtree("sources/CherryBombOne-Regular.ufo")
os.remove("sources/CherryBomb.designspace")

subprocess.check_call(
        [
            "ttfautohint",
            "--stem-width",
            "nsn",
            "fonts/ttf/CherryBombOne-Regular.ttf",
            "fonts/ttf/CherryBombOne-Regular-hinted.ttf",
        ]
    )
shutil.move("fonts/ttf/CherryBombOne-Regular-hinted.ttf", "fonts/ttf/CherryBombOne-Regular.ttf")