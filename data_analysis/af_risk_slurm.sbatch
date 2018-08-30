#!/bin/bash

#SBATCH --job-name af_induced_risk
#SBATCH --time 0-72:00:00
#SBATCH --array=503,513,534,535,543,544,548,549,550,551,552,553,554,555,556,560,561,562,565,566,567,568-596,681-692 %50
#SBATCH --mail-type END
#SBATCH --mail-user mff113@imperial.ac.uk


# Copy input file (called in this case input_file) to the directory job will
# run in. Slurm will start in the directory you submit your job from - so be
# sure this is in the home or data directory as workspace isn't shared between
# nodes.
# Run program (test_prog.x in this example).
echo Executing in /home/mff113/Documents/projects/Atrial-Fibrillation-CMP/ on $(hostname)
nice -n 19
module load python
python gen_risk_curve_data.py $SLURM_ARRAY_TASK_ID
