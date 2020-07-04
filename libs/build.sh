gcc -c -fpic open3dLines.c
gcc -shared -o "libopen3dLinesLib.so" "open3dLines.o"
