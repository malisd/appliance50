## Preparing a Build Environment

1. Place all files on a publicly-accessible web server.
1. Unzip "appliance50.zip" to overwrite appliance50/. Be sure to preserve permissions.
1. Update the following variables:
 * baseurl in appliance50/etc/yum.repos.d/appliance50.repo
 * URL in appliance50/usr/local/bin/update50
 * URL in updater
 * URL in install50
1. Run prepare-archive, which builds a new appliance50.zip file.
1. Build a new VM by booting a Fedora install DVD on a machine (virtual or bare-metal) and run the kickstart:
linux ks=http://URL-to-files/appliance50.ks
