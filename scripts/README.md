# TANOS Helper Scripts for Taxon Jackknifing

These scripts are intended to be run in order. They assume a specific directory
structure and specific file names. If you choose to use them, please review them
careful before executing them. These are intended as examples only.

## Usage Instructions

First, note that these scripts assume a very specific directory structure. Before
you do anything, you should create a new project directory and create this
directory stucture. The directory structure looks like this:

```
|-- data
|   |-- jackknife
|   |   |-- aln
|   |   `-- tree
|   |       |-- Taxon_1
|   |       |-- Taxon_2
|   |       |-- Taxon_3
|   |       |-- ...
|   |       |-- ...
|   |       |-- ...
|   |       `-- Taxon_N
|   |-- mainTree
|   |-- modelTest
|   `-- orig
|-- job_files
`-- scripts
```

You can create this directory structure with the following simple commands:

```
cd /path/to/your/project/directory
mkdir -p data/{jackknife/{aln,tree},mainTree,modelTest,orig} job_files scripts
```

You will need to place all the example scripts in the `scripts` directory. The
SLURM stdout and stderr files will automatically be placed in the `job_files`
directory. All of the data and results will be in the `data` directory. If you
already have a primary tree that you wish to score, you will be able to skip
steps 0-2, but you will need to ensure the resultant files are in the correct
location, so you should still read the details for those steps. The following
will contain basic usage instructions and potential "gotchas" for each step.

**NOTE:** All scripts are written to be run from the main project directory,
_not_ from inside `scripts` or `data` or its subdirectories.

### Initial Data Transfer: 00-copyOriginalData.sh

This script doesn't do anything other than write a message to the screen. Your objective is to copy the alignment file, presumably in .phy format.

```
cd /path/to/your/project/directory
./scripts/00-copyOriginalData.sh
```

### Model Test: 01-iqtreeModelTest.submit

If you do not already have a tree, steps 1 and 2 will create the tree for you.
To save time in building all the trees in step 4, we will re-use the model
selected from model selection on the main tree. You could, of course, require
model selection for each jackknifed tree if desired. `01-iqtreeModelTest.submit`
takes zero or one parameters. If you wish to run model selection on your local
machine or login node, simply run with zero parameters like this:

```
cd /path/to/your/project/directory
./scripts/01-iqtreeModelTest.submit
```

A simple message will be printed to the screen that can be copied to run
`01-iqtreeModelTest.slurm` locally. To have model selection run as a job on the
cluster, simply run it like this:

```
cd /path/to/your/project/directory
./scripts/01-iqtreeModelTest.submit cluster
```

**NOTE:** If you wish to edit the IQ-TREE command, see line 121 of the slurm
script. IQ-TREE is put in your path via the command `module load iqtree`; please,
delete or modify as necessary (line 68). Memory provided to the job is calculated
at the top of the slurm script. It assumes certain SLURM environment variables
are set and that memory values are in megabytes. If you need to modify resource
requests or add quality of service or other misc. options, see the sbatch command
in the submission script (line 44). Expected input files and directory structure
is specified near line 83 of the submission script; visit there to modify the
input alignment file's name.

### Tree Inference for Primary Tree: 02-iqtreeTree.submit

The previous step could be combined with this step by modifying the command in
the slurm script if desired. I separated things for the sake of modularity. You
will need to modify the model parameter on line 55 of the submission script based
on the output from the previous step. Once modified, you can submit the job to
the cluster like this:

```
cd /path/to/your/project/directory
./scripts/02-iqtreeTree.submit
```

**NOTE:** If you wish to edit the IQ-TREE command, see line 122 of the slurm
script. IQ-TREE is put in your path via the command `module load iqtree`; please,
delete or modify as necessary (line 68). Memory provided to the job is calculated
at the top of the slurm script. It assumes certain SLURM environment variables
are set and that memory values are in megabytes. If you need to modify resource
requests or add quality of service or other misc. options, see the sbatch command
in the submission script (line 34). Expected input files and directory structure
is specified near line 53 of the submission script; visit there to modify the
input alignment file's name. Be sure to change the MODEL variable on line 55 to
match the report from the previous step.

### Alignment Jackknifing: 03-jackknifeAlignment.sh

This step can be run locally / on the login node. You will call the shell
script `03-jackknifeAlignment.sh`, which will in turn run the Python script
sharing the same name (but ending in .py):

```
cd /path/to/your/project/directory
./scripts/03-jackknifeAlignment.sh
```

**NOTE:** The python script is written in Python 3, and it accepts two arguments.
_caveat emptor_: it does not do any argument checking/validating. You can modify
the assumed directory structure or input file name near line 26 of the shell
script. The appropriate binary for python is placed in the environment PATH via
the command `module load python/3.7.3`; please, delete or modify as necessary
(line 64). The actual call to python is made on line 65. The python script works
for alignments in only PHYLIP format.

### Tree Inference for Jackknifed Trees: 04-iqtreeJackknife.submit

This script is written to handle the most difficult step of the process. In
effect, this is just step 2 again, but for r\*n trees, where r is the number of
replicates and n is the number of taxa. Gratefully multiple jobs can be run at
the same time in parallel. Despite this, as jobs finish (successfully and/or
unsuccessfully), it would be very time-consuming to ascertain which jobs finished
successfully and which ones did not. Resubmitting a subset of the jobs would also
be time-consuming. This script is intended to resolve those problems. The core
aspect of the script that enables this is a check that decides whether a specific
tree has been generated yet (even if an attempt has been made unsuccessfully
previously). This check works with only IQ-TREE output because it relies on
IQ-TREE's checkpoint files. If you wish to use something other than IQ-TREE, you
would need to devise another method of determining whether the output tree was
successfully generated. As jobs finish, you may (but should not need to) view
the stdout and stderr files in the `job_files` directory. Any time jobs need to
be (re-)submitted, you may do so like this:

```
cd /path/to/your/project/directory
./scripts/04-iqtreeJackknife.submit
```

**NOTE:** If you wish to edit the IQ-TREE command, see line 174 of the slurm
script. IQ-TREE is put in your path via the command `module load iqtree`; please,
delete or modify as necessary (line 104). Memory provided to the job is calculated
at the top of the slurm script. It assumes certain SLURM environment variables
are set and that memory values are in megabytes. If you need to modify resource
requests or add quality of service or other misc. options, see the sbatch command
in the submission script (line 74). Expected input files and directory structure
is specified near line 94 of the submission script; visit there to modify the
number of jobs to run at once (per taxon!) and the number or replicates desired.
Be sure to change the MODEL variable on line 99 to match the report from step 1.
As this generates r\*n jobs, many processes across multiple nodes will be writing
to the same storage device at the same time. This will be a significant load for
any drive, and it may cripple NSF drives. Accordingly, the slurm script starts
and ends the job by copying data to and from the local drive on the node, which
is assumed to be mounted at /tmp. Double check with your sys. admins. whether
this is done correctly for your cluster. Note that this job will attempt to
clean itself up if time runs out or a kill signal (except SIGKILL, which cannot
be caught) is sent. In the event of some kind of system failure or variance of
your system from mine, you may have to clean up the /tmp directories of the nodes
you used manually. A record of which job ran on which node is created for your
convenience and record in the main project directory (cleanup.tsv).

