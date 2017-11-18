{ system ? builtins.currentSystem
, pkgs ? import ((import <nixpkgs> {}).pkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "cfafd6f5a819472911eaf2650b50a62f0c143e3e";
    sha256 = "10xgiyh4hbwwiy8qg70ma1f27nd717aflksk9fx3ci8bmxmqbkkn";
  }) { inherit system; }
, python ? "python3"
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
}:

with builtins;
with pkgs.lib;

let

  pip2nix = (import (pkgs.fetchFromGitHub {
    owner = "johbo";
    repo = "pip2nix";
    rev = "714b51eb69711474a9a2fbddf144e5e66b36986b";
    sha256 = "0h7hg95p1v392h4a310ng2kri9r59ailpj3r4mkr6x1dhq6l4fic";
  } + "/release.nix") {}).pip2nix.python36;

  requirements = import ./requirements.nix {
    inherit pkgs;
    inherit (pkgs) fetchurl fetchgit fetchhg;
  };

  overrides = import ./overrides.nix {
    inherit pkgs pythonPackages;
  };

  packages =
    (fix
    (extends overrides
    (extends requirements
             pythonPackages.__unfix__)));

in {

  pip2nix = (pip2nix.python.withPackages (ps: [ pip2nix ])).env;

  pkgs = pkgs;

  pythonPackages = packages;

  env = packages.python.withPackages (ps: map
    (name: getAttr name packages) (attrNames (requirements {} {})));

  shell = (packages.python.withPackages (ps: map
    (name: getAttr name packages) (attrNames (requirements {} {})))).env;

}
