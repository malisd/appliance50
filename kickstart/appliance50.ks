############################################################################
## Kickstart Options
############################################################################

cdrom
firstboot --disable
install
keyboard us
lang en_US.UTF-8
repo --cost=1 --name=os --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-17&arch=i386
repo --cost=1 --name=fedora-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-debug-17&arch=i386
repo --cost=1 --name=updates --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-f17&arch=i386
repo --cost=1 --name=updates-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-debug-f17&arch=i386
repo --cost=2 --name=appliance50 --baseurl=http://mirror-local.cs50.net/appliance50/17/i386/RPMS/
repo --cost=3 --name=dropbox --baseurl=http://linux.dropbox.com/fedora/17/
repo --cost=3 --name=google-chrome --baseurl=http://dl.google.com/linux/chrome/rpm/stable/i386/
repo --cost=3 --name=nodejs-stable --baseurl=http://nodejs.tchol.org/stable/f17/i386/
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

# per https://bugzilla.redhat.com/show_bug.cgi?id=547152, avoids
# Unable to disable SELinux because the installed package set did not include the file /usr/sbin/lokkit
system-config-firewall-base

# release
generic-logos
generic-release
-fedora-logos
-fedora-release
-fedora-release-notes

# fonts
dejavu-fonts-common
dejavu-sans-fonts
dejavu-sans-mono-fonts
dejavu-serif-fonts

# CS50
appliance50

# Xfce
@xfce-desktop

# unwanted
-audit
-leafpad
-libpcap
-ModemManager
-openssh-askpass
-orage
-ppp
-xfce4-power-manager
-xscreensaver-base

%end


############################################################################
## Post-installation Script
############################################################################

%post

# lock root (because doing so in appliance50 RPM alone doesn't work when boxgrinding or kickstarting)
/usr/bin/passwd -l root

# reinstall to ensure appliance's RPM overwrites other RPMs' files
/usr/bin/yum -y reinstall appliance50

## unwanted, but - doesn't suffice above
/usr/bin/yum -y remove \
abrt \
dnsmasq \
NetworkManager \
NetworkManager-gnome \
wpa_supplicant

# finish configuration after a boot
/bin/cat > /etc/rc.d/rc.local << "EOF"
#!/bin/bash

# ensure networking has enough time to start
/bin/sleep 10

# re-install appliance's RPM (to configure MySQL)
/usr/bin/yum -y reinstall appliance50

# install VirtualBox Guest Additions or VMware Tools
declare vmm=$(/bin/grep vmm= /proc/cmdline)
declare regex='vmm=(\w+)'
if [[ "$vmm" =~ $regex ]]
then
    case ${BASH_REMATCH[1]} in
    vbox)
        # download and mount VirtualBox Guest Additions
        /usr/bin/wget --directory-prefix=/tmp http://download.virtualbox.org/virtualbox/4.1.22/VBoxGuestAdditions_4.1.22.iso
        /bin/mount -r -o loop -t iso9660 /tmp/VBoxGuestAdditions_4.1.22.iso /mnt

        # install VirtualBox Guest Additions
        /mnt/VBoxLinuxAdditions.run --nox11

        # tidy up
        /bin/umount /mnt
        /bin/rm -f /tmp/VBoxGuestAdditions_4.1.22.iso
    ;;
    vmware)
        # download and mount VMware Tools ISO
        #/usr/bin/wget --directory-prefix=/tmp http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/4.1.3/730298/packages/com.vmware.fusion.tools.linux.zip.tar
        /usr/bin/wget --directory-prefix=/tmp http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/5.0.1/825449/packages/com.vmware.fusion.tools.linux.zip.tar
        /bin/tar xf /tmp/com.vmware.fusion.tools.linux.zip.tar -C /tmp
        /usr/bin/unzip /tmp/com.vmware.fusion.tools.linux.zip -d /tmp
        /bin/mount -r -o loop -t iso9660 /tmp/payload/linux.iso /mnt
        #/bin/tar xf /mnt/VMwareTools-8.8.4-730257.tar.gz -C /tmp
        /bin/tar xf /mnt/VMwareTools-9.2.1-818201.tar.gz -C /tmp
        #/bin/rm -f /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm

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
        /bin/rm -rf /tmp/payload
        /bin/rm -f /tmp/com.vmware.fusion.tools.linux.zip
        /bin/rm -f /tmp/com.vmware.fusion.tools.linux.zip.tar
    ;;
    esac
fi
/bin/rm -f /etc/rc.d/rc.local
/bin/rm -f /root/*
/usr/bin/poweroff
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

# fill disk with 0s, to facilitate VMDK's compression
/bin/cat /dev/zero > /tmp/zero.fill
/bin/sync
/bin/sleep 1
/bin/sync
/bin/rm -f /tmp/zero.fill


%end
