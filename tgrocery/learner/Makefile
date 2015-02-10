#You must ensure nmake.exe, cl.exe, link.exe are in system path.
#VCVARS32.bat
#Under dosbox prompt
#nmake -f Makefile.win

##########################################
CXX = cl.exe
CFLAGS = /nologo /O2 /EHsc /I. /D _WIN32 /D _CRT_SECURE_NO_DEPRECATE
TARGET = .

lib: util.c
	$(CXX) $(CFLAGS) -LD util.c /Iliblinear -Fe$(TARGET)\util -link -DEF:util.def

clean:
	 -erase /Q *.obj