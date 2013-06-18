## Preparing a Build Environment

1. Download ISO of Fedora 18 DVD 64-bit from http://fedoraproject.org/en/get-fedora-options#formats.
1. Create a VM with 64 GB of disk and 2 GB of RAM. (Recommended to "Pre-allocate disk space", so that thin provisioning does not cause the VM to continuously increase in size)
1. Attached ISO to VM, boot VM, and start installer.
1. Remove lv_home volume, if any; expand lv_root volume to maximum size.
1. ...
1. Boot VM.
1. Follow http://boxgrinder.org/tutorials/boxgrinder-build-quick-start/installation/.
1. `yum -y install qemu VirtualBox` (else boxgrinder errs)
1. `gem install multidisk-boxgrinder-plugin`
1. Change `SELINUX=enforcing` to `SELINUX=permissive` in /etc/sysconfig/selinux in boxgrinding VM.
1. `export LIBGUESTFS_ATTACH_METHOD=appliance` so that boxgrinder will build (recommended to add to ~/.bashrc).
1. Modify /usr/share/gems/gems/boxgrinder-build-0.10.4/lib/boxgrinder-build/plugins/os/fedora/fedora-plugin.rb so that SUPPORTED_VERSIONS includes '18'.
1. Patch guestfs and kickstart generation with `cd /; patch -p1 <~/appliance/boxgrinder.patch` (boxgrinder.patch is found in this repo)

To build VMWare-ready VMs:
`alias bv="setarch i386 /root/appliance50/boxgrinder/boxgrinder-build -f appliance50.appl -p vmware --platform-config type:personal,thin_disk:true --debug"
alias bv64="/root/appliance50/boxgrinder/boxgrinder-build-64 -f appliance50.appl -p vmware --platform-config type:personal,thin_disk:true --debug"`

Execute either 'bv' (for 32-bit) or 'bv64' (for 64-bit) when in the boxgrinder directory. The above alias commands are useful in ~/.bashrc.

## References

* http://fedoraproject.org/wiki/How_to_create_an_RPM_package
