{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    std = {
      url = "github:divnix/std";
      inputs.devshell.url = "github:numtide/devshell";
      inputs.nixago.url = "github:nix-community/nixago";
    };
    semver = {
      url = "sourcehut:~yuiyukihira/semver";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    helpers = {
      url = "sourcehut:~yuiyukihira/devshell";
    };
  };

  outputs = { std, ... }@inputs:
    std.growOn
      {
        inherit inputs;
        cellsFrom = ./nix;
        cellBlocks = [
          (std.blockTypes.runnables "apps")
          (std.blockTypes.installables "packages")
          (std.blockTypes.devshells "devshells")
          (std.blockTypes.nixago "configs")
        ];
      }
      {
        packages = std.harvest inputs.self [ [ "alchemy" "packages" ] ];
        apps = std.harvest inputs.self [ [ "alchemy" "apps" ] ];
        devShells = std.harvest inputs.self [ [ "_automation" "devshells" ] ];
      };
}
