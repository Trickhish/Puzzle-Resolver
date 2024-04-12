from PIL import Image
import math
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider
import time
import random

def cutImage(img, n):
    w,h = img.size
    xs, ys = math.floor(w/n), math.floor(h/n)

    il=[]
    for y in range(0, w, xs):
        for x in range(0, h, ys):
            pp = img.crop((x, y, min(w, x+xs), min(h, y+ys)))
            il.append(pp)
    
    return(il)

def updatePlot(sil, fig, axes):
    for i, subimage in enumerate(sil):
        ax = axes[i // 16, i % 16]
        ax.imshow(subimage)
        ax.axis('off')

    fig.canvas.draw()
    fig.canvas.flush_events()

def formatLen(n, l=2):
    n=str(n)
    while len(n)<l:
        n=" "+n
    return(n)

def printPuzzle(pl, ll=[]):
    cnb = int(math.sqrt(len(pl)))
    mln = len(str(len(pl)-1))

    print("")
    for y in range(cnb):
        for x in range(cnb):
            cdt = y*cnb+x

            if (pl[cdt]==-1):
                print("   ", end="")
                continue

            nb = formatLen(pl[cdt], mln)

            # red:\033[91m  green:\033[92m  blue:\033[94m  reset:\033[0m
            if cdt in ll:
                nb= "\033[91m"+nb+"\033[0m"
            else:
                nb= "\033[92m"+nb+"\033[0m"

            print(nb+" ", end="")
        print(" \n")
    print("-"*(cnb*3))

def markNeihbors(pc, w, ln, nbh):
    for nb in [pc-1, pc+1, pc-w, pc+w]:
        if nb>0 and nb<ln:
            nbh[nb]+=1

def findBestPiece(ct, nbh):
    mxi=0
    mxn=nbh[0]

    for i in range(1, len(ct)):
        if ct[i]==-1:
            if nbh[i]==4:
                return(i)
            elif nbh[i]>mxn:
                mxn=nbh[i]
                mxi=i
    
    return(mxi, mxn)

def sideScore(im1, im2, side):
    w,h = im1.size

    if side=='r':
        l1 = [im1.getpixel((w-1, y)) for y in range(h)]
        l2 = [im2.getpixel((0, y)) for y in range(h)]
    elif side=='l':
        l1 = [im1.getpixel((0, y)) for y in range(h)]
        l2 = [im2.getpixel((w-1, y)) for y in range(h)]
    elif side=='u':
        l1 = [im1.getpixel((x, 0)) for x in range(w)]
        l2 = [im2.getpixel((x, h-1)) for x in range(w)]
    elif side=='d':
        l1 = [im1.getpixel((x, h-1)) for x in range(w)]
        l2 = [im2.getpixel((x, 0)) for x in range(w)]
    
    ttdist=0
    for i in range(min(len(l1), len(l2))):
        c1 = l1[i]
        c2 = l2[i]

        ttdst = 0
        for ii in range(min(len(c1), len(c2))):
            dst = abs(c1[ii]-c2[ii])
            ttdist+=dst
        ttdist+=ttdst
    
    return(ttdist)
        


def fillPiece(il, pc, w, ln, ct):
    fnb = [(e, f) for (e, f) in [(pc-1, 'r'), (pc+1, 'l'), (pc-w, 'd'), (pc+w, 'u')] if e>0 and e<ln and ct[e]!=-1]
    
    # pc vide, ct[pc]=-1

    mx=0
    mxp=0
    for i in range(ln):
        if any(e==i for e in ct):
            continue

        sc=0
        for (p, s) in fnb:
            sc+=sideScore(il[ct[p]], il[i], s)
        if sc>mx:
            mx=sc
            mxp=i
    
    return(mxp)

def resolvePuzzle(il):
    ct = [-1 for i in range(pnb)]
    nbh = [0] * len(ct)

    fp = random.randint(0, len(ct))
    w = int(math.sqrt(len(ct)))
    mdl = (len(ct)//2) + w//2

    ct[mdl] = fp
    markNeihbors(mdl, w, len(ct), nbh)
    dpc = [mdl]

    printPuzzle(ct, dpc)

    (bp, bpn) = (mdl+1, 1)

    for i in range(5):
        ct[bp] = fillPiece(il, bp, w, len(ct), ct)
        dpc.append(bp)

        printPuzzle(ct, [bp])

        markNeihbors(bp, w, len(ct), nbh)
        (bp, bpn) = findBestPiece(ct, nbh)
        



i = Image.open("tk.jpg")
print("Image Loaded")

pnb = 64

sil = cutImage(i, math.sqrt(pnb))
print("Image Cut")

#fig, axes = plt.subplots(16, 16, figsize=(8, 8))
#plt.ion()

#ct = [-1 for i in range(pnb)]
#random.shuffle(ct)
#print("Puzzle Shuffled")

resolvePuzzle(sil)