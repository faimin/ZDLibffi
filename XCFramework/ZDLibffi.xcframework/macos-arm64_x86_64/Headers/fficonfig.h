#if defined(__arm64__) && !defined(__ILP32__)

#if __has_include(<fficonfig_arm64.h>)
#include <fficonfig_arm64.h>
#else
#include "fficonfig_arm64.h"
#endif


#endif
#if defined(__arm64__) && defined(__ILP32__)

#if __has_include(<fficonfig_arm64_32.h>)
#include <fficonfig_arm64_32.h>
#else
#include "fficonfig_arm64_32.h"
#endif


#endif
#if defined(__x86_64__)

#if __has_include(<fficonfig_x86_64.h>)
#include <fficonfig_x86_64.h>
#else
#include "fficonfig_x86_64.h"
#endif


#endif
