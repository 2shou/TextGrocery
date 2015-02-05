# make sure you have install vs2010 or other cpp compile tools
cd "tgrocery\learner\liblinear"
mkdir "windows"
call "vcvars32.bat"
nmake.exe /f Makefile lib
nmake.exe /f Makefile clean
copy "windows\liblinear.dll" "C:\windows\system32"