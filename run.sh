#!/bin/bash
help__()
{
  echo "Usage: `basename ${0}` -m <MasterPhone> -p <PartnerPhone> -n <MasterPhoneNumber> [-r <ROUND>]"
  echo "Options: These are optional argument"
  echo " -m <MasterPhone>       - Master phone adb device serial"
  echo " -p <PartnerPhone>      - Partner phone adb device serial"
  echo " -n <MasterPhoneNumber> - Master phone number, using by call handling"
  echo " [-r <round>]           - Round of testing, default is round=1 "
  echo " [ -d report folder]     - report folder, default is device name"   
  echo " -t <tag>  default is MTBF"
  echo ""
  echo " Example:"
  printf '\e[1;31m'
  echo "        `basename ${0}` -m CB5A1TQNA0 -p CB51246PTS -n 1341020138 -r 10"
  printf '\e[0m'
  exit 1
}

upload()
{
    echo
}

LOGINFOMATION=0
RunTag=MTBF
REPORTS=''
while getopts m:p:n:r:t:d:Ih opt
do
  case "${opt}" in
    m) MUT1=${OPTARG};;
    p) MUT2=${OPTARG};;
    n) PHONE=${OPTARG};;
    r) ROUND=${OPTARG};;
    t) RunTag=${OPTARG};;
    d) REPORTS=${OPTARG};;
    I) LOGINFOMATION=1;;
    h) help__;;
    \?) help__;;
  esac
done
#####Parameters checking #########
if [[ -z "$MUT1" ]] 
then
    help__
fi

if [ -z "$ROUND" ]; then
    ROUND=1
fi

if [ -z "$REPORTS" ]; then
    REPORTS=$MUT1
fi
if [ $LOGINFOMATION -eq 1 ]; then
    LOG_INFO="--loglevel TRACE"
fi

echo Master Phone is: $MUT1
echo Partner phone is: $MUT2
echo Master phone num: $PHONE

adb -s $MUT1 root
adb -s $MUT1 remount


#### Precondition #########


#### Log Starts #########
mkdir ${REPORTS}
adb -s $MUT1 logcat -v time -b main > ${REPORTS}/main_log.txt &

#######################
#   Run Test Case     #
#######################
for((index=1;index<=$ROUND;index++))
{
    CREATED_TIME=`date +%F_%H%M%S`
    echo ${CREATED_TIME} "###Run Test Case for Round #$index"
    echo "========================================"
    pybot $LOG_INFO --include=${RunTag} -d ${REPORTS}/stability_report_${CREATED_TIME} --variable MUT1:$MUT1 StabilityKPI
}

############End of Logcat ###########
for logcatPID in `adb -s $MASTER shell ps -x | grep logcat | awk '{print $2}'`
do
    adb -s $MUT1 shell kill $logcatPID
done



#######################
#   Generate Report   #
#######################
RobotsReports=
cd ${REPORTS}
for d in `find . -name "output.xml" -print`
{
    RobotsReports="$REPORTS $d "
}

rebot --name StablityKPI -x result.xml ${RobotsReports}
