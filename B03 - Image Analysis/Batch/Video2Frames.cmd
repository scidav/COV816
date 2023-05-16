for %%F in (*.mp4) do (
If not Exist "%%~nF" MkDir "%%~nF"
"C:\ffmpeg\bin\ffmpeg.exe" -i %%F -r 2 -qscale:v 2 %%~nF\%%~nF-%%05d.jpeg
)