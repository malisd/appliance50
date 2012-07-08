%include appliance50.ks

bootloader --append="biosdevname=0 quiet rhgb" --location=mbr

# necessary, per https://bugzilla.redhat.com/show_bug.cgi?id=752216#c10
#clearpart --all --initlabel

# compels Anaconda to prompt user
clearpart --none

part biosboot --fstype=biosboot --size=1
part swap --label=swap --recommended
part /boot --fstype=ext4 --label=/boot --size=512
part / --fstype=ext4 --grow --label=/ --fsoptions=grpquota,usrquota
