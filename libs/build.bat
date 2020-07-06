gcc -c -fpic open3dLines.c
gcc -shared -o "libopen3dLinesLib.dll" "open3dLines.o"
