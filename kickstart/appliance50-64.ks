############################################################################
## Kickstart Options
############################################################################

cdrom
firstboot --disable
install
keyboard us
#network --onboot=yes --device=eth0 --bootproto=dhcp --noipv6 --nameserver=8.8.8.8
lang en_US.UTF-8
repo --cost=1 --name=os --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-18&arch=x86_64
repo --cost=1 --name=fedora-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-debug-18&arch=x86_64
repo --cost=1 --name=updates --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-f18&arch=x86_64
repo --cost=1 --name=updates-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-debug-f18&arch=x86_64
rootpw --plaintext crimson
selinux --permissive
timezone --utc America/New_York
xconfig --startxonboot


############################################################################
## Package Selection
############################################################################

%packages

# base
@base-x

# core
@core

# avoids
# Unable to create appliance : Unable to install grub2 bootloader
grub2

# release; cannot be installed by update50 due to grub2 dependencies
generic-logos
generic-release
-fedora-logos
-fedora-release
-fedora-release-notes

# necessary packages for update50
unzip

#prevent "Unable to run ['/usr/bin/firewall-offline-cmd', '--enabled']!" error
firewall-config
#@xfce-desktop

%end


############################################################################
## Post-installation Script
############################################################################

%post

# lock root (because doing so in appliance50 RPM alone doesn't work when boxgrinding or kickstarting)
/usr/bin/passwd -l root

# finish configuration after a boot
/bin/cat > /etc/rc.d/rc.local << "EOF"
#!/bin/bash

# ensure networking has enough time to start
/bin/sleep 10

# download and run the updater
#TODO update URL
/bin/curl -o /tmp/updater50 http://docs.danallan.net/cs50/updater
/bin/chmod +x /tmp/updater50
/tmp/updater50

# install Parallels Tools, VirtualBox Guest Additions, or VMware Tools
declare vmm=$(/bin/grep vmm= /proc/cmdline)
declare regex='vmm=(\w+)'
if [[ "$vmm" =~ $regex ]]
then
    case ${BASH_REMATCH[1]} in
    parallels)
        # download and mount Parallels Tools
        # /Applications/Parallels Desktop.app/Contents/Resources/Tools/prl-tools-lin.iso
        /usr/bin/wget --directory-prefix=/tmp http://mirror.cs50.net/appliance50/18a/source/iso/prl-tools-lin.iso
        /bin/mount -r -o loop -t iso9660 /tmp/prl-tools-lin.iso /mnt

        # install Parallels Tools
        /mnt/install --install-unattended
        /bin/rm -f /home/jharvard/Desktop/Parallels\ Shared\ Folders

        # tidy up
        /bin/umount /mnt
        /bin/rm -f /tmp/prl-tools-lin.iso
    ;;
    vbox)
        # download and mount VirtualBox Guest Additions
        # http://download.virtualbox.org/virtualbox/4.2.2/VBoxGuestAdditions_4.2.2.iso
        /usr/bin/wget --directory-prefix=/tmp http://mirror.cs50.net/appliance50/18a/source/iso/VBoxGuestAdditions_4.2.2.iso
        /bin/mount -r -o loop -t iso9660 /tmp/VBoxGuestAdditions_4.2.2.iso /mnt

        # install VirtualBox Guest Additions
        /mnt/VBoxLinuxAdditions.run --nox11

        # tidy up
        /bin/umount /mnt
        /bin/rm -f /tmp/VBoxGuestAdditions_4.2.2.iso
    ;;
    vmware)
        # download and mount VMware Tools
        # http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/5.0.1/825449/packages/com.vmware.fusion.tools.linux.zip.tar
        /usr/bin/wget --directory-prefix=/tmp http://mirror.cs50.net/appliance50/18a/source/iso/linux.iso
        /bin/mount -r -o loop -t iso9660 /tmp/linux.iso /mnt
        /bin/tar xf /mnt/VMwareTools-9.2.2-893683.tar.gz -C /tmp

        ## convince VMware Tools to install within VirtualBox
        #/bin/echo "#!/bin/bash" >> /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
        #/bin/echo "/bin/echo 'good'" >> /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
        #/bin/echo "/bin/true" >> /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
        #/bin/chmod a+x /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm

        # install VMware Tools
        /tmp/vmware-tools-distrib/vmware-install.pl -d

        # tidy up
        /bin/rm -rf /tmp/vmware-tools-distrib
        /bin/umount /mnt
        /bin/rm -f /tmp/linux.iso
    ;;
    *)
        # custom password for EC2 (trim leading and trailing whitespace)
        # http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/AESDG-chapter-instancedata.html
        PASSWORD=`/usr/bin/wget --output-document=- --quiet --timeout=5 --tries=10 http://169.254.169.254/latest/user-data`
        if [ $? -eq 0 ]; then
            PASSWORD=`/bin/echo "$PASSWORD" | /usr/bin/perl -p -e 's/^\s*(.*)\s*$/$1/g'`
        if [ ! -z "$PASSWORD" ]; then
            /bin/echo "$PASSWORD" | /usr/bin/passwd --stdin jharvard
            /bin/echo -e "$PASSWORD\n$PASSWORD" | /usr/bin/smbpasswd -a -s jharvard 
            /bin/mysqladmin -u jharvard -p"crimson" password "$PASSWORD"
        fi
        /bin/rm -f /etc/sysconfig/network-scripts/ifcfg-eth1
        /bin/rm -f /etc/sysconfig/network-scripts/ifcfg-eth2
        fi
    ;;
   esac
fi
/bin/rm -f /etc/rc.d/rc.local
/bin/rm -f /root/*
/usr/sbin/poweroff
EOF
/bin/chmod 755 /etc/rc.d/rc.local


############################################################################
# clean up
############################################################################

# delete yum's cache
/usr/bin/yum clean all
/usr/bin/yum clean metadata
/bin/rm -rf /var/cache/yum/*

# delete temporary files
/bin/rm -f /root/*
/bin/rm -rf /tmp/.[^.]* && /bin/rm -rf /tmp/..?*

# fill disk with 0s, to facilitate disk's compression
/bin/cat /dev/zero > /tmp/zero.fill
/bin/sync
/bin/sleep 1
/bin/sync
/bin/rm -f /tmp/zero.fill


%end
