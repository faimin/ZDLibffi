#
# Be sure to run `pod lib lint Libffi_iOS_static.podspec' to ensure this is a
# valid spec before submitting.
#
# Any lines starting with a # are optional, but their use is encouraged
# To learn more about a Podspec see https://guides.cocoapods.org/syntax/podspec.html
#

Pod::Spec.new do |s|
  s.name             = 'Libffi_iOS_static'
  s.version          = '0.0.1'
  s.summary          = 'Libffi_iOS_static library'
  s.description      = <<-DESC
  libffi v3.3 static library for iOS.
                       DESC
  s.homepage         = 'https://github.com/faimin/Libffi_iOS'
  s.license          = {
    :type => 'MIT',
    :file => 'LICENSE'
  }
  s.author           = { 'faimin' => 'fuxianchao@gmail.com' }
  
  s.platform = :ios, '9.0'
  s.ios.deployment_target = '9.0'
  s.prefix_header_file = false
  s.source           = {
    :git => 'https://github.com/faimin/Libffi_iOS.git',
    :tag => s.version.to_s
  }

  s.header_dir = 'Libffi_iOS_static/include/ffi'
  s.public_header_files = 'Libffi_iOS_static/include/ffi/*.h'
  s.source_files = 'Libffi_iOS_static/**/*.h'
  s.vendored_libraries = 'Libffi_iOS_static/Classes/*.a'
  s.module_name = s.name
  
end
