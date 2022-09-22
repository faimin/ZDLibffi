#
# Be sure to run `pod lib lint Libffi_iOS.podspec' to ensure this is a
# valid spec before submitting.
#
# Any lines starting with a # are optional, but their use is encouraged
# To learn more about a Podspec see https://guides.cocoapods.org/syntax/podspec.html
#

Pod::Spec.new do |s|
  s.name             = 'ZDLibffi'
  s.version          = '0.343.0'
  s.summary          = 'Libffi source code integrate'
  s.description      = <<-DESC
    libffi v3.4.3 integrate to iOS && macOS && watchos && tvos.
                       DESC
  s.homepage         = 'https://github.com/libffi/libffi'
  s.license          = "MIT"
  s.authors          = {
    'atgreen' => 'green@moxielogic.com',
    'faimin' => 'fuxianchao@gmail.com'
  }
  s.source           = {
    :git => 'https://github.com/faimin/ZDLibffi.git',
    :tag => s.version.to_s
  }
  s.prefix_header_file = false
  
  s.ios.deployment_target = '10.0'
  s.osx.deployment_target = '10.12'
  s.watchos.deployment_target = '3.0'
  s.tvos.deployment_target = '10.0'
  
  s.module_name = 'ZDLibffi'
  s.pod_target_xcconfig = {
    'DEFINES_MODULE' => 'YES',
    'GCC_PREPROCESSOR_DEFINITIONS' => 'USE_DL_PREFIX=1 HAVE_MORECORE=0', #ONLY_MSPACES=1
  }
  
  s.source_files = "Source/**/*.{h,c,S}"
  s.public_header_files = "Source/include/*.h"

end
