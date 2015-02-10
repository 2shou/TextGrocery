rem make sure you have install vs2010 or other cpp compile tools
cd "tgrocery\learner"
call "vcvars32.bat"
nmake.exe /f Makefile lib
nmake.exe /f Makefile clean
cd "liblinear"
nmake.exe /f Makefile lib
nmake.exe /f Makefile clean
cd "../../.."
