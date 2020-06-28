# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this project uses [Semantic Versioning](http://semver.org/).

# [0.3.0] - 2020-6-28
### Added
 - Background colors to buttons after clicking them
 - Ability to remove annotations by re-clicking a button, and also removing its color
 - Initializing `annotation_dict` as a `collections.default_dict` to make adding new elements simpler
### Changed
 - When annotations are complete, current image on display is cleared
 - When `options` is not a `dictionary`, a `ValueError`
 - Asset name is displayed in `count_label`

# [0.2.0] - 2019-9-6
### Added
 - readded the skip button to the multi-label annotator

# [0.1.2] - 2019-9-6
### Changed
 - doc changes and more gifs

# [0.1.1] - 2019-9-6
### Changed
 - setup.py bug

# [0.1.0] - 2019-9-6
### Added
 - inital commit for multi_label_pigeon to add function for multi-label annotation
