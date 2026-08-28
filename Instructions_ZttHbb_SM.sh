####################################################################################################################################
################ Making the gridpack
####################################################################################################################################
# # https://cms-generators.docs.cern.ch/how-to-produce-gridpacks/powheg-box/
# cmsrel CMSSW_12_4_24_patch1 -n CMSSW_12_4_24_patch1_powheg
# cd CMSSW_12_4_24_patch1_powheg/src
# cmsenv
# git clone --depth=1 --single-branch https://github.com/cms-sw/genproductions.git         
# cd genproductions/bin/Powheg   

# using central gridpack and filtering at LHE level for tautau + pt cuts
########################### Hacking gridpack
### to remove the PDF weights that take a lot of time

tar -xvzf /cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg/v1/HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg.tgz 
# edit pwg-rwl.dat and remove all weights
# retar gridpack :
tar -cvzf ../HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg_noWeights.tgz *
cp HZJ_slc7_amd64_gcc700_CMSSW_10_6_27_ZH_HToBB_ZToLL_M125_13TeV_powheg_noWeights.tgz /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/



cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/MCGeneration

# move fragments
cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZttHbb_fragment.py /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src/Configuration/GenProduction/python/
cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZttHbb_fragment_VpTGt200.py /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src/Configuration/GenProduction/python/


########################################################
########### prod
### Nb of evts : 
## 2018
# inclusive : ~ 150k
# VpT > 200 : 14k

# efficiency of LHE filters : 41/200=0.2

python3 batchSubmitterMC_all.py \
--process ZttHbb_v1 \
--maxEvents 200 --nJobs 1 --start_from 2 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/pilot --no_exec

# 2k evts per job -> 10k evts at LHE
python3 batchSubmitterMC_all.py \
--process ZttHbb_v1 \
--maxEvents 10000 --nJobs 10 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2018 

# resubmit with less evts per job
# pilot
python3 batchSubmitterMC_all.py \
--process ZttHbb_17_v1 \
--maxEvents 100 --nThreads 1 --nJobs 1 --start_from 2 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2017_pilot


python3 batchSubmitterMC_all.py \
--process ZttHbb_17_v1 \
--maxEvents 1000 --nThreads 1 --nJobs 100 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2017 
python3 batchSubmitterMC_all.py \
--process ZttHbb_16_v1 \
--maxEvents 1000 --nThreads 1 --nJobs 100 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2016
python3 batchSubmitterMC_all.py \
--process ZttHbb_16_HIPM_v1 \
--maxEvents 1000 --nThreads 1 --nJobs 100 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2016_HIPM

# add events
python3 batchSubmitterMC_all.py \
--process ZttHbb_v1 \
--maxEvents 1000 --nThreads 1 --nJobs 100 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2018 
python3 batchSubmitterMC_all.py \
--process ZttHbb_17_v1 \
--maxEvents 1000 --nThreads 1 --nJobs 100 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2017 
python3 batchSubmitterMC_all.py \
--process ZttHbb_16_v1 \
--maxEvents 1000 --nThreads 1 --nJobs 100 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2016
python3 batchSubmitterMC_all.py \
--process ZttHbb_16_HIPM_v1 \
--maxEvents 1000 --nThreads 1 --nJobs 100 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2016_HIPM




############ merging
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/frameworkJobs && source setup.sh
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/merging

python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2018/ZttHbb_v1 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_18 --target-size 500 --remote-io --merge-report report-ZttHbb_v1_18.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2018/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2017/ZttHbb_v1 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_17b --target-size 500 --remote-io --merge-report report-ZttHbb_v1_17.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2017/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016/ZttHbb_v1 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_16b --target-size 500 --remote-io --merge-report report-ZttHbb_v1_16.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2016/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016_HIPM/ZttHbb_v1 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_16_HIPMb --target-size 500 --remote-io --merge-report report-ZttHbb_v1_16_HIPM.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v1/2016_HIPM/Step_6



########################################################
########### prod VpT filter
# efficiency : 12 / 1000 = 0.012
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_v1 \
--maxEvents 1000 --nJobs 1 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/pilot --no_exec

# 200 evts after filter per job = 17k at LHE (~2h to generate)
# 20k LHE & 100 jobs -> 24k final events
# 15k evts takes min 15mins to run LHE
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_v1 \
--maxEvents 15000 --nThreads 8 --nJobs 120 --start_from 3 --queue short  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2018
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_17_v1 \
--maxEvents 12000 --nThreads 8 --nJobs 150 --start_from 1 --queue short  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2017 
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_16_v1 \
--maxEvents 12000 --nThreads 8 --nJobs 150 --start_from 1 --queue short  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2016
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_16_HIPM_v1 \
--maxEvents 12000 --nThreads 8 --nJobs 150 --start_from 1 --queue short  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2016_HIPM


# going 1CPU
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 150 --start_from 200 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2018
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_17_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2017 
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_16_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2016
python3 batchSubmitterMC_all.py \
--process ZttHbb_VpTGt200_16_HIPM_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2016_HIPM


## merging
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2018/ZttHbb_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_VpTGt200_18 --target-size 500 --remote-io --merge-report report-ZttHbb_v1_VpTGt200_18.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2018/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2017/ZttHbb_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_VpTGt200_17b --target-size 500 --remote-io --merge-report report-ZttHbb_v1_VpTGt200_17.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2017/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016/ZttHbb_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_VpTGt200_16b --target-size 500 --remote-io --merge-report report-ZttHbb_v1_VpTGt200_16.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2016/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016_HIPM/ZttHbb_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZttHbb_v1_VpTGt200_16_HIPMb --target-size 500 --remote-io --merge-report report-ZttHbb_v1_VpTGt200_16_HIPM.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_VpTGt200_v1/2016_HIPM/Step_6

####### new filters

python3 batchSubmitterMC_all.py \
--process ZttHbb_17_v2 \
--maxEvents 100 --nThreads 1 --nJobs 2 --start_from 3 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2017_pilot --no_exec

python3 batchSubmitterMC_all.py \
--process ZttHbb_18_v2 \
--maxEvents 30000 --nThreads 8 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2018 

python3 batchSubmitterMC_all.py \
--process ZttHbb_17_v2 \
--maxEvents 30000 --nThreads 8 --nJobs 100 --start_from 200 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2017 

python3 batchSubmitterMC_all.py \
--process ZttHbb_16_v2 \
--maxEvents 30000 --nThreads 8 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2016

python3 batchSubmitterMC_all.py \
--process ZttHbb_16_HIPM_v2 \
--maxEvents 30000 --nThreads 8 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2016_HIPM 

for i in $(seq 10 30); do 
# condor_prio -p 9 456653.$i; 
# condor_prio -p 9 456651.$i; 
#condor_prio -p 9 456652.$i; 
condor_release 456653.$i;
condor_prio -p 100 456653.$i;
done

condor_qedit 456653 RequestMemory 15720




## merging
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/frameworkJobs && source setup.sh
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/merging

python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2018/ZttHbb_v2 --work-dir /scratch/cuisset/tmp/ZttHbb_v2_18 --target-size 500 --remote-io --merge-report report-ZttHbb_v2_18.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2018/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2017/ZttHbb_v2 --work-dir /scratch/cuisset/tmp/ZttHbb_v2_17b --target-size 500 --remote-io --merge-report report-ZttHbb_v2_17.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2017/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016/ZttHbb_v2 --work-dir /scratch/cuisset/tmp/ZttHbb_v2_16b --target-size 500 --remote-io --merge-report report-ZttHbb_v2_16.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2016/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016_HIPM/ZttHbb_v2 --work-dir /scratch/cuisset/tmp/ZttHbb_v2_16_HIPMb --target-size 500 --remote-io --merge-report report-ZttHbb_v2_16_HIPM.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZttHbb_v2/2016_HIPM/Step_6

