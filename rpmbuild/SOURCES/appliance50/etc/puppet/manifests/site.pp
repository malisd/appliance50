node localhost {
    include appliance50 
    include cronie 
    include dhcp 
    include mysql
    include rsnapshot
}
