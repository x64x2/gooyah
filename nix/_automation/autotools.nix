{ lib, config, pkgs, ... }:
{
  config = {
    commands = [
      {
        name = "make";
        package = pkgs.gnumake;
        category = "cli-dev";
      }
      {
        name = "autoreconf";
        package = pkgs.autoconf;
        category = "cli-dev";
      }
    ];

    devshell.packages = [ pkgs.automake ];

    env = [
      {
        name = "ACLOCAL_PATH";
        eval = "$DEVSHELL_DIR/share/aclocal";
      }
    ];
  };
}
