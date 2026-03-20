// swift-tools-version: 5.9

import PackageDescription

let package = Package(
    name: "ZDLibffi",
    platforms: [
        .iOS(.v10),
        .macOS(.v10_12),
        .tvOS(.v10),
        .watchOS(.v3),
        .visionOS(.v1)
    ],
    products: [
        .library(
            name: "ZDLibffi",
            type: .static,
            targets: ["ZDLibffi"]
        ),
    ],
    targets: [
        .target(
            name: "ZDLibffi",
            path: "Source",
            publicHeadersPath: "include",
            cSettings: [
                .headerSearchPath("include"),
                .define("USE_DL_PREFIX", to: "1"),
                .define("HAVE_MORECORE", to: "0")
            ]
        ),
    ]
)
