############################################################################
Summary: Configures the CS50 Appliance.
Name: cs50-appliance
Version: 2.0
Release: 12
License: CC BY-NC-SA 3.0
Group: System Environment/Base
Source: %{name}-%{version}
Vendor: CS50
URL: https://manual.cs50.net/Appliance
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: generic-release = 15
Requires: garcon, gdm, httpd, iptables, mod_suphp, mysql-server, nano, openssh-server, php, phpMyAdmin, proftpd, rsnapshot, setup, sudo, teamviewer6, usermin, vim, webmin, xfce4-panel, xorg-x11-fonts-misc
BuildArch: i386


############################################################################
%description
The CS50 Appliance is a virtual machine that lets you
"take" CS50, even if you're not a student at Harvard.


############################################################################
%prep
/bin/rm -rf %{_builddir}/%{name}-%{version}/
/bin/cp -a %{_sourcedir}/%{name}-%{version} %{_builddir}/


############################################################################
%build


############################################################################
%check


############################################################################
%install
/bin/rm -rf %{buildroot}
/bin/cp -a %{_builddir}/%{name}-%{version} %{buildroot}/


############################################################################
%clean
/bin/rm -rf %{buildroot}


############################################################################
%pre

# /etc/group
/usr/sbin/groupadd -r courses > /dev/null 2>&1
/usr/sbin/groupadd students > /dev/null 2>&1

# /home/jharvard/
/usr/sbin/adduser --comment "John Harvard" --gid students --groups wheel jharvard > /dev/null 2>&1
/bin/echo crimson | /usr/bin/passwd --stdin jharvard > /dev/null

# /etc/gdm/custom.conf
/bin/cat > /etc/gdm/custom.conf <<"EOF"
[daemon]
AutomaticLoginEnable=True
AutomaticLogin=jharvard
EOF


############################################################################
%post

# /etc/banner
/bin/cp -a /etc/banner /etc/banner.rpmsave > /dev/null 2>&1
/bin/cat > /etc/banner <<"EOF"
This is CS50. In a box.
EOF

# /etc/gconf/gconf.xml.defaults/
/usr/bin/gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type bool --set /apps/gdm/simple-greeter/banner_message_enable true
/usr/bin/gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type bool --set /apps/gdm/simple-greeter/disable_user_list true
/usr/bin/gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/gdm/simple-greeter/banner_message_text "This is CS50. In a box."

# /etc/profile.d/cs50.sh
/bin/cp -a /etc/profile.d/cs50.sh /etc/profile.d/cs50.sh.rpmsave > /dev/null 2>&1
/bin/cat > /etc/profile.d/cs50.sh <<"EOF"
# are we in an interactive shell?
if [ "$PS1" ]; then

  # set umask
  umask 0077

  # configure prompt
  export PS1="\u@\h (\w): "

  # protect user
  alias cp="cp -i"
  alias mv="mv -i"
  alias rm="rm -i"

  # allow core dumps
  ulimit -c unlimited

  # disable auto-logout
  export TMOUT=0

  # set locale
  export LANG=C

  # set editor
  export EDITOR=nano

  # gcc
  export CC=gcc
  export CFLAGS="-ggdb -std=c99 -Wall -Werror -Wformat=0"
  export LDLIBS="-lcs50 -lm"

fi
EOF

# /etc/sysconfig/network
/bin/cp -a /etc/sysconfig/network /etc/sysconfig/network.rpmsave > /dev/null 2>&1
/bin/cat > /etc/sysconfig/network <<"EOF"
NETWORKING=yes
HOSTNAME=appliance
EOF

# /etc/sysconfig/network-scripts/ifcfg-eth0
/bin/cp -a /etc/sysconfig/network-scripts/ifcfg-eth0 /etc/sysconfig/network-scripts/ifcfg-eth0.rpmsave > /dev/null 2>&1
/bin/cat > /etc/sysconfig/network-scripts/ifcfg-eth0 <<"EOF"
BOOTPROTO=dhcp
DEVICE=eth0
NETWORKING_IPV6=no
ONBOOT=yes
TYPE=Ethernet
EOF

# /etc/sysconfig/network-scripts/ifcfg-eth1
/bin/cp -a /etc/sysconfig/network-scripts/ifcfg-eth1 /etc/sysconfig/network-scripts/ifcfg-eth1.rpmsave > /dev/null 2>&1
/bin/cat > /etc/sysconfig/network-scripts/ifcfg-eth1 <<"EOF"
BOOTPROTO=static
DEVICE=eth1
IPADDR=192.168.56.50
NETMASK=255.255.255.0
NETWORKING_IPV6=no
ONBOOT=yes
TYPE=Ethernet
EOF

# /etc/sysconfig/network-scripts/ifcfg-eth2
/bin/cp -a /etc/sysconfig/network-scripts/ifcfg-eth2 /etc/sysconfig/network-scripts/ifcfg-eth2.rpmsave > /dev/null 2>&1
/bin/cat > /etc/sysconfig/network-scripts/ifcfg-eth2 <<"EOF"
BOOTPROTO=dhcp
DEVICE=eth2
NETWORKING_IPV6=no
ONBOOT=no
TYPE=Ethernet
EOF


############################################################################
%preun


############################################################################
%postun


##########################################################################
%triggerin -- garcon

# /etc/xdg/menus/xfce-applications.menu
/bin/cp -a /etc/xdg/menus/xfce-applications.menu /etc/xdg/menus/xfce-applications.menu.rpmsave > /dev/null 2>&1
/bin/cat > /etc/xdg/menus/xfce-applications.menu <<"EOF"

<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN"
  "http://www.freedesktop.org/standards/menu-spec/1.0/menu.dtd">

<Menu>
    <Name>Xfce</Name>

    <DefaultAppDirs/>
    <DefaultDirectoryDirs/>
    <DefaultMergeDirs/>

    <Include>
        <Category>X-Xfce-Toplevel</Category>
    </Include>

    <Layout>
        <Filename>xfrun4.desktop</Filename>
        <Separator/>
        <Menuname>CS50</Menuname>
        <Separator/>
        <Filename>teamviewer.desktop</Filename>
        <Separator/>
        <Menuname>Administration</Menuname>        
        <Menuname>Preferences</Menuname>
        <Separator/>
        <Merge type="all"/>
        <Separator/>
        <Filename>xfce4-session-logout.desktop</Filename>
    </Layout>

    <Exclude>
        <Or>
            <Filename>exo-terminal-emulator.desktop</Filename>
            <Filename>exo-file-manager.desktop</Filename>
            <Filename>exo-mail-reader.desktop</Filename>
            <Filename>exo-web-browser.desktop</Filename>
        </Or>
    </Exclude>
    
    <Menu>
        <Name>CS50</Name>
        <Directory>CS50.directory</Directory>
        <Include>
            <Category>CS50</Category>
        </Include>
        <Layout>
            <Filename>cs50-appliance.desktop</Filename>
            <Separator/>
            <Merge type="all"/>
        </Layout>
    </Menu>

    <Menu>
        <Name>Preferences</Name>
        <Directory>xfce-settings.directory</Directory>
        <Include>
            <And>
                <Category>Settings</Category>
                <Not><Category>System</Category></Not>
                <Not><Category>Screensaver</Category></Not>
                <Not><Filename>fedora-im-chooser.desktop</Filename></Not>
                <Not><Filename>gnome-default-applications.desktop</Filename></Not>
            </And>
        </Include>
        <Layout>
            <Filename>xfce-settings-manager.desktop</Filename>
            <Separator/>
            <Merge type="all"/>
        </Layout>
    </Menu>

    <Menu>
        <Name>Administration</Name>
        <Directory>SystemConfig.directory</Directory>
        <Include>
            <And>
                <Category>Settings</Category>
                <Category>System</Category>
                <Not><Category>Screensaver</Category></Not>
            </And>
            <Filename>gpk-application.desktop</Filename>
            <Filename>gpk-update-viewer.desktop</Filename>
        </Include>
        <Exclude>
            <Filename>authconfig.desktop</Filename>
            <Filename>redhat-system-control-network.desktop</Filename>
            <Filename>system-config-users.desktop</Filename>
        </Exclude>
    </Menu>

    <Menu>
        <Name>Accessories</Name>
        <Directory>Utility.directory</Directory>
        <Include>
            <And>
                <Category>Utility</Category>
                <Not><Category>System</Category></Not>
            </And>
        </Include>
        <Exclude>
            <Or>
                <Filename>emacsclient.desktop</Filename>
                <Filename>exo-file-manager.desktop</Filename>
                <Filename>exo-terminal-emulator.desktop</Filename>
                <Filename>xfce4-about.desktop</Filename>
                <Filename>xfhelp4.desktop</Filename>
                <Filename>xfrun4.desktop</Filename>
            </Or>
        </Exclude>
    </Menu>

    <Menu>
        <Name>Development</Name>
        <Directory>Development.directory</Directory>
        <Include>
            <Or>
                <Category>Development</Category>
                <Filename>gedit.desktop</Filename>
            </Or>
        </Include>
    </Menu>

    <Menu>
        <Name>Documentation</Name>
        <Directory>Documentation.directory</Directory>
        <Include>
            <Category>Documentation</Category>
        </Include>
    </Menu>
        
    <Menu>
        <Name>Education</Name>
        <Directory>Education.directory</Directory>
        <Include>
            <Or>
            <Category>Education</Category>
            <Category>Science</Category>
        </Or>
        </Include>
    </Menu>

    <Menu>
        <Name>Games</Name>
        <Directory>Game.directory</Directory>
        <Include>
            <Category>Game</Category>
        </Include>
    </Menu>

    <Menu>
        <Name>Graphics</Name>
        <Directory>Graphics.directory</Directory>
        <Include>
            <Category>Graphics</Category>
        </Include>
    </Menu>

    <Menu>
        <Name>Multimedia</Name>
        <Directory>AudioVideo.directory</Directory>
        <Include>
            <Category>Audio</Category>
            <Category>Video</Category>
            <Category>AudioVideo</Category>
        </Include>
    </Menu>

    <Menu>
        <Name>Network</Name>
        <Directory>Network.directory</Directory>
        <Include>
            <Or>
                <Category>Network</Category>
                <Filename>Terminal.desktop</Filename>
            </Or>
        </Include>
        <Exclude>
            <Or>
                <Filename>exo-mail-reader.desktop</Filename>
                <Filename>exo-web-browser.desktop</Filename>
                <Filename>redhat-system-control-network.desktop</Filename>
            </Or>
        </Exclude>
    </Menu>

    <Menu>
        <Name>Office</Name>
        <Directory>Office.directory</Directory>
        <Include>
            <Category>Office</Category>
        </Include>
    </Menu>

    <Menu>
        <Name>System</Name>
        <Directory>System.directory</Directory>
        <Include>
            <And>
                <Or>
                    <Category>Emulator</Category>
                    <Category>System</Category>
                </Or>
                <Not><Category>Settings</Category></Not>
                <Not><Category>Screensaver</Category></Not>
                <Not><Filename>gpk-application.desktop</Filename></Not>
                <Not><Filename>gpk-update-viewer.desktop</Filename></Not>
            </And>
        </Include>
        <Exclude>
            <Or>
                <Filename>fedora-Thunar-bulk-rename.desktop</Filename>
                <Filename>redhat-usermount.desktop</Filename>
                <Filename>xfce4-session-logout.desktop</Filename>
            </Or>
        </Exclude>
    </Menu>

    <Menu>
        <Name>Other</Name>
        <Directory>xfce-other.directory</Directory>
        <OnlyUnallocated/>
        <Include>
            <And>
                <Not><Category>Core</Category></Not>
                <Not><Category>Settings</Category></Not>
                <Not><Category>SystemSetup</Category></Not>
                <Not><Category>X-Red-Hat-ServerConfig</Category></Not>
                <Not><Category>Screensaver</Category></Not>
            </And>
        </Include>
        <Exclude>
            <Or>
                <Filename>emacsclient.desktop</Filename>
                <Filename>exo-terminal-emulator.desktop</Filename>
                <Filename>exo-file-manager.desktop</Filename>
                <Filename>exo-mail-reader.desktop</Filename>
                <Filename>exo-web-browser.desktop</Filename>
                <Filename>redhat-usermount.desktop</Filename>
            </Or>
        </Exclude>
    </Menu>

</Menu>
EOF

# /usr/share/desktop-directories/CS50.directory
/bin/cat > /usr/share/desktop-directories/CS50.directory <<"EOF"
[Desktop Entry]
Name=CS50 Manual
Icon=help-browser
Type=Directory
Encoding=UTF-8
EOF

# /usr/share/applications/cs50-appliance.desktop
/bin/cat > /usr/share/applications/cs50-appliance.desktop <<"EOF"
[Desktop Entry]
Version=1.0
Type=Application
Exec=firefox https://manual.cs50.net/Appliance
Icon=help-contents
StartupNotify=false
Terminal=false
Categories=CS50;
Name=CS50 Appliance
EOF

# /usr/share/applications/cs50-2010-fall.desktop
/bin/cat > /usr/share/applications/cs50-2010-fall.desktop <<"EOF"
[Desktop Entry]
Version=1.0
Type=Application
Exec=firefox https://manual.cs50.net/Fall_2010
Icon=help-contents
StartupNotify=false
Terminal=false
Categories=CS50;
Name=Fall 2010
EOF

# /usr/share/applications/cs50-2011-fall.desktop
/bin/cat > /usr/share/applications/cs50-2011-fall.desktop <<"EOF"
[Desktop Entry]
Version=1.0
Type=Application
Exec=firefox https://manual.cs50.net/Fall_2011
Icon=help-contents
StartupNotify=false
Terminal=false
Categories=CS50;
Name=Fall 2011
EOF

# /usr/share/applications/teamviewer.desktop
/bin/cat > /usr/share/applications/teamviewer.desktop <<"EOF"
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Name=TeamViewer
Comment=TeamViewer Remote Control Application
Exec=/opt/teamviewer/teamviewer/6/bin/teamviewer
Icon=/opt/teamviewer/teamviewer/6/desktop/teamviewer.png
Type=Application
Categories=X-Xfce-Toplevel;
EOF


##########################################################################
%triggerin -- gdm

# /etc/pam.d/gdm
/bin/cp -a /etc/pam.d/gdm /etc/pam.d/gdm.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^\(auth[ \t]*required[ \t]*pam_succeed_if.so user != root quiet\)/#\1/' /etc/pam.d/gdm

# /etc/pam.d/gdm-password
/bin/cp -a /etc/pam.d/gdm-password /etc/pam.d/gdm-password.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^\(auth[ \t]*required[ \t]*pam_succeed_if.so user != root quiet\)/#\1/' /etc/pam.d/gdm-password


##########################################################################
%triggerin -- httpd

# /etc/httpd/conf/httpd.conf
/bin/cp -a /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.rpmsave > /dev/null 2>&1
/bin/cat > /etc/httpd/conf/httpd.conf <<"EOF"
#
# This is the main Apache server configuration file.  It contains the
# configuration directives that give the server its instructions.
# See <URL:http://httpd.apache.org/docs/2.2/> for detailed information.
# In particular, see
# <URL:http://httpd.apache.org/docs/2.2/mod/directives.html>
# for a discussion of each configuration directive.
#
#
# Do NOT simply read the instructions in here without understanding
# what they do.  They're here only as hints or reminders.  If you are unsure
# consult the online docs. You have been warned.  
#
# The configuration directives are grouped into three basic sections:
#  1. Directives that control the operation of the Apache server process as a
#     whole (the 'global environment').
#  2. Directives that define the parameters of the 'main' or 'default' server,
#     which responds to requests that aren't handled by a virtual host.
#     These directives also provide default values for the settings
#     of all virtual hosts.
#  3. Settings for virtual hosts, which allow Web requests to be sent to
#     different IP addresses or hostnames and have them handled by the
#     same Apache server process.
#
# Configuration and logfile names: If the filenames you specify for many
# of the server's control files begin with "/" (or "drive:/" for Win32), the
# server will use that explicit path.  If the filenames do *not* begin
# with "/", the value of ServerRoot is prepended -- so "logs/foo.log"
# with ServerRoot set to "/etc/httpd" will be interpreted by the
# server as "/etc/httpd/logs/foo.log".
#

### Section 1: Global Environment
#
# The directives in this section affect the overall operation of Apache,
# such as the number of concurrent requests it can handle or where it
# can find its configuration files.
#

#
# Don't give away too much information about all the subcomponents
# we are running.  Comment out this line if you don't mind remote sites
# finding out what major optional modules you are running
ServerTokens OS

#
# ServerRoot: The top of the directory tree under which the server's
# configuration, error, and log files are kept.
#
# NOTE!  If you intend to place this on an NFS (or otherwise network)
# mounted filesystem then please read the LockFile documentation
# (available at <URL:http://httpd.apache.org/docs/2.2/mod/mpm_common.html#lockfile>);
# you will save yourself a lot of trouble.
#
# Do NOT add a slash at the end of the directory path.
#
ServerRoot "/etc/httpd"

#
# PidFile: The file in which the server should record its process
# identification number when it starts.  Note the PIDFILE variable in
# /etc/sysconfig/httpd must be set appropriately if this location is
# changed.
#
PidFile run/httpd.pid

#
# Timeout: The number of seconds before receives and sends time out.
#
Timeout 60

#
# KeepAlive: Whether or not to allow persistent connections (more than
# one request per connection). Set to "Off" to deactivate.
#
KeepAlive Off

#
# MaxKeepAliveRequests: The maximum number of requests to allow
# during a persistent connection. Set to 0 to allow an unlimited amount.
# We recommend you leave this number high, for maximum performance.
#
MaxKeepAliveRequests 100

#
# KeepAliveTimeout: Number of seconds to wait for the next request from the
# same client on the same connection.
#
KeepAliveTimeout 5

##
## Server-Pool Size Regulation (MPM specific)
## 

# prefork MPM
# StartServers: number of server processes to start
# MinSpareServers: minimum number of server processes which are kept spare
# MaxSpareServers: maximum number of server processes which are kept spare
# ServerLimit: maximum value for MaxClients for the lifetime of the server
# MaxClients: maximum number of server processes allowed to start
# MaxRequestsPerChild: maximum number of requests a server process serves
<IfModule prefork.c>
StartServers       8
MinSpareServers    5
MaxSpareServers   20
ServerLimit      256
MaxClients       256
MaxRequestsPerChild  4000
</IfModule>

# worker MPM
# StartServers: initial number of server processes to start
# MaxClients: maximum number of simultaneous client connections
# MinSpareThreads: minimum number of worker threads which are kept spare
# MaxSpareThreads: maximum number of worker threads which are kept spare
# ThreadsPerChild: constant number of worker threads in each server process
# MaxRequestsPerChild: maximum number of requests a server process serves
<IfModule worker.c>
StartServers         4
MaxClients         300
MinSpareThreads     25
MaxSpareThreads     75 
ThreadsPerChild     25
MaxRequestsPerChild  0
</IfModule>

#
# Listen: Allows you to bind Apache to specific IP addresses and/or
# ports, in addition to the default. See also the <VirtualHost>
# directive.
#
# Change this to Listen on specific IP addresses as shown below to 
# prevent Apache from glomming onto all bound IP addresses (0.0.0.0)
#
#Listen 12.34.56.78:80
Listen 80

#
# Dynamic Shared Object (DSO) Support
#
# To be able to use the functionality of a module which was built as a DSO you
# have to place corresponding `LoadModule' lines at this location so the
# directives contained in it are actually available _before_ they are used.
# Statically compiled modules (those listed by `httpd -l') do not need
# to be loaded here.
#
# Example:
# LoadModule foo_module modules/mod_foo.so
#
LoadModule auth_basic_module modules/mod_auth_basic.so
LoadModule auth_digest_module modules/mod_auth_digest.so
LoadModule authn_file_module modules/mod_authn_file.so
LoadModule authn_alias_module modules/mod_authn_alias.so
LoadModule authn_anon_module modules/mod_authn_anon.so
LoadModule authn_dbm_module modules/mod_authn_dbm.so
LoadModule authn_default_module modules/mod_authn_default.so
LoadModule authz_host_module modules/mod_authz_host.so
LoadModule authz_user_module modules/mod_authz_user.so
LoadModule authz_owner_module modules/mod_authz_owner.so
LoadModule authz_groupfile_module modules/mod_authz_groupfile.so
LoadModule authz_dbm_module modules/mod_authz_dbm.so
LoadModule authz_default_module modules/mod_authz_default.so
LoadModule ldap_module modules/mod_ldap.so
LoadModule authnz_ldap_module modules/mod_authnz_ldap.so
LoadModule include_module modules/mod_include.so
LoadModule log_config_module modules/mod_log_config.so
LoadModule logio_module modules/mod_logio.so
LoadModule env_module modules/mod_env.so
LoadModule ext_filter_module modules/mod_ext_filter.so
LoadModule mime_magic_module modules/mod_mime_magic.so
LoadModule expires_module modules/mod_expires.so
LoadModule deflate_module modules/mod_deflate.so
LoadModule headers_module modules/mod_headers.so
LoadModule usertrack_module modules/mod_usertrack.so
LoadModule setenvif_module modules/mod_setenvif.so
LoadModule mime_module modules/mod_mime.so
LoadModule dav_module modules/mod_dav.so
LoadModule status_module modules/mod_status.so
LoadModule autoindex_module modules/mod_autoindex.so
LoadModule info_module modules/mod_info.so
LoadModule dav_fs_module modules/mod_dav_fs.so
LoadModule vhost_alias_module modules/mod_vhost_alias.so
LoadModule negotiation_module modules/mod_negotiation.so
LoadModule dir_module modules/mod_dir.so
LoadModule actions_module modules/mod_actions.so
LoadModule speling_module modules/mod_speling.so
LoadModule userdir_module modules/mod_userdir.so
LoadModule alias_module modules/mod_alias.so
LoadModule substitute_module modules/mod_substitute.so
LoadModule rewrite_module modules/mod_rewrite.so
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_balancer_module modules/mod_proxy_balancer.so
LoadModule proxy_ftp_module modules/mod_proxy_ftp.so
LoadModule proxy_http_module modules/mod_proxy_http.so
LoadModule proxy_ajp_module modules/mod_proxy_ajp.so
LoadModule proxy_connect_module modules/mod_proxy_connect.so
LoadModule cache_module modules/mod_cache.so
LoadModule suexec_module modules/mod_suexec.so
LoadModule disk_cache_module modules/mod_disk_cache.so
LoadModule cgi_module modules/mod_cgi.so
LoadModule version_module modules/mod_version.so

#
# The following modules are not loaded by default:
#
#LoadModule asis_module modules/mod_asis.so
#LoadModule authn_dbd_module modules/mod_authn_dbd.so
#LoadModule cern_meta_module modules/mod_cern_meta.so
#LoadModule cgid_module modules/mod_cgid.so
#LoadModule dbd_module modules/mod_dbd.so
#LoadModule dumpio_module modules/mod_dumpio.so
#LoadModule filter_module modules/mod_filter.so
#LoadModule ident_module modules/mod_ident.so
#LoadModule log_forensic_module modules/mod_log_forensic.so
#LoadModule unique_id_module modules/mod_unique_id.so
#

#
# Load config files from the config directory "/etc/httpd/conf.d".
#
Include conf.d/*.conf

#
# ExtendedStatus controls whether Apache will generate "full" status
# information (ExtendedStatus On) or just basic information (ExtendedStatus
# Off) when the "server-status" handler is called. The default is Off.
#
#ExtendedStatus On

#
# If you wish httpd to run as a different user or group, you must run
# httpd as root initially and it will switch.  
#
# User/Group: The name (or #number) of the user/group to run httpd as.
#  . On SCO (ODT 3) use "User nouser" and "Group nogroup".
#  . On HPUX you may not be able to use shared memory as nobody, and the
#    suggested workaround is to create a user www and use that user.
#  NOTE that some kernels refuse to setgid(Group) or semctl(IPC_SET)
#  when the value of (unsigned)Group is above 60000; 
#  don't use Group #-1 on these systems!
#
User apache
Group apache

### Section 2: 'Main' server configuration
#
# The directives in this section set up the values used by the 'main'
# server, which responds to any requests that aren't handled by a
# <VirtualHost> definition.  These values also provide defaults for
# any <VirtualHost> containers you may define later in the file.
#
# All of these directives may appear inside <VirtualHost> containers,
# in which case these default settings will be overridden for the
# virtual host being defined.
#

#
# ServerAdmin: Your address, where problems with the server should be
# e-mailed.  This address appears on some server-generated pages, such
# as error documents.  e.g. admin@your-domain.com
#
ServerAdmin root@localhost

#
# ServerName gives the name and port that the server uses to identify itself.
# This can often be determined automatically, but we recommend you specify
# it explicitly to prevent problems during startup.
#
# If this is not set to valid DNS name for your host, server-generated
# redirections will not work.  See also the UseCanonicalName directive.
#
# If your host doesn't have a registered DNS name, enter its IP address here.
# You will have to access it by its address anyway, and this will make 
# redirections work in a sensible way.
#
#ServerName www.example.com:80

#
# UseCanonicalName: Determines how Apache constructs self-referencing 
# URLs and the SERVER_NAME and SERVER_PORT variables.
# When set "Off", Apache will use the Hostname and Port supplied
# by the client.  When set "On", Apache will use the value of the
# ServerName directive.
#
UseCanonicalName Off

#
# DocumentRoot: The directory out of which you will serve your
# documents. By default, all requests are taken from this directory, but
# symbolic links and aliases may be used to point to other locations.
#
DocumentRoot "/var/www/html"

#
# Each directory to which Apache has access can be configured with respect
# to which services and features are allowed and/or disabled in that
# directory (and its subdirectories). 
#
# First, we configure the "default" to be a very restrictive set of 
# features.  
#
<Directory />
    Options FollowSymLinks
    AllowOverride None
</Directory>

#
# Note that from this point forward you must specifically allow
# particular features to be enabled - so if something's not working as
# you might expect, make sure that you have specifically enabled it
# below.
#

#
# This should be changed to whatever you set DocumentRoot to.
#
<Directory "/var/www/html">

#
# Possible values for the Options directive are "None", "All",
# or any combination of:
#   Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
#
# Note that "MultiViews" must be named *explicitly* --- "Options All"
# doesn't give it to you.
#
# The Options directive is both complicated and important.  Please see
# http://httpd.apache.org/docs/2.2/mod/core.html#options
# for more information.
#
    Options Indexes FollowSymLinks

#
# AllowOverride controls what directives may be placed in .htaccess files.
# It can be "All", "None", or any combination of the keywords:
#   Options FileInfo AuthConfig Limit
#
    AllowOverride None

#
# Controls who can get stuff from this server.
#
    Order allow,deny
    Allow from all

</Directory>

#
# UserDir: The name of the directory that is appended onto a user's home
# directory if a ~user request is received.
#
# The path to the end user account 'public_html' directory must be
# accessible to the webserver userid.  This usually means that ~userid
# must have permissions of 711, ~userid/public_html must have permissions
# of 755, and documents contained therein must be world-readable.
# Otherwise, the client will only receive a "403 Forbidden" message.
#
# See also: http://httpd.apache.org/docs/misc/FAQ.html#forbidden
#
<IfModule mod_userdir.c>
    #
    # UserDir is disabled by default since it can confirm the presence
    # of a username on the system (depending on home directory
    # permissions).
    #
    #UserDir disabled

    #
    # To enable requests to /~user/ to serve the user's public_html
    # directory, remove the "UserDir disabled" line above, and uncomment
    # the following line instead:
    # 
    UserDir public_html

</IfModule>

#
# Control access to UserDir directories.  The following is an example
# for a site where these directories are restricted to read-only.
#
#<Directory /home/*/public_html>
#    AllowOverride FileInfo AuthConfig Limit
#    Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
#    <Limit GET POST OPTIONS>
#        Order allow,deny
#        Allow from all
#    </Limit>
#    <LimitExcept GET POST OPTIONS>
#        Order deny,allow
#        Deny from all
#    </LimitExcept>
#</Directory>

#
# DirectoryIndex: sets the file that Apache will serve if a directory
# is requested.
#
# The index.html.var file (a type-map) is used to deliver content-
# negotiated documents.  The MultiViews Option can be used for the 
# same purpose, but it is much slower.
#
DirectoryIndex index.html index.html.var

#
# AccessFileName: The name of the file to look for in each directory
# for additional configuration directives.  See also the AllowOverride
# directive.
#
AccessFileName .htaccess

#
# The following lines prevent .htaccess and .htpasswd files from being 
# viewed by Web clients. 
#
<Files ~ "^\.ht">
    Order allow,deny
    Deny from all
    Satisfy All
</Files>

#
# TypesConfig describes where the mime.types file (or equivalent) is
# to be found.
#
TypesConfig /etc/mime.types

#
# DefaultType is the default MIME type the server will use for a document
# if it cannot otherwise determine one, such as from filename extensions.
# If your server contains mostly text or HTML documents, "text/plain" is
# a good value.  If most of your content is binary, such as applications
# or images, you may want to use "application/octet-stream" instead to
# keep browsers from trying to display binary files as though they are
# text.
#
DefaultType text/plain

#
# The mod_mime_magic module allows the server to use various hints from the
# contents of the file itself to determine its type.  The MIMEMagicFile
# directive tells the module where the hint definitions are located.
#
<IfModule mod_mime_magic.c>
#   MIMEMagicFile /usr/share/magic.mime
    MIMEMagicFile conf/magic
</IfModule>

#
# HostnameLookups: Log the names of clients or just their IP addresses
# e.g., www.apache.org (on) or 204.62.129.132 (off).
# The default is off because it'd be overall better for the net if people
# had to knowingly turn this feature on, since enabling it means that
# each client request will result in AT LEAST one lookup request to the
# nameserver.
#
HostnameLookups Off

#
# EnableMMAP: Control whether memory-mapping is used to deliver
# files (assuming that the underlying OS supports it).
# The default is on; turn this off if you serve from NFS-mounted 
# filesystems.  On some systems, turning it off (regardless of
# filesystem) can improve performance; for details, please see
# http://httpd.apache.org/docs/2.2/mod/core.html#enablemmap
#
#EnableMMAP off

#
# EnableSendfile: Control whether the sendfile kernel support is 
# used to deliver files (assuming that the OS supports it). 
# The default is on; turn this off if you serve from NFS-mounted 
# filesystems.  Please see
# http://httpd.apache.org/docs/2.2/mod/core.html#enablesendfile
#
#EnableSendfile off

#
# ErrorLog: The location of the error log file.
# If you do not specify an ErrorLog directive within a <VirtualHost>
# container, error messages relating to that virtual host will be
# logged here.  If you *do* define an error logfile for a <VirtualHost>
# container, that host's errors will be logged there and not here.
#
ErrorLog logs/error_log

#
# LogLevel: Control the number of messages logged to the error_log.
# Possible values include: debug, info, notice, warn, error, crit,
# alert, emerg.
#
LogLevel warn

#
# The following directives define some format nicknames for use with
# a CustomLog directive (see below).
#
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
LogFormat "%h %l %u %t \"%r\" %>s %b" common
LogFormat "%{Referer}i -> %U" referer
LogFormat "%{User-agent}i" agent

# "combinedio" includes actual counts of actual bytes received (%I) and sent (%O); this
# requires the mod_logio module to be loaded.
#LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio

#
# The location and format of the access logfile (Common Logfile Format).
# If you do not define any access logfiles within a <VirtualHost>
# container, they will be logged here.  Contrariwise, if you *do*
# define per-<VirtualHost> access logfiles, transactions will be
# logged therein and *not* in this file.
#
#CustomLog logs/access_log common

#
# If you would like to have separate agent and referer logfiles, uncomment
# the following directives.
#
#CustomLog logs/referer_log referer
#CustomLog logs/agent_log agent

#
# For a single logfile with access, agent, and referer information
# (Combined Logfile Format), use the following directive:
#
CustomLog logs/access_log combined

#
# Optionally add a line containing the server version and virtual host
# name to server-generated pages (internal error documents, FTP directory
# listings, mod_status and mod_info output etc., but not CGI generated
# documents or custom error documents).
# Set to "EMail" to also include a mailto: link to the ServerAdmin.
# Set to one of:  On | Off | EMail
#
ServerSignature On

#
# Aliases: Add here as many aliases as you need (with no limit). The format is 
# Alias fakename realname
#
# Note that if you include a trailing / on fakename then the server will
# require it to be present in the URL.  So "/icons" isn't aliased in this
# example, only "/icons/".  If the fakename is slash-terminated, then the 
# realname must also be slash terminated, and if the fakename omits the 
# trailing slash, the realname must also omit it.
#
# We include the /icons/ alias for FancyIndexed directory listings.  If you
# do not use FancyIndexing, you may comment this out.
#
Alias /icons/ "/var/www/icons/"

<Directory "/var/www/icons">
    Options Indexes MultiViews FollowSymLinks
    AllowOverride None
    Order allow,deny
    Allow from all
</Directory>

#
# WebDAV module configuration section.
# 
<IfModule mod_dav_fs.c>
    # Location of the WebDAV lock database.
    DAVLockDB /var/lib/dav/lockdb
</IfModule>

#
# ScriptAlias: This controls which directories contain server scripts.
# ScriptAliases are essentially the same as Aliases, except that
# documents in the realname directory are treated as applications and
# run by the server when requested rather than as documents sent to the client.
# The same rules about trailing "/" apply to ScriptAlias directives as to
# Alias.
#
ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"

#
# "/var/www/cgi-bin" should be changed to whatever your ScriptAliased
# CGI directory exists, if you have that configured.
#
<Directory "/var/www/cgi-bin">
    AllowOverride None
    Options None
    Order allow,deny
    Allow from all
</Directory>

#
# Redirect allows you to tell clients about documents which used to exist in
# your server's namespace, but do not anymore. This allows you to tell the
# clients where to look for the relocated document.
# Example:
# Redirect permanent /foo http://www.example.com/bar

#
# Directives controlling the display of server-generated directory listings.
#

#
# IndexOptions: Controls the appearance of server-generated directory
# listings.
#
IndexOptions FancyIndexing VersionSort NameWidth=* HTMLTable Charset=UTF-8

#
# AddIcon* directives tell the server which icon to show for different
# files or filename extensions.  These are only displayed for
# FancyIndexed directories.
#
AddIconByEncoding (CMP,/icons/compressed.gif) x-compress x-gzip

AddIconByType (TXT,/icons/text.gif) text/*
AddIconByType (IMG,/icons/image2.gif) image/*
AddIconByType (SND,/icons/sound2.gif) audio/*
AddIconByType (VID,/icons/movie.gif) video/*

AddIcon /icons/binary.gif .bin .exe
AddIcon /icons/binhex.gif .hqx
AddIcon /icons/tar.gif .tar
AddIcon /icons/world2.gif .wrl .wrl.gz .vrml .vrm .iv
AddIcon /icons/compressed.gif .Z .z .tgz .gz .zip
AddIcon /icons/a.gif .ps .ai .eps
AddIcon /icons/layout.gif .html .shtml .htm .pdf
AddIcon /icons/text.gif .txt
AddIcon /icons/c.gif .c
AddIcon /icons/p.gif .pl .py
AddIcon /icons/f.gif .for
AddIcon /icons/dvi.gif .dvi
AddIcon /icons/uuencoded.gif .uu
AddIcon /icons/script.gif .conf .sh .shar .csh .ksh .tcl
AddIcon /icons/tex.gif .tex
AddIcon /icons/bomb.gif core

AddIcon /icons/back.gif ..
AddIcon /icons/hand.right.gif README
AddIcon /icons/folder.gif ^^DIRECTORY^^
AddIcon /icons/blank.gif ^^BLANKICON^^

#
# DefaultIcon is which icon to show for files which do not have an icon
# explicitly set.
#
DefaultIcon /icons/unknown.gif

#
# AddDescription allows you to place a short description after a file in
# server-generated indexes.  These are only displayed for FancyIndexed
# directories.
# Format: AddDescription "description" filename
#
#AddDescription "GZIP compressed document" .gz
#AddDescription "tar archive" .tar
#AddDescription "GZIP compressed tar archive" .tgz

#
# ReadmeName is the name of the README file the server will look for by
# default, and append to directory listings.
#
# HeaderName is the name of a file which should be prepended to
# directory indexes. 
ReadmeName README.html
HeaderName HEADER.html

#
# IndexIgnore is a set of filenames which directory indexing should ignore
# and not include in the listing.  Shell-style wildcarding is permitted.
#
IndexIgnore .??* *~ *# HEADER* README* RCS CVS *,v *,t

#
# DefaultLanguage and AddLanguage allows you to specify the language of 
# a document. You can then use content negotiation to give a browser a 
# file in a language the user can understand.
#
# Specify a default language. This means that all data
# going out without a specific language tag (see below) will 
# be marked with this one. You probably do NOT want to set
# this unless you are sure it is correct for all cases.
#
# * It is generally better to not mark a page as 
# * being a certain language than marking it with the wrong
# * language!
#
# DefaultLanguage nl
#
# Note 1: The suffix does not have to be the same as the language
# keyword --- those with documents in Polish (whose net-standard
# language code is pl) may wish to use "AddLanguage pl .po" to
# avoid the ambiguity with the common suffix for perl scripts.
#
# Note 2: The example entries below illustrate that in some cases 
# the two character 'Language' abbreviation is not identical to 
# the two character 'Country' code for its country,
# E.g. 'Danmark/dk' versus 'Danish/da'.
#
# Note 3: In the case of 'ltz' we violate the RFC by using a three char
# specifier. There is 'work in progress' to fix this and get
# the reference data for rfc1766 cleaned up.
#
# Catalan (ca) - Croatian (hr) - Czech (cs) - Danish (da) - Dutch (nl)
# English (en) - Esperanto (eo) - Estonian (et) - French (fr) - German (de)
# Greek-Modern (el) - Hebrew (he) - Italian (it) - Japanese (ja)
# Korean (ko) - Luxembourgeois* (ltz) - Norwegian Nynorsk (nn)
# Norwegian (no) - Polish (pl) - Portugese (pt)
# Brazilian Portuguese (pt-BR) - Russian (ru) - Swedish (sv)
# Simplified Chinese (zh-CN) - Spanish (es) - Traditional Chinese (zh-TW)
#
AddLanguage ca .ca
AddLanguage cs .cz .cs
AddLanguage da .dk
AddLanguage de .de
AddLanguage el .el
AddLanguage en .en
AddLanguage eo .eo
AddLanguage es .es
AddLanguage et .et
AddLanguage fr .fr
AddLanguage he .he
AddLanguage hr .hr
AddLanguage it .it
AddLanguage ja .ja
AddLanguage ko .ko
AddLanguage ltz .ltz
AddLanguage nl .nl
AddLanguage nn .nn
AddLanguage no .no
AddLanguage pl .po
AddLanguage pt .pt
AddLanguage pt-BR .pt-br
AddLanguage ru .ru
AddLanguage sv .sv
AddLanguage zh-CN .zh-cn
AddLanguage zh-TW .zh-tw

#
# LanguagePriority allows you to give precedence to some languages
# in case of a tie during content negotiation.
#
# Just list the languages in decreasing order of preference. We have
# more or less alphabetized them here. You probably want to change this.
#
LanguagePriority en ca cs da de el eo es et fr he hr it ja ko ltz nl nn no pl pt pt-BR ru sv zh-CN zh-TW

#
# ForceLanguagePriority allows you to serve a result page rather than
# MULTIPLE CHOICES (Prefer) [in case of a tie] or NOT ACCEPTABLE (Fallback)
# [in case no accepted languages matched the available variants]
#
ForceLanguagePriority Prefer Fallback

#
# Specify a default charset for all content served; this enables
# interpretation of all content as UTF-8 by default.  To use the 
# default browser choice (ISO-8859-1), or to allow the META tags
# in HTML content to override this choice, comment out this
# directive:
#
AddDefaultCharset UTF-8

#
# AddType allows you to add to or override the MIME configuration
# file mime.types for specific file types.
#
#AddType application/x-tar .tgz

#
# AddEncoding allows you to have certain browsers uncompress
# information on the fly. Note: Not all browsers support this.
# Despite the name similarity, the following Add* directives have nothing
# to do with the FancyIndexing customization directives above.
#
#AddEncoding x-compress .Z
#AddEncoding x-gzip .gz .tgz

# If the AddEncoding directives above are commented-out, then you
# probably should define those extensions to indicate media types:
#
AddType application/x-compress .Z
AddType application/x-gzip .gz .tgz

#
#   MIME-types for downloading Certificates and CRLs
#
AddType application/x-x509-ca-cert .crt
AddType application/x-pkcs7-crl    .crl

#
# AddHandler allows you to map certain file extensions to "handlers":
# actions unrelated to filetype. These can be either built into the server
# or added with the Action directive (see below)
#
# To use CGI scripts outside of ScriptAliased directories:
# (You will also need to add "ExecCGI" to the "Options" directive.)
#
#AddHandler cgi-script .cgi

#
# For files that include their own HTTP headers:
#
#AddHandler send-as-is asis

#
# For type maps (negotiated resources):
# (This is enabled by default to allow the Apache "It Worked" page
#  to be distributed in multiple languages.)
#
AddHandler type-map var

#
# Filters allow you to process content before it is sent to the client.
#
# To parse .shtml files for server-side includes (SSI):
# (You will also need to add "Includes" to the "Options" directive.)
#
AddType text/html .shtml
AddOutputFilter INCLUDES .shtml

#
# Action lets you define media types that will execute a script whenever
# a matching file is called. This eliminates the need for repeated URL
# pathnames for oft-used CGI file processors.
# Format: Action media/type /cgi-script/location
# Format: Action handler-name /cgi-script/location
#

#
# Customizable error responses come in three flavors:
# 1) plain text 2) local redirects 3) external redirects
#
# Some examples:
#ErrorDocument 500 "The server made a boo boo."
#ErrorDocument 404 /missing.html
#ErrorDocument 404 "/cgi-bin/missing_handler.pl"
#ErrorDocument 402 http://www.example.com/subscription_info.html
#

#
# Putting this all together, we can internationalize error responses.
#
# We use Alias to redirect any /error/HTTP_<error>.html.var response to
# our collection of by-error message multi-language collections.  We use 
# includes to substitute the appropriate text.
#
# You can modify the messages' appearance without changing any of the
# default HTTP_<error>.html.var files by adding the line:
#
#   Alias /error/include/ "/your/include/path/"
#
# which allows you to create your own set of files by starting with the
# /var/www/error/include/ files and
# copying them to /your/include/path/, even on a per-VirtualHost basis.
#

Alias /error/ "/var/www/error/"

<IfModule mod_negotiation.c>
<IfModule mod_include.c>
    <Directory "/var/www/error">
        AllowOverride None
        Options IncludesNoExec
        AddOutputFilter Includes html
        AddHandler type-map var
        Order allow,deny
        Allow from all
        LanguagePriority en es de fr
        ForceLanguagePriority Prefer Fallback
    </Directory>

#    ErrorDocument 400 /error/HTTP_BAD_REQUEST.html.var
#    ErrorDocument 401 /error/HTTP_UNAUTHORIZED.html.var
#    ErrorDocument 403 /error/HTTP_FORBIDDEN.html.var
#    ErrorDocument 404 /error/HTTP_NOT_FOUND.html.var
#    ErrorDocument 405 /error/HTTP_METHOD_NOT_ALLOWED.html.var
#    ErrorDocument 408 /error/HTTP_REQUEST_TIME_OUT.html.var
#    ErrorDocument 410 /error/HTTP_GONE.html.var
#    ErrorDocument 411 /error/HTTP_LENGTH_REQUIRED.html.var
#    ErrorDocument 412 /error/HTTP_PRECONDITION_FAILED.html.var
#    ErrorDocument 413 /error/HTTP_REQUEST_ENTITY_TOO_LARGE.html.var
#    ErrorDocument 414 /error/HTTP_REQUEST_URI_TOO_LARGE.html.var
#    ErrorDocument 415 /error/HTTP_UNSUPPORTED_MEDIA_TYPE.html.var
#    ErrorDocument 500 /error/HTTP_INTERNAL_SERVER_ERROR.html.var
#    ErrorDocument 501 /error/HTTP_NOT_IMPLEMENTED.html.var
#    ErrorDocument 502 /error/HTTP_BAD_GATEWAY.html.var
#    ErrorDocument 503 /error/HTTP_SERVICE_UNAVAILABLE.html.var
#    ErrorDocument 506 /error/HTTP_VARIANT_ALSO_VARIES.html.var

</IfModule>
</IfModule>

#
# The following directives modify normal HTTP response behavior to
# handle known problems with browser implementations.
#
BrowserMatch "Mozilla/2" nokeepalive
BrowserMatch "MSIE 4\.0b2;" nokeepalive downgrade-1.0 force-response-1.0
BrowserMatch "RealPlayer 4\.0" force-response-1.0
BrowserMatch "Java/1\.0" force-response-1.0
BrowserMatch "JDK/1\.0" force-response-1.0

#
# The following directive disables redirects on non-GET requests for
# a directory that does not include the trailing slash.  This fixes a 
# problem with Microsoft WebFolders which does not appropriately handle 
# redirects for folders with DAV methods.
# Same deal with Apple's DAV filesystem and Gnome VFS support for DAV.
#
BrowserMatch "Microsoft Data Access Internet Publishing Provider" redirect-carefully
BrowserMatch "MS FrontPage" redirect-carefully
BrowserMatch "^WebDrive" redirect-carefully
BrowserMatch "^WebDAVFS/1.[0123]" redirect-carefully
BrowserMatch "^gnome-vfs/1.0" redirect-carefully
BrowserMatch "^XML Spy" redirect-carefully
BrowserMatch "^Dreamweaver-WebDAV-SCM1" redirect-carefully

#
# Allow server status reports generated by mod_status,
# with the URL of http://servername/server-status
# Change the ".example.com" to match your domain to enable.
#
#<Location /server-status>
#    SetHandler server-status
#    Order deny,allow
#    Deny from all
#    Allow from .example.com
#</Location>

#
# Allow remote server configuration reports, with the URL of
#  http://servername/server-info (requires that mod_info.c be loaded).
# Change the ".example.com" to match your domain to enable.
#
#<Location /server-info>
#    SetHandler server-info
#    Order deny,allow
#    Deny from all
#    Allow from .example.com
#</Location>

#
# Proxy Server directives. Uncomment the following lines to
# enable the proxy server:
#
#<IfModule mod_proxy.c>
#ProxyRequests On
#
#<Proxy *>
#    Order deny,allow
#    Deny from all
#    Allow from .example.com
#</Proxy>

#
# Enable/disable the handling of HTTP/1.1 "Via:" headers.
# ("Full" adds the server version; "Block" removes all outgoing Via: headers)
# Set to one of: Off | On | Full | Block
#
#ProxyVia On

#
# To enable a cache of proxied content, uncomment the following lines.
# See http://httpd.apache.org/docs/2.2/mod/mod_cache.html for more details.
#
#<IfModule mod_disk_cache.c>
#   CacheEnable disk /
#   CacheRoot "/var/cache/mod_proxy"
#</IfModule>
#

#</IfModule>
# End of proxy directives.

### Section 3: Virtual Hosts
#
# VirtualHost: If you want to maintain multiple domains/hostnames on your
# machine you can setup VirtualHost containers for them. Most configurations
# use only name-based virtual hosts so the server doesn't need to worry about
# IP addresses. This is indicated by the asterisks in the directives below.
#
# Please see the documentation at 
# <URL:http://httpd.apache.org/docs/2.2/vhosts/>
# for further details before you try to setup virtual hosts.
#
# You may use the command line option '-S' to verify your virtual host
# configuration.

#
# Use name-based virtual hosting.
#
#NameVirtualHost *:80
#
# NOTE: NameVirtualHost cannot be used without a port specifier 
# (e.g. :80) if mod_ssl is being used, due to the nature of the
# SSL protocol.
#

#
# VirtualHost example:
# Almost any Apache directive may go into a VirtualHost container.
# The first VirtualHost section is used for requests without a known
# server name.
#
#<VirtualHost *:80>
#    ServerAdmin webmaster@dummy-host.example.com
#    DocumentRoot /www/docs/dummy-host.example.com
#    ServerName dummy-host.example.com
#    ErrorLog logs/dummy-host.example.com-error_log
#    CustomLog logs/dummy-host.example.com-access_log common
#</VirtualHost>

<Directory /home/*/public_html>
    Options All
</Directory>
EOF

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- iptables 

# /etc/sysconfig/iptables
/bin/cp -a /etc/sysconfig/iptables /etc/sysconfig/iptables.rpmsave > /dev/null 2>&1
/bin/cat > /etc/sysconfig/iptables <<"EOF"
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -i eth1 -j ACCEPT
-A INPUT -i eth2 -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
-A INPUT -i eth2 -m state --state NEW -m tcp -p tcp --dport 25 -j ACCEPT
-A INPUT -i eth2 -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT
EOF


##########################################################################
%triggerin -- mod_suphp

# /etc/suphp.conf
/bin/cp -a /etc/suphp.conf /etc/suphp.conf.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^check_vhost_docroot=true/check_vhost_docroot=false/' /etc/suphp.conf
/bin/sed -i -e 's/^min_uid=.*/min_uid=1/' /etc/suphp.conf
/bin/sed -i -e 's/^min_gid=.*/min_gid=1/' /etc/suphp.conf

# /etc/httpd/conf.d/mod_suphp.conf
/bin/cp -a /etc/httpd/conf.d/mod_suphp.conf /etc/httpd/conf.d/mod_suphp.conf.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^#\(suPHP_AddHandler php5-script\)/\1/' /etc/httpd/conf.d/mod_suphp.conf

# /etc/httpd/conf.d/mod_suphp.conf
/bin/cp -a /etc/httpd/conf.d/mod_suphp.conf /etc/httpd/conf.d/mod_suphp.conf.rpmsave > /dev/null 2>&1
/bin/cat > /etc/httpd/conf.d/mod_suphp.conf <<"EOF"

# This is the Apache server configuration file providing suPHP support..
# It contains the configuration directives to instruct the server how to
# serve php pages while switching to the user context before rendering.

LoadModule suphp_module modules/mod_suphp.so


### Uncomment to activate mod_suphp
suPHP_AddHandler php5-script


# This option tells mod_suphp if a PHP-script requested on this server (or
# VirtualHost) should be run with the PHP-interpreter or returned to the
# browser "as it is".
<Directory /home/>
    suPHP_Engine on
</Directory>

# This option tells mod_suphp which path to pass on to the PHP-interpreter
# (by setting the PHPRC environment variable).
# Do *NOT* refer to a file but to the directory the file resists in.
#
# E.g.: If you want to use "/path/to/server/config/php.ini", use "suPHP_Config
# /path/to/server/config".
#
# If you don't use this option, PHP will use its compiled in default path.
#suPHP_ConfigPath /etc
EOF

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- mysql-server

# /etc/my.cnf
/bin/cp -a /etc/my.cnf /etc/my.cnf.rpmsave > /dev/null 2>&1
/bin/cat > /etc/my.cnf <<"EOF"
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
user=mysql
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
#skip-grant-tables
#skip-networking

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
EOF

# root
/sbin/service mysqld stop > /dev/null
/bin/sed -i -e 's/^#skip-grant-tables/skip-grant-tables/' /etc/my.cnf
/bin/sed -i -e 's/^#skip-networking/skip-networking/' /etc/my.cnf
/sbin/service mysqld start > /dev/null
/usr/bin/mysql --user=root > /dev/null 2>&1 <<"EOF"
UPDATE mysql.user SET Password=PASSWORD('crimson') WHERE User='root';
FLUSH PRIVILEGES;
EOF
/sbin/service mysqld stop > /dev/null
/bin/sed -i -e 's/^skip-grant-tables/#skip-grant-tables/' /etc/my.cnf
/bin/sed -i -e 's/^skip-networking/#skip-networking/' /etc/my.cnf
/sbin/service mysqld start > /dev/null

# jharvard, etc.
/usr/bin/mysql --force --user=root --password=crimson > /dev/null 2>&1 <<"EOF"
DROP USER ''@'%';
DROP USER ''@'localhost';
DROP USER ''@'localhost.localdomain';
DROP USER 'jharvard'@'%';
CREATE USER 'jharvard'@'%' IDENTIFIED BY 'crimson';
GRANT USAGE ON *.* TO 'jharvard'@'%' IDENTIFIED BY 'crimson';
GRANT ALL PRIVILEGES ON `jharvard\_%`.* TO 'jharvard'@'%';
EOF

/bin/true


##########################################################################
%triggerin -- nano

# /etc/nanorc
/bin/cp -a /etc/nanorc /etc/nanorc.rpmsave > /dev/null 2>&1
/bin/cat > /etc/nanorc <<"EOF"
set autoindent
set const
set fill 80
set matchbrackets "(<[{)>]}"
set nowrap
set smooth
set suspend
set tabsize 4
include "/usr/share/nano/c.nanorc"
include "/usr/share/nano/css.nanorc"
include "/usr/share/nano/html.nanorc"
include "/usr/share/nano/java.nanorc"
include "/usr/share/nano/makefile.nanorc"
include "/usr/share/nano/nanorc.nanorc"
include "/usr/share/nano/objc.nanorc"
include "/usr/share/nano/ocaml.nanorc"
include "/usr/share/nano/php.nanorc"
include "/usr/share/nano/python.nanorc"
include "/usr/share/nano/ruby.nanorc"
include "/usr/share/nano/xml.nanorc"
EOF


##########################################################################
%triggerin -- openssh-server

# /etc/ssh/sshd_config
/bin/sed -i -e 's/^#Banner none/Banner \/etc\/banner/' /etc/ssh/sshd_config
/bin/sed -i -e 's/^#ClientAliveInterval 0/ClientAliveInterval 60/' /etc/ssh/sshd_config
/bin/sed -i -e 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
/bin/sed -i -e 's/^#PrintMotd yes/PrintMotd no/' /etc/ssh/sshd_config
/bin/sed -i -e 's/^#TCPKeepAlive yes/TCPKeepAlive yes/' /etc/ssh/sshd_config

/sbin/service sshd restart > /dev/null 2>&1


##########################################################################
%triggerin -- php

# /etc/php.ini
/bin/cp -a /etc/php.ini /etc/php.ini.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^;date\.timezone =/date.timezone = America\/New_York/' /etc/php.ini
/bin/sed -i -e 's/^display_errors = Off/display_errors = On/' /etc/php.ini
/bin/sed -i -e 's/^display_startup_errors = Off/display_startup_errors = On/' /etc/php.ini
/bin/sed -i -e 's/^html_errors = Off/html_errors = On/' /etc/php.ini
/bin/sed -i -e 's/^short_open_tag = Off/short_open_tag = On/' /etc/php.ini
/bin/sed -i -e 's/^session\.save_path = .*/session.save_path = "\/tmp"/' /etc/php.ini

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- phpMyAdmin

# /etc/httpd/conf.d/phpMyAdmin.conf
/bin/cp -a /etc/httpd/conf.d/phpMyAdmin.conf /etc/httpd/conf.d/phpMyAdmin.conf.rpmsave > /dev/null 2>&1
/bin/cat > /etc/httpd/conf.d/phpMyAdmin.conf <<"EOF"
Alias /phpMyAdmin /usr/share/phpMyAdmin
Alias /phpmyadmin /usr/share/phpMyAdmin

<Directory /usr/share/phpMyAdmin/>
   Order Deny,Allow
   Deny from All
   Allow from 127.0.0.1
   Allow from 192.168.56.1
   Allow from 192.168.56.50
</Directory>

<Directory /usr/share/phpMyAdmin/setup/>
   Order Deny,Allow
   Deny from All
   Allow from 127.0.0.1
   Allow from 192.168.56.1
   Allow from 192.168.56.50
</Directory>

<Directory /usr/share/phpMyAdmin/libraries/>
   Order Deny,Allow
   Deny from All
   Allow from None
</Directory>

<Directory /usr/share/phpMyAdmin/setup/lib/>
   Order Deny,Allow
   Deny from All
   Allow from None
</Directory>

<Directory /usr/share/phpMyAdmin/setup/frames/>
   Order Deny,Allow
   Deny from All
   Allow from None
</Directory>
EOF

# /etc/phpMyAdmin/config.inc.php
/bin/cp -a /etc/phpMyAdmin/config.inc.php /etc/phpMyAdmin/config.inc.php.rpmsave > /dev/null 2>&1
/bin/cat > /etc/phpMyAdmin/config.inc.php <<"EOF"
<?php
/*
 * Generated configuration file
 * Generated by: phpMyAdmin 3.4.2 setup script
 */

/* Servers configuration */
$i = 0;

/* Server: localhost [1] */
$i++;
$cfg['Servers'][$i]['verbose'] = '';
$cfg['Servers'][$i]['host'] = 'localhost';
$cfg['Servers'][$i]['port'] = '';
$cfg['Servers'][$i]['socket'] = '';
$cfg['Servers'][$i]['connect_type'] = 'tcp';
$cfg['Servers'][$i]['extension'] = 'mysqli';
$cfg['Servers'][$i]['auth_type'] = 'http';
$cfg['Servers'][$i]['user'] = '';
$cfg['Servers'][$i]['password'] = '';
$cfg['Servers'][$i]['auth_http_realm'] = 'CS50 Appliance';
$cfg['Servers'][$i]['hide_db'] = 'information_schema|mysql|performance_schema';

/* End of servers configuration */

$cfg['UploadDir'] = '';
$cfg['SaveDir'] = '';
$cfg['AllowUserDropDatabase'] = true;
$cfg['SuggestDBName'] = false;
$cfg['DefaultLang'] = 'en';
$cfg['ServerDefault'] = 1;
$cfg['AjaxEnable'] = false;
$cfg['VersionCheck'] = false;
$cfg['DisplayDatabasesList'] = 0;
$cfg['ShowPhpInfo'] = true;
$cfg['ShowAll'] = true;
$cfg['NavigationBarIconic'] = 'both';
$cfg['PmaNoRelation_DisableWarning'] = true;
?>
EOF

/sbin/service httpd restart > /dev/null 2>&1


##########################################################################
%triggerin -- rsnapshot

# /etc/rsnapshot.conf
/bin/cp -a /etc/rsnapshot.conf /etc/rsnapshot.conf.rpmsave > /dev/null 2>&1
/bin/cat > /etc/rsnapshot.conf <<"EOF"
config_version	1.2
snapshot_root	/.snapshots/
cmd_rm	/bin/rm
cmd_rsync	/usr/bin/rsync
cmd_logger	/usr/bin/logger
interval	minutely	6
verbose	2
loglevel	3
lockfile	/var/run/rsnapshot.pid
include	*/
include	*.c
include	*.css
include	*.h
include	*.js
include	*.php
include	*.py
include	*.rb
exclude	*
include	Makefile
backup	/home	./
EOF

# /etc/cron.d/rsnapshot
/bin/cat > /etc/cron.d/rsnapshot <<"EOF"
*/10 * * * * root /usr/bin/rsnapshot minutely
EOF


##########################################################################
%triggerin -- setup

# /etc/hosts
/bin/cp -a /etc/hosts /etc/hosts.rpmsave > /dev/null 2>&1
/bin/cat > /etc/hosts <<"EOF"
127.0.0.1   appliance appliance.localdomain localhost localhost.localdomain
EOF


##########################################################################
%triggerin -- sudo

# /etc/sudoers
/bin/cp -a /etc/sudoers /etc/sudoers.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^# \(%wheel[ \t]*ALL=(ALL)[ \t]*ALL\)$/\1/' /etc/sudoers


##########################################################################
%triggerin -- usermin

# /etc/usermin/miniserv.conf
/bin/cp -a /etc/usermin/miniserv.conf /etc/usermin/miniserv.conf.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^ssl=1/ssl=0/' /etc/usermin/miniserv.conf

# /etc/usermin/changepass/config
/bin/cp -a /etc/usermin/changepass/config /etc/usermin/changepass/config.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^passwd_cmd=file/passwd_cmd=/' /etc/usermin/changepass/config

# /etc/usermin/webmin.acl
/bin/cp -a /etc/usermin/webmin.acl /etc/usermin/webmin.acl.rpmsave > /dev/null 2>&1
/bin/cat > /etc/usermin/webmin.acl <<"EOF"
user: changepass chfn cshrc file htaccess htaccess-htpasswd language man proc quota ssh telnet theme updown 
EOF

/sbin/service usermin restart > /dev/null 2>&1


##########################################################################
%triggerin -- vim

# /etc/vimrc
/bin/cp -a /etc/vimrc /etc/vimrc.rpmsave > /dev/null 2>&1
/bin/cat > /etc/vimrc <<"EOF"
version 6.x
set fileformats=unix
syntax on

hi Comment      term=bold       ctermfg=Yellow      guifg=LightBlue
hi Constant     term=underline  ctermfg=Green       guifg=Green             gui=underline
hi Identifier   term=underline  ctermfg=LightCyan   guifg=DarkCyan
hi Statement    term=bold       ctermfg=Magenta     guifg=Brown             gui=bold
hi PreProc      term=underline  ctermfg=Magenta     guifg=Purple
hi Type         term=underline  ctermfg=DarkGreen   guifg=SeaGreen          gui=bold
hi Special      term=bold       ctermfg=LightBlue   guifg=SlateBlue         gui=underline

hi Comment      cterm=NONE
hi Constant     cterm=NONE
hi Identifier   cterm=NONE
hi Statement    cterm=NONE
hi PreProc      cterm=NONE
hi Type         cterm=NONE
hi Special      cterm=NONE

set backspace=2

set gfn=-b&h-lucidatypewriter-medium-r-normal-*-*-120-*-*-m-*-iso8859-1
set whichwrap=<,>,[,]
set autoindent
set incsearch
set background=dark
set formatoptions=tcq2
set mouse=a
set ruler
set shiftwidth=4
set showmatch
set tabstop=4
set textmode

set tabstop=4
set expandtab
set ruler
set sw=4
set showmatch
set ai

hi Normal guibg=black
hi Normal guifg=gray80

set nobackup
set cmdheight=2

set nocompatible
EOF


##########################################################################
%triggerin -- webmin

# /etc/webmin/miniserv.conf
/bin/cp -a /etc/webmin/miniserv.conf /etc/webmin/miniserv.conf.rpmsave > /dev/null 2>&1
/bin/sed -i -e 's/^ssl=1/ssl=0/' /etc/webmin/miniserv.conf

# /etc/webmin/proftpd/config
/bin/cp -a /etc/webmin/proftpd/config /etc/webmin/proftpd/config.rpmsave > /dev/null 2>&1
/bin/cat > /etc/webmin/proftpd/config <<"EOF"
ftpusers=/etc/ftpusers
pid_file=/run/proftpd/proftpd.pid
test_always=0
test_config=1
proftpd_path=/usr/sbin/proftpd
test_manual=0
proftpd_conf=/etc/proftpd.conf
start_cmd=
stop_cmd=
add_file=
EOF

/sbin/service webmin restart > /dev/null 2>&1


##########################################################################
%triggerin -- xfce4-panel

# /etc/xdg/xfce4/panel/default.xml
/bin/cp -a /etc/xdg/xfce4/panel/default.xml /etc/xdg/xfce4/panel/default.xml.rpmsave > /dev/null 2>&1
/bin/cat > /etc/xdg/xfce4/panel/default.xml <<"EOF"
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfce4-panel" version="1.0">
  <property name="panels" type="uint" value="1">
    <property name="panel-0" type="empty">
      <property name="position" type="string" value="p=12;x=67;y=743"/>
      <property name="length" type="uint" value="100"/>
      <property name="position-locked" type="bool" value="true"/>
      <property name="autohide" type="bool" value="false"/>
      <property name="span-monitors" type="bool" value="false"/>
      <property name="horizontal" type="bool" value="true"/>
      <property name="size" type="uint" value="30"/>
      <property name="length-adjust" type="bool" value="true"/>
      <property name="enter-opacity" type="uint" value="100"/>
      <property name="leave-opacity" type="uint" value="100"/>
      <property name="background-alpha" type="uint" value="100"/>
      <property name="background-style" type="uint" value="0"/>
      <property name="background-color" type="array">
        <value type="uint" value="60909"/>
        <value type="uint" value="60652"/>
        <value type="uint" value="60395"/>
        <value type="uint" value="65535"/>
      </property>
      <property name="background-image" type="string" value=""/>
      <property name="output-name" type="string" value=""/>
      <property name="disable-struts" type="bool" value="false"/>
      <property name="plugin-ids" type="array">
        <value type="int" value="1"/>
        <value type="int" value="2"/>
        <value type="int" value="3"/>
        <value type="int" value="4"/>
        <value type="int" value="5"/>
        <value type="int" value="6"/>
        <value type="int" value="7"/>
        <value type="int" value="8"/>
        <value type="int" value="9"/>
        <value type="int" value="10"/>
        <value type="int" value="11"/>
      </property>
    </property>
  </property>
  <property name="plugins" type="empty">
    <property name="plugin-1" type="string" value="applicationsmenu">
      <property name="button-title" type="string" value=" Menu"/>
      <property name="button-icon" type="string" value="/usr/share/icons/hicolor/32x32/cs50/menu.png"/>
    </property>
    <property name="plugin-2" type="string" value="separator"/>
    <property name="plugin-3" type="string" value="launcher">
      <property name="items" type="array">
        <value type="string" value="Eclipse.desktop"/>
      </property>
    </property>
    <property name="plugin-4" type="string" value="launcher">
      <property name="items" type="array">
        <value type="string" value="Firefox.desktop"/>
      </property>
    </property>
    <property name="plugin-5" type="string" value="launcher">
      <property name="items" type="array">
        <value type="string" value="Terminal.desktop"/>
      </property>
    </property>
    <property name="plugin-6" type="string" value="separator"/>
    <property name="plugin-7" type="string" value="showdesktop"/>
    <property name="plugin-8" type="string" value="separator"/>
    <property name="plugin-9" type="string" value="tasklist">
      <property name="show-handle" type="bool" value="false"/>
    </property>
    <property name="plugin-10" type="string" value="separator"/>
    <property name="plugin-11" type="string" value="actions"/>
  </property>
</channel>
EOF

# /etc/skel/.config/xfce4/panel/launcher-3/Eclipse.desktop
/bin/mkdir -p /etc/skel/.config/xfce4/panel/launcher-3
/bin/cat > /etc/skel/.config/xfce4/panel/launcher-3/Eclipse.desktop <<"EOF"
[Desktop Entry]
Version=1.0
Name=Eclipse
Exec=eclipse
Icon=/usr/share/icons/hicolor/32x32/apps/eclipse.png
Terminal=false
Type=Application
Categories=Development;IDE;
X-XFCE-Source=file:///usr/share/applications/eclipse.desktop
EOF

# /etc/skel/.config/xfce4/panel/launcher-4/Firefox.desktop
/bin/mkdir -p /etc/skel/.config/xfce4/panel/launcher-4
/bin/cat > /etc/skel/.config/xfce4/panel/launcher-4/Firefox.desktop <<"EOF"
[Desktop Entry]
Version=1.0
Name=Firefox
GenericName=Web Browser
Comment=Browse the Web
Exec=firefox %u
Icon=firefox
Terminal=false
Type=Application
StartupWMClass=Firefox-bin
MimeType=text/html;text/xml;application/xhtml+xml;application/vnd.mozilla.xul+xml;text/mml;x-scheme-handler/http;x-scheme-handler/https;
StartupNotify=true
Categories=Network;WebBrowser;
X-Desktop-File-Install-Version=0.18
X-XFCE-Source=file:///usr/share/applications/mozilla-firefox.desktop
EOF

# /etc/skel/.config/xfce4/panel/launcher-5/Terminal.desktop
/bin/mkdir -p /etc/skel/.config/xfce4/panel/launcher-5
/bin/cat > /etc/skel/.config/xfce4/panel/launcher-5/Terminal.desktop <<"EOF"
[Desktop Entry]
Version=1.0
Name=Terminal
Comment=Terminal Emulator
GenericName=Terminal Emulator
Exec=Terminal
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=GTK;System;TerminalEmulator;Utility;
StartupNotify=true
X-Desktop-File-Install-Version=0.18
X-XFCE-Source=file:///usr/share/applications/Terminal.desktop
EOF

# /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml
/bin/mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
/bin/ln -sf /etc/xdg/xfce4/panel/default.xml /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml

# /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
/bin/mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
/bin/cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml <<"EOF"
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfwm4" version="1.0">
  <property name="general" type="empty">
    <property name="activate_action" type="string" value="bring"/>
    <property name="borderless_maximize" type="bool" value="true"/>
    <property name="box_move" type="bool" value="false"/>
    <property name="box_resize" type="bool" value="false"/>
    <property name="button_layout" type="string" value="O|SHMC"/>
    <property name="button_offset" type="int" value="0"/>
    <property name="button_spacing" type="int" value="0"/>
    <property name="click_to_focus" type="bool" value="true"/>
    <property name="focus_delay" type="int" value="250"/>
    <property name="cycle_apps_only" type="bool" value="false"/>
    <property name="cycle_draw_frame" type="bool" value="true"/>
    <property name="cycle_hidden" type="bool" value="true"/>
    <property name="cycle_minimum" type="bool" value="true"/>
    <property name="cycle_workspaces" type="bool" value="false"/>
    <property name="double_click_time" type="int" value="250"/>
    <property name="double_click_distance" type="int" value="5"/>
    <property name="double_click_action" type="string" value="maximize"/>
    <property name="easy_click" type="string" value="Alt"/>
    <property name="focus_hint" type="bool" value="true"/>
    <property name="focus_new" type="bool" value="true"/>
    <property name="frame_opacity" type="int" value="100"/>
    <property name="full_width_title" type="bool" value="true"/>
    <property name="inactive_opacity" type="int" value="100"/>
    <property name="maximized_offset" type="int" value="0"/>
    <property name="move_opacity" type="int" value="100"/>
    <property name="placement_ratio" type="int" value="20"/>
    <property name="placement_mode" type="string" value="center"/>
    <property name="popup_opacity" type="int" value="100"/>
    <property name="mousewheel_rollup" type="bool" value="true"/>
    <property name="prevent_focus_stealing" type="bool" value="false"/>
    <property name="raise_delay" type="int" value="250"/>
    <property name="raise_on_click" type="bool" value="true"/>
    <property name="raise_on_focus" type="bool" value="false"/>
    <property name="raise_with_any_button" type="bool" value="true"/>
    <property name="repeat_urgent_blink" type="bool" value="false"/>
    <property name="resize_opacity" type="int" value="100"/>
    <property name="restore_on_move" type="bool" value="true"/>
    <property name="scroll_workspaces" type="bool" value="true"/>
    <property name="shadow_delta_height" type="int" value="0"/>
    <property name="shadow_delta_width" type="int" value="0"/>
    <property name="shadow_delta_x" type="int" value="0"/>
    <property name="shadow_delta_y" type="int" value="-3"/>
    <property name="shadow_opacity" type="int" value="50"/>
    <property name="show_app_icon" type="bool" value="false"/>
    <property name="show_dock_shadow" type="bool" value="true"/>
    <property name="show_frame_shadow" type="bool" value="false"/>
    <property name="show_popup_shadow" type="bool" value="false"/>
    <property name="snap_resist" type="bool" value="false"/>
    <property name="snap_to_border" type="bool" value="true"/>
    <property name="workspace_names" type="array">
      <value type="string" value="Workspace 1"/>
    </property>
    <property name="snap_to_windows" type="bool" value="false"/>
    <property name="snap_width" type="int" value="10"/>
    <property name="theme" type="string" value="Nodoka"/>
    <property name="title_alignment" type="string" value="center"/>
    <property name="title_font" type="string" value="Sans Bold 9"/>
    <property name="title_horizontal_offset" type="int" value="0"/>
    <property name="title_shadow_active" type="string" value="false"/>
    <property name="title_shadow_inactive" type="string" value="false"/>
    <property name="title_vertical_offset_active" type="int" value="0"/>
    <property name="title_vertical_offset_inactive" type="int" value="0"/>
    <property name="toggle_workspaces" type="bool" value="false"/>
    <property name="unredirect_overlays" type="bool" value="true"/>
    <property name="urgent_blink" type="bool" value="false"/>
    <property name="use_compositing" type="bool" value="false"/>
    <property name="workspace_count" type="int" value="1"/>
    <property name="wrap_cycle" type="bool" value="true"/>
    <property name="wrap_layout" type="bool" value="true"/>
    <property name="wrap_resistance" type="int" value="10"/>
    <property name="wrap_windows" type="bool" value="true"/>
    <property name="wrap_workspaces" type="bool" value="false"/>
  </property>
</channel>

EOF

# /home/jharvard/.config/xfce4/panel/
/usr/bin/sudo -u jharvard /bin/mkdir -p /home/jharvard/.config/xfce4/panel/
/usr/bin/sudo -u jharvard /usr/bin/rsync --delete --copy-links --recursive /etc/skel/.config/xfce4/panel/* /home/jharvard/.config/xfce4/panel/

# /home/jharvard/.config/xfce4/xfconf/
/usr/bin/sudo -u jharvard /bin/mkdir -p /home/jharvard/.config/xfce4/xfconf/
/usr/bin/sudo -u jharvard /usr/bin/rsync --delete --copy-links --recursive /etc/skel/.config/xfce4/xfconf/* /home/jharvard/.config/xfce4/xfconf/

# /root/.config/xfce4/panel/
/bin/mkdir -p /root/.config/xfce4/panel/
/usr/bin/rsync --copy-links --delete --recursive /etc/skel/.config/xfce4/panel/* /root/.config/xfce4/panel/

# /root/.config/xfce4/xfconf/
/bin/mkdir -p /root/.config/xfce4/xfconf/
/usr/bin/rsync --copy-links --delete --recursive /etc/skel/.config/xfce4/xfconf/* /root/.config/xfce4/xfconf/


##########################################################################
%triggerin -- xorg-x11-fonts-misc

# /etc/X11/Xresources
/bin/cp -a /etc/X11/Xresources /etc/X11/Xresources.rpmsave > /dev/null 2>&1
/bin/cat > /etc/X11/Xresources <<"EOF"
! This is the global resources file that is loaded when
! all users log in, as well as for the login screen

! Fix the Xft dpi to 96; this prevents tiny fonts
! or HUGE fonts depending on the screen size.
Xft.dpi: 96

! hintstyle: medium means that (for Postscript fonts) we
! position the stems for maximum constrast and consistency
! but do not force the stems to integral widths. hintnone,
! hintslight, and hintfull are the other possibilities.
Xft.hintstyle: hintmedium
Xft.hinting: true

! Give XTerm and Emacs a black background and a clean monospace font.
XTerm*font:           9x15
XTerm*reverseVideo:   on

Emacs*font:           9x15
Emacs*reverseVideo:   on
EOF


##########################################################################
%files
%defattr(-,root,root,-)
/


##########################################################################
%changelog
* Sat Jul 23 2011 David J. Malan <dmalan@harvard.edu> - 2.0-11
- Defined EDITOR.
- Made release distribution-specific with %{?dist}.

* Sat Jul 16 2011 David J. Malan <dmalan@harvard.edu> - 2.0-9
- Various updates.

* Sat Jul 16 2011 David J. Malan <dmalan@harvard.edu> - 2.0-7
- Various updates.

* Sat Jul 16 2011 David J. Malan <dmalan@harvard.edu> - 2.0-6
- Reconfigured phpMyAdmin.

* Wed Jul 13 2011 David J. Malan <dmalan@harvard.edu> - 2.0-1
- Removed Fall 2009 from Menu.

* Tue Jul 12 2011 David J. Malan <dmalan@harvard.edu> - 
- Initial build
