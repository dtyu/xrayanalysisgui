#!../../bin/linux-x86/mtrSim

## You may have to change motorSim to something else
## everywhere it appears in this file

< envPaths
cd ${TOP}

## Register all support components
dbLoadDatabase("dbd/mtrSim.dbd",0,0)
mtrSim_registerRecordDeviceDriver(pdbbase) 

## Load record instances
dbLoadTemplate("db/sensor.substitutions")
dbLoadTemplate("db/motorSim.substitutions")

# Create simulated motors: ( start card , start axis , low limit, high limit, home posn, # cards, # axes to setup)
motorSimCreate( 0, 0, -32000, 32000, 0, 1, 4 )
# Setup the Asyn layer (portname, low-level driver drvet name, card, number of axes on card)
drvAsynMotorConfigure("motorSim1", "motorSim", 0, 4)

## autosave/restore machinery
save_restoreSet_Debug(0)
save_restoreSet_IncompleteSetsOk(1)
save_restoreSet_DatedBackupFiles(1)
#save_restoreSet_status_prefix("test:")

set_savefile_path("${TOP}/as","/save")
set_requestfile_path("${TOP}/as","/req")

set_pass0_restoreFile("motorSim_positions.sav")
set_pass0_restoreFile("motorSim_settings.sav")
set_pass1_restoreFile("motorSim_settings.sav")

cd ${TOP}/iocBoot/${IOC}
iocInit()

## more autosave/restore machinery
create_monitor_set("motorSim_positions.req", 5 , "P=test:")
create_monitor_set("motorSim_settings.req", 15 , "P=test:")
