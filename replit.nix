{pkgs}: {
  deps = [
    pkgs.libuv
    pkgs.glibcLocales
    pkgs.zlib
    pkgs.xcodebuild
    pkgs.cacert
    pkgs.libffi
    pkgs.rustc
    pkgs.pkg-config
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.cargo
    pkgs.libiconv
  ];
}
