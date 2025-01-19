{ inputs
, cell
}:
let
  inherit (inputs) nixpkgs std;
  l = nixpkgs.lib // builtins;

  src = std.incl (inputs.self) [
    (inputs.self + /configure.ac)
    (inputs.self + /Makefile.am)
    (inputs.self + /src)
    (inputs.self + /alchemy.1.scd)
  ];
in
rec {
  default = alchemy;
  alchemy = nixpkgs.stdenv.mkDerivation {
    name = "alchemy";

    inherit src;

    nativeBuildInputs = with nixpkgs; [ scdoc autoreconfHook pkg-config ];
    buildInputs = with nixpkgs; [ SDL2 ];
  };

  alchemy-dist = nixpkgs.stdenv.mkDerivation {
    name = "alchemy-dist";

    inherit src;

    nativeBuildInputs = with nixpkgs; [ autoconfiHook ];

    buildPhase = ''
      make distcheck
    '';

    installPhase = ''
      mkdir -p $out/share

      cp alchemy-*.tar.gx $out/share/
    '';
  };
}
