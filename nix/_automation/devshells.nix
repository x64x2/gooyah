{ inputs
, cell
}:
let
  inherit (inputs) nixpkgs std;
  l = nixpkgs.lib // builtins;
in
l.mapAttrs (_: std.lib.dev.mkShell) {
  default = { ... }: {
    name = "lusp devshell";

    imports = [
      std.std.devshellProfiles.default
      inputs.helpers.nixosModules.base
      inputs.helpers.nixosModules."language/cpp"
    ];

    language.c.compiler = nixpkgs.gcc;

    includes = with nixpkgs; [ SDL2 ];

    commands = [
      {
        name = "gcc";
        package = nixpkgs.gcc;
        category = "cli-dev";
      }
      {
        package = inputs.semver.packages.semver;
        category = "releases";
        help = "A tool to make creating semantic versioning easier";
      }
      {
        package = nixpkgs.scdoc;
        category = "docs";
      }
    ];

    devshell.packages = l.optional (nixpkgs.stdenv.system != "aarch64-darwin") nixpkgs.gdb;

    nixago = [
      ((std.lib.dev.mkNixago std.lib.cfg.lefthook) cell.configs.lefthook)
      (std.lib.dev.mkNixago cell.configs.prettier)
      ((std.lib.dev.mkNixago std.lib.cfg.treefmt) cell.configs.treefmt)
    ];
  };
}
