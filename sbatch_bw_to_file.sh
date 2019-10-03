#!/bin/bash
#SBATCH --nodes=1
#SBATCH --mem=300G                    # Memory total in MB (for all cores)
#SBATCH -o jjyu_%j.out                 # File to which STDOUT will be written, including job ID
#SBATCH -e jjyu_%j.err                 # File to which STDERR will be written, including job ID
#SBATCH --mail-type=FAIL                    # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=jjyu@jimmy.harvard.edu   # Email to which notifications will be sent

# >>> conda init >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$(CONDA_REPORT_ERRORS=false '/homes/jjyu/miniconda3/bin/conda' shell.bash hook 2> /dev/null)"
if [ $? -eq 0 ]; then
    \eval "$__conda_setup"
else
    if [ -f "/homes/jjyu/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/homes/jjyu/miniconda3/etc/profile.d/conda.sh"
        CONDA_CHANGEPS1=false conda activate base
    else
        \export PATH="/homes/jjyu/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda init <<<
#for sample in 0 1 2 3 4 
for sample in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
do
		conda activate higlass
		python bw_to_bedfile_kraken.py $sample  & 
done
