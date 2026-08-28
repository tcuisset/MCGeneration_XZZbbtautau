####################################################################################################################################
################ Making the gridpack
####################################################################################################################################

# using central gridpack and filtering at LHE level for tautau + pt cuts
# /cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/HZJ_HanythingJ_NNPDF31_13TeV_M125/v1/HZJ_HanythingJ_NNPDF31_13TeV_M125.tgz

########################### Hacking gridpack
### to remove the PDF weights that take a lot of time

tar --extract --file /cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/HZJ_HanythingJ_NNPDF31_13TeV_M125/v1/HZJ_HanythingJ_NNPDF31_13TeV_M125.tgz
# edit pwg-rwl.dat and remove all weights
# retar gridpack :
tar -cvzf ../HZJ_HanythingJ_NNPDF31_13TeV_M125_noWeights.tgz *
cp HZJ_HanythingJ_NNPDF31_13TeV_M125_noWeights.tgz /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/



cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/MCGeneration

# move fragments
cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZbbHtt_fragment.py /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src/Configuration/GenProduction/python/
cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZbbHtt_fragment_VpTGt200.py /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src/Configuration/GenProduction/python/
scram b

########################################################
########### prod
### Nb of events
## 2018
# inclusive : 30k
# VpT>200   : 14k


# 20% filter efficiency
# pilot
python3 batchSubmitterMC_all.py \
--process ZbbHtt_v1 \
--maxEvents 100 --nThreads 1 --nJobs 1 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2018_pilot --no_exec

# 400 evts per job
python3 batchSubmitterMC_all.py \
--process ZbbHtt_v1 \
--maxEvents 2000 --nThreads 1 --nJobs 100 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2018
python3 batchSubmitterMC_all.py \
--process ZbbHtt_17_v1 \
--maxEvents 2000 --nThreads 1 --nJobs 100 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2017 
python3 batchSubmitterMC_all.py \
--process ZbbHtt_16_v1 \
--maxEvents 2000 --nThreads 1 --nJobs 100 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2016
python3 batchSubmitterMC_all.py \
--process ZbbHtt_16_HIPM_v1 \
--maxEvents 2000 --nThreads 1 --nJobs 100 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2016_HIPM




############################################################################
#### VptGt200
# pilot
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_v1 \
--maxEvents 2000 --nThreads 8 --nJobs 1 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2018_pilot --no_exec

python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2018
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_17_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2017 
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_16_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2016
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_16_HIPM_v1 \
--maxEvents 10000 --nThreads 1 --nJobs 200 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2016_HIPM


# should make ~700 evts/job
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_v1 \
--maxEvents 100000 --nThreads 8 --nJobs 20 --start_from 200 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2018
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_17_v1 \
--maxEvents 100000 --nThreads 8 --nJobs 20 --start_from 200 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2017 
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_16_v1 \
--maxEvents 100000 --nThreads 8 --nJobs 20 --start_from 200 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2016
python3 batchSubmitterMC_all.py \
--process ZbbHtt_VpTGt200_16_HIPM_v1 \
--maxEvents 100000 --nThreads 8 --nJobs 20 --start_from 200 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2016_HIPM

## merging
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/frameworkJobs && source setup.sh
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/merging
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --ignore-empty --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2018/ZbbHtt_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZbbHtt_v1_VpTGt200_18b --target-size 500 --remote-io --merge-report report-ZbbHtt_v1_VpTGt200_18.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2018/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --ignore-empty --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2017/ZbbHtt_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZbbHtt_v1_VpTGt200_17b --target-size 500 --remote-io --merge-report report-ZbbHtt_v1_VpTGt200_17.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2017/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --ignore-empty --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016/ZbbHtt_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZbbHtt_v1_VpTGt200_16b --target-size 500 --remote-io --merge-report report-ZbbHtt_v1_VpTGt200_16.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2016/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --ignore-empty --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016_HIPM/ZbbHtt_v1_VpTGt200 --work-dir /scratch/cuisset/tmp/ZbbHtt_v1_VpTGt200_16_HIPMb --target-size 500 --remote-io --merge-report report-ZbbHtt_v1_VpTGt200_16_HIPM.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_VpTGt200_v1/2016_HIPM/Step_6



####### new filters
### inclusive v2 
# filter eff is ~6/100
python3 batchSubmitterMC_all.py \
--process ZbbHtt_18_v2 \
--maxEvents 100 --nThreads 1 --nJobs 1 --start_from 1 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2018_pilot --no_exec

# 
### TODO this was accidentally set to output in ZttHbb_v2 !!!! Need to fish out the correct ones
### 
python3 batchSubmitterMC_all.py \
--process ZbbHtt_18_v2 \
--maxEvents 10000 --nThreads 8 --nJobs 45 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2018 
python3 batchSubmitterMC_all.py \
--process ZbbHtt_17_v2 \
--maxEvents 10000 --nThreads 8 --nJobs 50 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2017 
python3 batchSubmitterMC_all.py \
--process ZbbHtt_16_v2 \
--maxEvents 10000 --nThreads 8 --nJobs 50 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2016
python3 batchSubmitterMC_all.py \
--process ZbbHtt_16_HIPM_v2 \
--maxEvents 10000 --nThreads 8 --nJobs 50 --start_from 100 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2016_HIPM 

for i in $(seq 11 20); do 
condor_prio -p +10 457106.$i 457107.$i 457108.$i 457109.$i;
done

## merging
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/frameworkJobs && source setup.sh
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/merging

python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2018/ZbbHtt_v2 --work-dir /scratch/cuisset/tmp/ZbbHtt_v2_18 --target-size 500 --remote-io --merge-report report-ZbbHtt_v2_18.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2018/Step_6 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2018/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2017/ZbbHtt_v2 --work-dir /scratch/cuisset/tmp/ZbbHtt_v2_17b --target-size 500 --remote-io --merge-report report-ZbbHtt_v2_17.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2017/Step_6 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2017/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016/ZbbHtt_v2 --work-dir /scratch/cuisset/tmp/ZbbHtt_v2_16b --target-size 500 --remote-io --merge-report report-ZbbHtt_v2_16.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2016/Step_6 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2016/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016_HIPM/ZbbHtt_v2 --work-dir /scratch/cuisset/tmp/ZbbHtt_v2_16_HIPMb --target-size 500 --remote-io --merge-report report-ZbbHtt_v2_16_HIPM.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v1/2016_HIPM/Step_6 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZbbHtt_v2/2016_HIPM/Step_6

