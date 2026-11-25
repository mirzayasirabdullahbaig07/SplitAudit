"""Prepare Yu et al. 2025 E. coli data for SplitAudit (streams the Rtab; low memory).
usage: python prepare_yu_ecoli.py <Rtab.gz> <metadata_checkm.csv(tsv)> <out_dir> [min_prev]
Writes: genes.npz (uint8 matrix genomes x kept genes, gene names, genome ids), meta_by_genome.csv
Frequency filter (genes present in fewer than min_prev or more than 1-min_prev of all genomes) is unsupervised
and applied to all genomes before any split; it is stated as a limitation in the manuscript."""
import sys, gzip, numpy as np, pandas as pd
rtab, meta, out = sys.argv[1:4]; lo = float(sys.argv[4]) if len(sys.argv)>4 else 0.05
rows=[]; names=[]
with gzip.open(rtab,'rt') as f:
    ids=f.readline().rstrip('\n').split('\t')[1:]; n=len(ids); total=0
    for line in f:
        total+=1
        t=line.rstrip('\n').split('\t'); v=np.array(t[1:],dtype=np.uint8)
        p=v.mean()
        if lo<=p<=1-lo: rows.append(v); names.append(t[0])
X=np.vstack(rows).T; print('genes total',total,'kept',X.shape[1],'genomes',X.shape[0])
np.savez_compressed(out+'/genes.npz',X=X,genes=np.array(names),ids=np.array(ids))
m=pd.read_csv(meta,sep='\t',low_memory=False)
m['genome_id']=m.genome_id.astype(str)
print('id overlap',len(set(ids)&set(m.genome_id)),'of',len(ids))
