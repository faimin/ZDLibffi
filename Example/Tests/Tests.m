//
//  Libffi_iOSTests.m
//  Libffi_iOSTests
//
//  Created by faimin on 12/23/2020.
//  Copyright (c) 2020 faimin. All rights reserved.
//

@import XCTest;
@import Libffi_iOS;

@interface Tests : XCTestCase

@end

@implementation Tests

- (void)setUp
{
    [super setUp];
    // Put setup code here. This method is called before the invocation of each test method in the class.
}

- (void)tearDown
{
    // Put teardown code here. This method is called after the invocation of each test method in the class.
    [super tearDown];
}

- (void)testExample
{
    XCTFail(@"No implementation for \"%s\"", __PRETTY_FUNCTION__);
}

#pragma mark - 调用C函数

static int cFunc(int a , int b, int c) {
    int x = a + b + c;
    return x;
}

- (void)testCallCFunc {
    ffi_cif cif;
    ffi_type *argTypes[] = {&ffi_type_sint, &ffi_type_sint, &ffi_type_sint};
    ffi_prep_cif(&cif, FFI_DEFAULT_ABI, 3, &ffi_type_sint, argTypes);
    
    int a = 123;
    int b = 456;
    int c = 890;
    
    void **args = alloca(sizeof(void *) * 3);
    args[0] = &a;
    args[1] = &b;
    args[2] = &c;
    int retValue;
    ffi_call(&cif, (void *)cFunc, &retValue, args);
    
    int m = cFunc(a, b, c);
    
    NSCAssert(retValue == m, @"值不相等");
}


@end

