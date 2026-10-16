#!/usr/bin/env python3
"""Read-only ISO9660 directory audit for a user-provided PS1 Mode2/2352 BIN.
No game data is copied, patched, uploaded, or redistributed.
"""
import argparse
from pathlib import Path

SECTOR=2352
DATA_OFFSET=24

def scan_image(path):
    with open(path,"rb") as fh:
        def sector(lba):
            fh.seek(lba*SECTOR+DATA_OFFSET)
            data=fh.read(2048)
            if len(data)<2048: raise ValueError("Truncated ISO image")
            return data
        pvd=sector(16)
        if pvd[1:6] != b"CD001": raise ValueError("Not ISO9660")
        root=pvd[156:190]
        def walk(extent,size,prefix="",depth=0):
            if depth>8: return
            blocks=(size+2047)//2048
            if blocks>10000: raise ValueError("Unexpected huge directory")
            buf=b"".join(sector(extent+i) for i in range(blocks))[:size]
            i=0
            while i<len(buf):
                if buf[i]==0:
                    i=(i//2048+1)*2048
                    continue
                n=buf[i];entry=buf[i:i+n];i+=n
                if len(entry)<34: break
                name=entry[33:33+entry[32]].decode("latin1")
                if name in ("\x00","\x01"): continue
                block=int.from_bytes(entry[2:6],"little")
                length=int.from_bytes(entry[10:14],"little")
                folder=bool(entry[25]&2)
                yield prefix+"/"+name,block,block+(length+2047)//2048,folder
                if folder:yield from walk(block,length,prefix+"/"+name,depth+1)
        yield from walk(int.from_bytes(root[2:6],"little"),int.from_bytes(root[10:14],"little"))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("disc",type=Path,help="Path to personally provided NASCAR Rumble .bin")
    args=parser.parse_args()
    entries=list(scan_image(args.disc))
    for name,start,end,folder in entries:
        if folder or name.startswith("/CW/OPENING/") or name.startswith("/DUMMY"):
            print(("DIR " if folder else "FILE"),name,":",start,"..",end-1)
    opening=next((v for v in entries if v[0].upper().endswith("/OPENING/INTRO.WVE;1")),None)
    if opening:
        print("Opening WVE logical sector interval",opening[1],opening[2],
              "(end exclusive)")
if __name__=="__main__":main()
