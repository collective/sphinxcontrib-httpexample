{ pkgs ? import <nixpkgs> {}
, python ? "python3"
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
}:

with builtins;
with pkgs.lib;

let

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

in

{

  pythonPackages = packages;

  env = packages.python.withPackages (ps: map
    (name: getAttr name packages) (attrNames (requirements {} {})));

  shell = (packages.python.withPackages (ps: map
    (name: getAttr name packages) (attrNames (requirements {} {})))).env;

}
