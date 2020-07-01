# README

## Table of Contents
   [I. Introduction](#I.-Introduction)<br>
  [II. Installation Instructions](#II.-Installation-Instructions)<br>
 [III. Usage Instructions](#III.-Usage-Instructions)<br>
  [IV. License](#IV.-License)<br>
  [V. Contributors](#V.-Contributors)<br>
 [VI. Citation](#VI.-Citation)<br>
[VII. Contact](#VII.-Contact)


## I. Introduction
This package can calculate the taxa resiliency for a provided tree. In effect, the question is as follows: "how resilient is the tree topology to the removal of taxa?" To determine this, we remove a taxon from the alignment and build a new tree, comparing it to the original tree. To avoid anomalies, a new tree is built multiple times (say 50). This process is repeated for each taxon. Thus, if 100 taxa are in a given tree and 50 replicates are performed for the removal of each taxon then 5,000
new trees are built. These new trees are compared with with the original tree
to see how frequently different clades appear.
The intent is to assign a value to each node, similar to bootstrapping, but the values have a very different meaning. A value of 1 indicates 100% of sampled trees includes the grouping in that clade (sans the one taxon intentionally removed). Valid values fit in the range [0,1]. Note that this value has no meaning for leaf nodes, parents of
leaf nodes, and the root node. Since our "sampling" (systematically removing
one taxon at a time) is  necessarily done without replacement, we use the
term "jackknife" to desribe how we make new sets of alignments and new trees. This term is something of a misnomer, but it is convenient.
Please note that this package assumes the following has already been performed:

1. The original alignment of all taxa
2. A tree built with all taxa
3. "jackknifing" the alignment (making one copy per taxon in the tree, minus that taxon)
4. New trees built using the "jackknifed" alignments with a pre-determined level of replication

The program must have access to all the relevant trees (_i.e._, the original/main
tree and the "jackknifed" trees) and a mapping of which trees are associated
with which taxa. A default directory structure and file naming scheme is assumed.
These assumptions can be modified to some degree, or bypassed entirely, with
certain command-line arguments. Please consult the section [III. Usage
Instructions](#III.-Usage-Instructions) for details.

We are in the process of publishing a paper describing this work. Once
available, we will provide relevant details here:

See our paper in [_journal_](#README) for further information:<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>[https://sub-domain.domain.tld/some/path/to/resource](#README)


## II. Installation Instructions
This package is written in [Python](https://www.python.org). You must have a version of Python (v3.6+) that supports [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings). This package also depends on the following Python modules: sys, re, pkgutil, argparse, and pathlib, which are all included by default in most Python installations. Installation may be accomplished using pip like this:

<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>`pip install taxaResiliency`

Alternately, you may install it manually using setuptools like this:

<span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>`python setup.py install`

If running `setup.py`, you may wish to add `--user` or `--prefix` for an
installation in non-default locations.

## III. Usage Instructions
Please run `taxaResil -h` or `taxaResil --help`.


## IV. License
Please see the [LICENSE](https://github.com/pickettbd/taxonResiliency/blob/master/LICENSE).


## V. Contributors
Brandon Pickett (Github: [@pickettbd](https://github.com/pickettbd)) is the sole author of this software.


## VI. Citation
Until a version of the paper is available, we ask that you cite the Github
repository. Thereafter, you will be able to include a citation following
this general form:

> Pickett BD, Powell GS, Ridge PG, Bybee SM. Paper title. _journal_. Year. Volume(Issue):pages.


## VII. Contact
For questions, comments, concerns, feature requests, suggestions, etc., please
open an issue on Github.

**Note:** Before asking for help, please ensure you (a) are using the latest
official release and (b) consult first the section [III. Usage Instructions](#III.-Usage-Instructions).

