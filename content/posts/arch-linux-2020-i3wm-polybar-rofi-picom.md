---
title: "Arch Linux 2020 i3wm polybar rofi picom"
date: 2020-05-03T21:20:30+02:00
draft: false
---

### the video
the following video shows the whole installation below the video you'll find the transcript

{{<  youtube_lazy ytid="PSutMZ0phXs" yttitle="test title" >}}

### fix for the last part
typo in the /etc/fstab file

### general stuff
we now create a non root  user
```
useradd -m loeken
passwd loeken
gpasswd -a loeken wheel
```

we now uncomment the line in the sudoers file to enable access for the wheel group
#### **`/etc/sudoers`**
```
%sudo	ALL=(ALL) ALL
```
### i3wm installation

we start by installing i3-gaps this is a fork of i3 which has a few more features git
```
sudo pacman -S i3-gaps xorg-xinit xorg-server terminator
```

### installation polybar

I've upped a small repo to github with a few files lets grab that

```
mkdir Projects
git clone https://github.com/loeken/dotfiles
cd dotfiles
```


#### installation of rofi
```
sudo pacman -S rofi
mkdir -p ~/.config/rofi
cp rofi/config ~/.config/rofi/config
cp .xinitrc ~/
```

### increase build times my using multiple cores to build
we edit the /etc/makepkg.conf and set the MAKEFLAGS -j count to the amount of cores we have in our system to speed up the build processes.
#### **`/etc/makepkg.conf`**
```
#-- Make Flags: change this for DistCC/SMP systems
MAKEFLAGS="-j8"
#-- Debugging flags
```

### installation of pacaur
in the following part we are going to install pacaur a package manage that accepts syntax similar to pacman but installs from the aur instead

```
git clone https://aur.archlinux.org/auracle-git.git
cd auracle-git
makepkg -s
sudo pacman -U auracle-git-r315.d4b4548-1-x86_64.pkg.tar.xz
cd ~/Projects
git clone https://aur.archlinux.org/pacaur.git
cd pacaur
makepkg -s
sudo pacman -U pacaur-4.8.6-1-any.pkg.tar.xz
```
#### installation of polybar
```
pacaur -S polybar siji-git
mkdir -p ~/.config/polybar
sudo cp polybar/config ~/.config/polybar/config
sudo cp loadbar /usr/local/bin/loadbar
```

#### installation of picom
```
sudo pacman -S picom
mkdir -p ~/.config/picom
cp picom/picom.conf ~/.config/picom/picom.conf
```

#### update of i3 config
```
mkdir -p ~/.config/i3
cp i3/config ~/.config/i3/config
cp .xinitrc ~/
```

#### installation of feh
to apply backgrounds
```
sudo pacman -S feh
```
#### installation of xrandr
xrandr is the best tool to setup desktop resolution etc
```
sudo pacman -S xorg-xrandr
xrandr --output Virtual-1 --mode 1920x1080
```

#### copy over .xinitrc 
```
cp .xinitrc ~/
```