#! /bin/bash

# Ensure we're running from the correct location
CWD_check()
{
	#local SCRIPTS_DIR
	local MAIN_DIR
	local RUN_DIR

	SCRIPTS_DIR=$(readlink -f `dirname "${BASH_SOURCE[0]}"`)
	MAIN_DIR=$(readlink -f `dirname "${SCRIPTS_DIR}/"`)
	RUN_DIR=$(readlink -f .)

	if [ "${RUN_DIR}" != "${MAIN_DIR}" ] || ! [[ "${SCRIPTS_DIR}" =~ ^"${MAIN_DIR}"/scripts.* ]]
	then
		printf "\n\t%s\n\t%s\n\n" "Script must be run from ${MAIN_DIR}" "You are currently at:   ${RUN_DIR}" 1>&2
		exit 1
	fi
}
CWD_check

# ###################################### #
# sanity check on input and output files #
# ###################################### #

# define key variables
DATA_DIR="data"
INPUT_ALN="${DATA_DIR}/orig/supermatrix_dna.phy"
OUTPUT_ALN_DIR="${DATA_DIR}/jackknife/aln"

# check for existence of needed input files
EXIT_EARLY=0
INPUT_FILES=("${INPUT_ALN}")

declare -a NON_EXIST_INPUT_FILES
for INPUT_FILE in "${INPUT_FILES[@]}"
do
	if ! [ -e "${INPUT_FILE}" ]
	then
		NON_EXIST_INPUT_FILES+=("${INPUT_FILE}")
	fi
done

if [ ${#NON_EXIST_INPUT_FILES} -gt 0 ]
then
	printf "%s\n" "Some necessary input files did not exist; we will not proceed. The missing files" "are as follows:" 1>&2
	printf "\t\"%s\"\n" "${NON_EXIST_INPUT_FILES[@]}" 1>&2
	EXIT_EARLY=1
fi
unset NON_EXIST_INPUT_FILES INPUT_FILES

if [ $EXIT_EARLY -ne 0 ]
then
	exit $EXIT_EARLY
fi

# create output directories, if needed
mkdir -p "${OUTPUT_ALN_DIR}" &> /dev/null

# "jackknife" the alnignments. In other words, for an alignment with n taxa,
# create n copies of the alignment where each alignment is missing a single
# taxa. Each taxa should be missing from only a single alignment.
module purge
module load python/3.7.3
time python3 "${SCRIPTS_DIR}"/03-jackknifeAlignment.py "${INPUT_ALN}" "${OUTPUT_ALN_DIR}"
exit $?

