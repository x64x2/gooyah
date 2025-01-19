{ lib, config, pkgs, ... }:
{
  config = {
    devshell.packages = [ pkgs.pkg-config ];

    env = [
      {
        name = "PKG_CONFIG_PATH";
        eval = "$DEVSHELL_DIR/lib/pkgconfig";
      }
    ];
  };
}
