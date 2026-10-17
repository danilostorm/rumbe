#!/usr/bin/env python3
"""Summarize CD-ROM and DMA observations from local test logs without game content."""
import json,sys
rows=[]
for line in open(sys.argv[1],encoding='utf-8'):
    if line.startswith('SAMPLE '):
        record=json.loads(line[line.index('{'):]); d=record['d']; rows.append((record['v'],d[6],d[11],d[49],d[50],d[55],d[56],record.get('draw',0)))
print('vblank mdec_count disc_lba cd_int1 dma3_active mdec_in_active mdec_out_active draws')
for row in rows:print(*row)
if rows:
    print('Final sample:',rows[-1]);print('MDEC stalled:',len(rows)>=3 and len({r[1] for r in rows[-3:]})==1)
