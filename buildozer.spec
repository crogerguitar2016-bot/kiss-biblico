[app]

title = Kiss

package.name = kissbiblico
package.domain = com.croger

source.dir = .

source.include_exts = py,png,jpg,jpeg,json,kv,atlas,txt

source.exclude_dirs = backup,saves,tools,.git,.github,__pycache__

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

icon.filename = %(source.dir)s/icon.png


# ======================================================
# ANDROID
# ======================================================

android.api = 36
android.minapi = 24

android.ndk = 29

android.archs = arm64-v8a

android.sdk_path = /home/runner/android-sdk

android.accept_sdk_license = True


# ======================================================
# PYTHON-FOR-ANDROID
# ======================================================

p4a.branch = develop
p4a.source_dir = /home/runner/p4a


# ======================================================
# BUILDOZER
# ======================================================

[buildozer]

log_level = 2
warn_on_root = 1
