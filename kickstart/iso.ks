#%include appliance50.ks

bootloader --append="biosdevname=0 quiet rhgb" --location=mbr

%packages

kernel*
grub-efi
grub2
efibootmgr
mactel-boot

@anaconda-tools

%end
