{ pkgs ? import <nixpkgs> {}
, python ? "python3"
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
, setup ? import (pkgs.fetchFromGitHub {
    owner = "datakurre";
    repo = "setup.nix";
    rev = "41016d8b302b6bb2644eff341fbd8a536dce29bb";
    sha256 = "1s8l69izxzhwcgg5dkbqfq5jgd1847mf9ijzxry68sh8lni6w0q7";
  })
}:

let overrides = self: super: {

};

in setup {
  inherit pkgs pythonPackages overrides;
  src = ./.;
}
