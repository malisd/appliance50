%include appliance50.ks

bootloader --append="biosdevname=0 quiet rhgb" --location=mbr
clearpart --all --initlabel
part biosboot --fstype=biosboot --size=1
part swap --label=swap --recommended
part /boot --fstype=ext4 --label=/boot --size=500
part / --fstype=ext4 --grow --label=/ --fsoptions=grpquota,usrquota
