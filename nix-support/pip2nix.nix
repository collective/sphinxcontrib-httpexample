{ pkgs ? import <nixpkgs> {} }:

let

  pip2nix = (import (pkgs.fetchFromGitHub {
    owner = "johbo";
    repo = "pip2nix";
    rev = "714b51eb69711474a9a2fbddf144e5e66b36986b";
    sha256 = "0h7hg95p1v392h4a310ng2kri9r59ailpj3r4mkr6x1dhq6l4fic";
  } + "/release.nix") {}).pip2nix.python36;

in

(pip2nix.python.withPackages (ps: [ pip2nix ])).env
