<#
.DESCRIPTION
	This script will download and install and run the speculation check onto a list of hosts. 
  The script pulls from an external file source. Set the hostList source before you run. One host per line.
  Run this after you install and reboot the system.
.NOTES
	Author	: Mike Dreyfus
#>
#####################################################
## Set path to your host list here. One host per line
#####################################################

$hostList = "C:\path\to\servers.txt"

foreach ($serverName in (get-content $hostList))
{	
	Write-Host "*+*+*+*+*+*+*+*+*+Downloading SpeculationControl Check onto $serverName *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+"
	Invoke-Command -ComputerName $serverName -ScriptBlock {
		Invoke-WebRequest https://gallery.technet.microsoft.com/scriptcenter/Speculation-Control-e36f0050/file/190138/1/SpeculationControl.zip -OutFile c:\SpeculationControl.zip
	}
	Write-Host "Installing and Running SpeculationControl Check onto $serverName"
	Invoke-Command -ComputerName $serverName -ScriptBlock {
		unzip c:\SpeculationControl.zip
		cd .\SpeculationControl
		$SaveExecutionPolicy = Get-ExecutionPolicy 
		Set-ExecutionPolicy RemoteSigned -Scope Currentuser -Force
		Import-Module .\SpeculationControl.psd1
		Get-SpeculationControlSettings 
		Set-ExecutionPolicy $SaveExecutionPolicy -Scope Currentuser -Force
	}
	Write-Host "*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+"
}
