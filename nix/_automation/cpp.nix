{ lib, config, pkgs, ... }:
let
  ccfg = config.language.c;

  hasIncludes = lib.length ccfg.includes > 0;
in
with lib;
{
  imports = [
    ./c.nix
  ];

  config = {
    env =
      (lib.optionals hasIncludes [
        {
          name = "CPLUS_INCLUDE_PATH";
          eval = "$DEVSHELL_DIR/include";
        }
      ]);
  };
}
