#!/usr/bin/env python3
"""Read-only analysis of NASCAR Rumble opening stream sectors in Mode2/2352 BIN.
Private disc path supplied by operator. Does not extract or copy game media.
"""
from pathlib import Path
from collections import Counter
import argparse,json
RAW=2352
def main():
  ap=argparse.ArgumentParser()
  ap.add_argument("bin",type=Path)
  ap.add_argument("--intro-start",type=int,default=93447)
  ap.add_argument("--intro-end",type=int,default=97407)
  args=ap.parse_args()
  s=args.intro_start;e=args.intro_end
  total=args.bin.stat().st_size//RAW
  assert args.bin.stat().st_size%RAW==0, "Not a full 2352-byte sector image"
  assert 16 < s < e < total
  sectors=Counter();mode=Counter();invalid_sync=[];submode_transitions=[];last=None
  with args.bin.open("rb") as f:
    for lba in range(s-5,e+10):
      f.seek(lba*RAW)
      sec=f.read(RAW)
      if sec[:12]!=b'\x00'+b'\xff'*10+b'\x00':
        invalid_sync.append(lba)
      sector_mode=sec[15]
      submode=sec[18] if sector_mode==2 else -1
      mode[sector_mode]+=1
      sectors[submode]+=1
      if submode!=last:
        submode_transitions.append((lba,submode))
        last=submode
  report={"total_raw_sectors":total,"intro_first":s,"intro_last_inclusive":e-1,
          "intro_sector_count":e-s,"mode_counts":dict(mode),
          "xa_submode_counts":dict(sectors),"invalid_sync_lbas":invalid_sync[:15],
          "submode_transitions":submode_transitions[:35],
          "transition_count":len(submode_transitions)}
  print(json.dumps(report,indent=2))
  if invalid_sync: raise SystemExit("Corrupted sync markers in opening sequence")
if __name__=="__main__":main()
