[app]

title = Kiss

package.name = kissbiblico
package.domain = com.croger

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,kv,atlas,ttf,otf

source.exclude_dirs = backup,saves,tools,.git,.github,__pycache__

requirements = python3,kivy

version = 1.0

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png

p4a.branch = develop
p4a.source_dir = /home/runner/p4a

android.archs = arm64-v8a
android.minapi = 24
android.api = 36
android.ndk = 29

android.sdk_path = /home/runner/android-sdk
android.accept_sdk_license = True


[buildozer]

log_level = 2
warn_on_root = 1
