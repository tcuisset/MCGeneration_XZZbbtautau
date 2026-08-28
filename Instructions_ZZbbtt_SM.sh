####################################################################################################################################
################ Making the card
####################################################################################################################################
Copy the folders with the cards into `genproductions/bin/MadGraph5_aMCatNLO`
Then run `./gridpack_generation.sh <NameOfOutputInProcCard> <pathToCardFolder>`


cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO

cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZZbbtt_nonres/card_leptonCuts/* ZZTo2B2Tau_leptonCuts/

NB_CORE=5 ./gridpack_generation.sh ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX ZZTo2B2Tau_leptonCuts




####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/MCGeneration

# move fragments
cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZZbbtt_fragment.py /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src/Configuration/GenProduction/python/
cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZZbbtt_fragment_LHEFilter.py /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src/Configuration/GenProduction/python/
cp /grid_mnt/vol_home/llr/cms/cuisset/bbtautau/ZZbbtautau/MCGeneration/ZZbbtt_fragment_LHEFilter_before_shower.py /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_47/src/Configuration/GenProduction/python/

### Editing JobMaterializeLimit : sets nb of max_materialize jobs. Set to 0 to stop starting new jobs but keepin running ones
condor_qedit 404791 JobMaterializeLimit 0

# pilot
python3 batchSubmitterMC_all.py \
--process ZZbbtt_v1 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 50 --nJobs 1 --start_from 5 --queue short --max-materialize 5 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/


python3 batchSubmitterMC_all.py \
--process ZZbbtt_v1 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 5000 --nJobs 40 --start_from 25 --queue long --max-materialize 5 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1/



# LHEFilter
# NB : the nb of events is the nb of events generated at LHE before filtering, so need to divide by filter efficiency to get the wanted nb of events (eff is ~2.901e-02 for VpT>200) -> for 5k events need 200k at LHE
python3 batchSubmitterMC_all.py \
--process ZZbbtt_v1_LHEFilter \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 200000 --nJobs 10 --start_from 3 --queue long --max-materialize 3 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter/


# ZZbbtt_v1_LHEFilter_before_shower
# a bit bugged v1
python3 batchSubmitterMC_all.py \
--process ZZbbtt_v1_LHEFilter_before_shower \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 200000 --nJobs 20 --start_from 1 --queue long --max-materialize 5 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower/


# v2
#  condor_qedit 402112 JobMaterializeLimit 25
python3 batchSubmitterMC_all.py \
--process ZZbbtt_v1_LHEFilter_before_shower \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 200000 --nJobs 20 --start_from 100 --queue long --max-materialize 10 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_attempt2/

python3 batchSubmitterMC_all.py \
--process ZZbbtt_v1_LHEFilter_before_shower \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 200000 --nJobs 60 --start_from 120 --queue long --max-materialize 20 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_attempt2/


# v2 no LHE filter
python3 batchSubmitterMC_all.py \
--process ZZbbtt_v1 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 3000 --nJobs 40 --start_from 130 --queue long --max-materialize 15 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_leptonCuts/



######################################################################## Other years
######################## LHE filter
## pilot
python3 batchSubmitterMC_all.py \
--process ZZbbtt_16_v1_LHEFilter_before_shower \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 2000 --nJobs 1 --start_from 1 --queue long --max-materialize 15 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_multiYears/pilot_2016 --no_exec
ZZbbtt_16_HIPM_v1

# main run : 20k evts per year
# 20k /(20k*(2,901e-02)) = 35 jobs (makes 580 evts per job)
python3 batchSubmitterMC_all.py \
--process ZZbbtt_17_v1_LHEFilter_before_shower \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 20000 --nJobs 35 --start_from 1 --queue long --max-materialize 20 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_multiYears/2017

python3 batchSubmitterMC_all.py \
--process ZZbbtt_16_v1_LHEFilter_before_shower \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 20000 --nJobs 35 --start_from 1 --queue long --max-materialize 20 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_multiYears/2016

python3 batchSubmitterMC_all.py \
--process ZZbbtt_16_HIPM_v1_LHEFilter_before_shower \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 20000 --nJobs 35 --start_from 1 --queue long --max-materialize 20 \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_multiYears/2016_HIPM



##################### inclusive
# main run : 100k evts per year
# 30 jobs at 3k evts per job
# --max-materialize 10
python3 batchSubmitterMC_all.py \
--process ZZbbtt_17_v1 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 3000 --nJobs 20 --start_from 21 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_multiYears/2017

python3 batchSubmitterMC_all.py \
--process ZZbbtt_16_v1 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 3000 --nJobs 20 --start_from 21 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_multiYears/2016

python3 batchSubmitterMC_all.py \
--process ZZbbtt_16_HIPM_v1 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/ZZTo2B2Tau01j_leptonCuts_5f_NLO_FXFX_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 3000 --nJobs 20 --start_from 21 --queue long  \
--base /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_multiYears/2016_HIPM


############ merging
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/ZZbbtt_v1_VptGt200 --work-dir /scratch/cuisset/tmp/ZZbbtt_VptGt200 --target-size 500 --remote-io --merge-report report-ZZbbtt_v1_VptGt200.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower/Step_6 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_attempt2/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2017/ZZbbtt_v1_VptGt200 --work-dir /scratch/cuisset/tmp/ZZbbtt_VptGt200_17 --target-size 500 --remote-io --merge-report report-ZZbbtt_17_VptGt200.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_multiYears/2017/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016/ZZbbtt_v1_VptGt200 --work-dir /scratch/cuisset/tmp/ZZbbtt_VptGt200_16 --target-size 500 --remote-io --merge-report report-ZZbbtt_16_VptGt200.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_multiYears/2016/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016_HIPM/ZZbbtt_v1_VptGt200 --work-dir /scratch/cuisset/tmp/ZZbbtt_VptGt200_16_HIPM --target-size 500 --remote-io --merge-report report-ZZbbtt_16_HIPM_VptGt200.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_LHEFilter_before_shower_multiYears/2016_HIPM/Step_6

python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2018/ZZbbtt_v1_inclusive --work-dir /scratch/cuisset/tmp/ZZbbtt_18_inclusive --target-size 500 --remote-io --merge-report report-ZZbbtt_18_inclusive.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/ZZbbtt_v1_2018_tempResults
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2017/ZZbbtt_v1_inclusive --work-dir /scratch/cuisset/tmp/ZZbbtt_17_inclusive --target-size 500 --remote-io --merge-report report-ZZbbtt_17_inclusive.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_multiYears/2017/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016/ZZbbtt_v1_inclusive --work-dir /scratch/cuisset/tmp/ZZbbtt_16_inclusive --target-size 500 --remote-io --merge-report report-ZZbbtt_16_inclusive.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_multiYears/2016/Step_6
python3 /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/boostedTausProd/haddnanoEx.py --output-dir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/DNNTrainingSamples/2016_HIPM/ZZbbtt_v1_inclusive --work-dir /scratch/cuisset/tmp/ZZbbtt_16_HIPM_inclusive --target-size 500 --remote-io --merge-report report-ZZbbtt_16_HIPM_inclusive.txt /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/ZZbbtt_v1_multiYears/2016_HIPM/Step_6
