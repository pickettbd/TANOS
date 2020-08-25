#! /bin/bash

tail -n +9 "${BASH_SOURCE[0]}" | head -n -1 | fold -s

exit 0

# Everything below this line is simple documentation
:'
This should be really be done manually. Simply copy the alignment file from wherever you presently have a copy to this project directory. The next step assumes it will be in the data/orig directory and named supermatrix_dna.phy. It is possible to change the name (manually). You could also modify the next step to run with amino acid alignments instead of nucleotide alignments.
'
