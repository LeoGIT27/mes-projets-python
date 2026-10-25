# NotSoffiz

Native C++/Win32 dialogue prototype using the assets in `assets/`.

From a **Developer PowerShell for Visual Studio**:

```powershell
cmake -S . -B build
cmake --build build --config Release
.\build\Release\NotSoffiz.exe
```

The warning alternates between `NotSoffiz.jpg` and `TalkingNotSoffiz.jpg` while
playing `NotSoffizSFX1.m4a`. Press Enter for the threat dialogue, then Enter
again to open two `AngryNotSoffiz.jpg` windows. The angry scene uses the
virtual-screen bounds for placement, shakes only those two windows briefly,
and keeps the two angry windows in independent, continuous, bounded,
T-Rex-like tremors. Each window uses `BitBlt` only for its own back-buffered
rendering; the desktop and other applications are never copied or moved.
Closing the main dialogue also triggers the angry scene. The prototype does
not move unrelated desktop windows or launch unbounded parallel audio.