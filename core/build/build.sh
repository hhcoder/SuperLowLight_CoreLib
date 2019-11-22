RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "\n${GREEN}==== Build Lib ====${NC}"
echo -e "build flavor : ${PURPLE}$1${NC}" 
echo -e "build target : ${PURPLE}$2${NC}"
    
CORE_GEN_LIB="lib$CORE_GEN_NAME.a"
ANDROID_ARM64_TOOLCHAIN="../../Android_Arm64_toolchain"
LIB_ROOT="../core/

# case $1 in
#     mac)
#         # LIBRARY_OPTIONS="-L $./$1/bin/"
#     ;;
#     linux)
#         LIBRARY_OPTIONS="$./$1/lib/libHalide.a $CORE_GEN_DIR$CORE_GEN_LIB"
#     ;;
#     *)
#         echo -e "\n${RED}Wrong build flavor: $1${NC}"
#         exit -2
#     ;;    
# esac


INCLUDES="-I $HALIDE_ROOT/include/ -I $HALIDE_ROOT/tools/ -I $CORE_GEN_DIR"

SRCS="process.cpp "

COMPILER_OPTION="-std=c++11 -O3 -g -fno-rtti -Wall -v"
LINKER_OPTIONS="-ldl -lpthread -lz "
OUT_DIR="./bin/"
OUT_TARGET="nr "
OUT_OPTION="-o $OUT_DIR$OUT_TARGET"

if [ ! -d "$OUT_DIR" ]; then
  mkdir $OUT_DIR
fi

case $2 in
    arm|hvx128|hvx64)
        echo -e "\n${PURPLE}Generate on device runnable${NC}"
        CXX=$ANDROID_ARM64_TOOLCHAIN/bin/aarch64-linux-android-c++
		echo $CXX $COMPILER_OPTION $INCLUDES $SRCS $LIBRARY_OPTIONS $OUT_OPTION -llog -fPIE -pie
        $CXX $COMPILER_OPTION $INCLUDES $SRCS $LIBRARY_OPTIONS $OUT_OPTION -llog -fPIE -pie
        ;;
    host)
        echo -e "\n${PURPLE}Generate Host runnable${NC}"
        CXX="g++"
        $CXX $COMPILER_OPTION $INCLUDES $SRCS $LIBRARY_OPTIONS $OUT_OPTION $LINKER_OPTIONS
        ;;
    *)
        echo -e "\n${RED} Wrong build target: $2${NC}"
        echo -e "\n${RED} Wrong build target: $2${NC}"
        exit -2
    ;;          
esac

cp $OUT_DIR$OUT_TARGET $CORE_GEN_DIR

if [ $? -eq 0 ]; then

    echo -e "\n${BLUE}Build Lib Successfully${NC}\n"

else
    echo -e "\n${RED}Build Lib Failed${NC}\n"
fi
