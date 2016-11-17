# Leap
Repo for codes for integrating gestures from Leap motion with Blender/OpenGL

# Dive In

# Requirements
* Python3
* PyOpenGL
* PyGame
* numpy
* numpy-quaternion
* numa

# Install
* Installation instructions (assuming Ubuntu, 64 bit):
  ```bash
  dpkg -i ./SDK/Leap*x64.deb # x86.deb for 32 bit versions
  ```

* Only if case the system uses systemd instead of Upstart, do the
following:
  ```bash
  cp systemd/leapd.service /lib/systemd/system/leapd.service
  cp /lib/systemd/system/leapd.service /etc/systemd/system/leapd.service
  systemctl daemon-reload
  systemctl enable leapd
  systemctl leapd start
  ```

* Follow these by:
  ```bash
  apt install -f
  apt install python3 python3-pip python3-virtualenv
  pip3 install PyOpenGL PyOpenGL_accelerate
  ```
* For more details, see
[Installation](http://pyopengl.sourceforge.net/documentation/installation.html) and [Tutorial](http://pyopengl.sourceforge.net/context/tutorials/shader_intro.html) instructions

# Contributors
@kunaltyagi
@PradyumnaParuchuri

# Dev/Code Guidelines
* [Leap](https://api.leapmotion.com/documentation/v2/python/devguide/Leap_Guides.html)
* Pylint and pep8

# SDK Documentation
* [Migrate to Py 3.0](https://support.leapmotion.com/hc/en-us/articles/223784048)
* [Python v2 API](https://api.leapmotion.com/documentation/v2/python/index.html)

# Idea Inspiration
* [Solidworks Plugin](https://apps.leapmotion.com/apps/ossewa-solidworks-plug-in/windows)
* [Future of Design (video)](https://www.youtube.com/watch?v=xNqs_S-zEBY)

# Potential sources of code inspiration
* [OpenLeap](https://github.com/openleap)
