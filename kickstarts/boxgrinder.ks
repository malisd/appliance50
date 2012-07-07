bootloader --append="biosdevname=0 quiet rhgb" --location=mbr
#clearpart --all --initlabel
part biosboot --fstype=biosboot --ondisk=sda --size=1
part swap --label=swap --ondisk=sda --size=1024
part /boot --fstype=ext4 --label=/boot --ondisk=sda --size=512
part / --fstype=ext4 --label=/ --ondisk=sda --size=32768

%packages

system-config-firewall

%end
