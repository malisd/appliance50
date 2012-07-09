## Preparing a Build Environment

1. Download ISO of Fedora 17 DVD 32-bit from http://fedoraproject.org/en/get-fedora-options#formats.
1. Create a VM with 64 GB of disk and 2 GB of RAM.
1. Attached ISO to VM, boot VM, and start installer.
1. Remove lv_home volume, if any; expand lv_root volume to maximum size.
1. ...
1. Boot VM.
1. Follow http://fedoraproject.org/wiki/How_to_create_an_RPM_package#Preparing_your_system.
1. Follow http://boxgrinder.org/tutorials/boxgrinder-build-quick-start/installation/.
1. `yum install qemu` (else boxgrinder errs)
1. gem install multidisk-boxgrinder-plugin
1. `su -c 'yum localinstall --nogpgcheck http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm'`
1. `yum install VirtualBox`
1. Change `SELINUX=enforcing` to `SELINUX=permissive` in /etc/sysconfig/selinux in boxgrinding VM.

## References

* http://fedoraproject.org/wiki/How_to_create_an_RPM_package
