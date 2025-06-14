Create an Installer MSI package that executes an arbitrary command to exploit an `AlwaysInstallElevated` policy.

Instructions:
* May require [HeatWave](https://www.firegiant.com/docs/heatwave/) to build in Visual Studio.
* Change the "RunMe" custom action of Package.wxs with your custom command.
* The installer intentionally fails after executing the command. This allows it to be used again without needing an uninstall/upgrade.