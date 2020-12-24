//
//  Libffi_iOS.h
//  Libffi-iOS
//
//  Created by Zero.D.Saber on 2020/12/23.
//

#import <Foundation/Foundation.h>

//! Project version number for Libffi_iOS.
FOUNDATION_EXPORT double Libffi_iOSVersionNumber;

//! Project version string for Libffi_iOS.
FOUNDATION_EXPORT const unsigned char Libffi_iOSVersionString[];

// In this header, you should import all the public headers of your framework using statements like #import <Libffi_iOS/PublicHeader.h>

#if __has_include(<Libffi_iOS/ffi.h>)
#import <Libffi_iOS/ffi.h>
#elif __has_include(<ffi.h>)
#import <ffi.h>
#elif __has_include("ffi.h")
#import "ffi.h"
#endif


// libffi v3.3
// architectures: x86_64 i386 armv7 arm64
// make by faimin(Zero.D.Saber)
