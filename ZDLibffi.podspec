#
# Be sure to run `pod lib lint Libffi_iOS.podspec' to ensure this is a
# valid spec before submitting.
#
# Any lines starting with a # are optional, but their use is encouraged
# To learn more about a Podspec see https://guides.cocoapods.org/syntax/podspec.html
#

Pod::Spec.new do |s|
  s.name             = 'ZDLibffi'
  s.version          = '0.0.1'
  s.summary          = 'Libffi framework for iOS (i386, x86_64, armv7, arm64)'
  s.description      = <<-DESC
  libffi v3.4.2 for iOS (i386, x86_64, armv7, arm64) which support module.
                       DESC
  s.homepage         = 'https://github.com/faimin/ZDLibffi_iOS'
  s.license          = {
    :type => 'MIT',
    :file => 'LICENSE'
  }
  s.author           = { 'faimin' => 'fuxianchao@gmail.com' }
  
  s.platform = :ios, '9.0'
  s.ios.deployment_target = '9.0'
  s.prefix_header_file = false
  s.source           = {
    :git => 'https://github.com/faimin/ZDLibffi_iOS.git',
    :tag => s.version.to_s
  }
  s.module_name = 'ZDLibffi'
  s.pod_target_xcconfig = {
    'DEFINES_MODULE' => 'YES'
  }
  s.source_files = "Source/**/*.{h,c,S}"
  s.public_header_files = "Source/include/*.h"

  
end
