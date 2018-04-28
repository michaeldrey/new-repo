
<#
.DESCRIPTION
	This script will download and install KB4056898 (Spector) patch onto a list of hosts. 
  The script pulls from an external file source. Set the hostList source before you run. 
  One host per line.
.NOTES
	Author	: Mike Dreyfus
#>
##############################################################
##Set where to read your list of servers. One server per line.
##############################################################
$hostList = "C:\Path\to\server\list.txt"

######################################################################################################
## This section will download the script
## Since this is running as a job it may error here as it's not waiting for the insall to complete
## you can simply remove the asjob flag in the Invoke-Webrequest to work around this, however, it will
## take longer depending on the number of hosts.
######################################################################################################
foreach ($serverName in (get-content $hostList))
{	
	Write-Host "Downloading patch onto $serverName"
	Invoke-Command -ComputerName $serverName -ScriptBlock {
	Invoke-WebRequest http://download.windowsupdate.com/c/msdownload/update/software/secu/2018/01/windows8.1-kb4056898-v2-x64_754f420c1d505f4666437d06ac97175109631bf2.msu -OutFile c:\windows8.1-kb4056898.msu
	} -AsJob
}
Write-Output "All Downloads finished"	
##########################################
## Section install and verifies the hotfix
##########################################
Write-Output "Installing patch on hosts. This could take a while"
psexec -s @$hostList wusa C:\windows8.1-kb4056898.msu /passive /quiet /norestart 2> $null
Write-Output "Verifying host installs"
foreach ($serverName in (get-content $hostList))
{		
	Invoke-Command -ComputerName $serverName -ScriptBlock { Get-HotFix -id KB4056898 }
}
###############################
##Section enables registry keys
###############################
foreach ($serverName in (get-content $hostList))
{	
	Write-Host "Enabling Registry keys for $serverName"
	Invoke-Command -ComputerName $serverName -ScriptBlock {
		reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverride /t REG_DWORD /d 0 /f
		reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverrideMask /t REG_DWORD /d 3 /f
		reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization" /v MinVmVersionForCpuBasedMitigations /t REG_SZ /d "1.0" /f
	}
}
Write-Output "Complete"
###########################################
## Issues restarts to apply patch
## Comment out this section to skip reboots
###########################################
Write-Output "Issuing restarts"
foreach ($serverName in (get-content $hostList))
{	
	Write-Host "Restarting $serverName"
	Invoke-Command -ComputerName $serverName -ScriptBlock {
		Restart-Computer -Force
	}
}
Write-Output "Complete"
