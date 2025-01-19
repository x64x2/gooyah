{ inputs
, cell
}:
let
  inherit (inputs) nixpkgs std;
  l = nixpkgs.lib // builtins;
in
rec {
  default = std.inputs.flake-utils.lib.mkApp {
    src = cell.packages.default;
  };
  alchemy = std.inputs.flake-utils.lib.mkApp {
    src = cell.packages.alchemy;
  };
}
