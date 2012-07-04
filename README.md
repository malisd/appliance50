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

## References

* http://fedoraproject.org/wiki/How_to_create_an_RPM_package
