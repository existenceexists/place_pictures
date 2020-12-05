# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2020-12-05
### Added
- File README.md with description of the project.
- This CHANGELOG.md file.
- Dependencies: 
Pygame 1.8.0 or higher version, FunnyGUI, FunnyMenuSystem, FunnyPathGetter.
- Create GUI. As GUI widgets toolkits use projects 
FunnyGUI and FunnyMenuSystem and FunnyPathGetter.
- GUI widget menu bar using FunnyMenuSystem.
- GUI widgets dialog windows using GUI FunnyGUI. 
Develop GUI FunnyGUI to suit the needs of this project.
- GUI widgets path getting dialog windows using FunnyPathGetter.
- Option to add map background image on that user can move the viewed part 
up and down and right and left using arrow keys on keybord.
- Option to create background image filled with a color.
Let user specify width and height
and a color the background image will be filled with.
Set background image at the start of the application
to be filled with color black and to have width 2000 and height 2000.
- Option to open (load) image file and display it on top of background image.
- Move pictures if user uses arrow keyboard keys to move on map.
- Move selected pictures to position on that user clicked with mouse.
- Pictures' state "selected". 
Picture(s) in state "selected" is(are) surrounded by yellow square.
Select a picture on that user clicks with mouse 
and deselect the picture again if another picture is selected. 
Modify this behaviour with additional features.
- Pictures' state "highlighted". 
Picture in state "highlighted" is surrounded by white square.
Highlight topmost picture above that mouse is hovering 
and unhighlight the highlighted picture if mouse moves from the picture.
- When opening an image display a dialog window GUI widget 
used to let user specify percent the loaded image will be scaled to 
and layer number the loaded image will be added to.
- Option to start the application with command line arguments 
--width and --height that specify application window size.
- Option to scale selected pictures.
- Option to save game.
- Option to load saved game.
- Savegame files format.
- Option to copy selected pictures.
- Option to keep pictures in different layers.
Pictures in higher layers are drawn on top of pictures in lower layers.
There will be no empty layers i.e. layers that hold no pictures.
- Option to create new layer and move selected pictures into the new layer.
- Option to move selected pictures to existing layer.
- Information labels that provide information 
about highlighted picture and selected pictures.
- Option to turn on and off information labels.
- Option to turn on and off selecting of multiple pictures 
- Deselect picture if user clicked on it again for the second time.
- Option to turn on and off selecting of pictures.
- Option to deselect all selected pictures.
- Option to select pictures with same image file(s)
as selected picture(s).
- Option to select pictures with same image file(s) and scale 
as selected picture(s).
- Option to delete selected pictures.
- Option to limit selecting to selecting among pictures 
that are in specific layers.
- Option to move layers to a different position in relation to other layers.
- Option to join two or more neighbouring layers.
- Do not allow pictures to be moved outside map borders.
- Option to quit the application.
- Display exception that rises when user tries to open a picture file
and it can not be opened.
- Display exception that rises when user tries to open a map file
and it can not be opened.
- Buttons in main menu representing planned features 
not yet implemented. Some of the main menu bar menu items 
do nothing now when user clicks on them with mouse. 
They represent planned features not yet implemented.
- License this project under the 
Do What The Fuck You Want To Public License, Version 2

[Unreleased]: https://github.com/existenceexists/place_pictures/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/existenceexists/place_pictures/releases/tag/v0.1.0

