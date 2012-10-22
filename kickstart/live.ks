#%include appliance50.ks

bootloader --append="biosdevname=0 quiet rhgb" --location=mbr

part / --size 3072 --fstype ext4
repo --name=fedora --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=fedora-$releasever&arch=$basearch
repo --name=updates --mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f$releasever&arch=$basearch

%packages

kernel*
grub-efi
grub2
efibootmgr
mactel-boot

@anaconda-tools

%end
